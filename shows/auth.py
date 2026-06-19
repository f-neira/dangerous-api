import base64
import hashlib
import hmac
import json
import time
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.apps import apps

STANDARD_TOKEN_ERROR = "El TOKEN entregado no es valido."


def _b64url_decode(segment):
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def _b64url_encode(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode("ascii")


def _unauthorized(message):
    response = JsonResponse({"error": message}, status=401)
    response["WWW-Authenticate"] = 'Bearer realm="api"'
    return response


def _token_registered(token):
    ApiToken = apps.get_model("shows", "ApiToken")
    return ApiToken.objects.filter(token=token).exists()


def _validate_claims(payload):
    now = int(time.time())

    if "exp" in payload and now >= int(payload["exp"]):
        return False, "Token expirado."

    if "nbf" in payload and now < int(payload["nbf"]):
        return False, "Token aun no valido."

    if settings.JWT_ISSUER and payload.get("iss") != settings.JWT_ISSUER:
        return False, "Issuer invalido."

    if settings.JWT_AUDIENCE:
        aud_claim = payload.get("aud")
        if isinstance(aud_claim, list):
            if settings.JWT_AUDIENCE not in aud_claim:
                return False, "Audience invalido."
        elif aud_claim != settings.JWT_AUDIENCE:
            return False, "Audience invalido."

    return True, ""


def verify_jwt(token, secret):
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        return False, "El TOKEN entregado no es valido.", None

    try:
        header = json.loads(_b64url_decode(header_b64))
        payload = json.loads(_b64url_decode(payload_b64))
        signature = _b64url_decode(signature_b64)
    except (ValueError, json.JSONDecodeError):
        return False, "El TOKEN entregado no es valido.", None

    if header.get("alg") != "HS256":
        return False, "Algoritmo no soportado.", None

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected):
        return False, "Firma invalida.", None

    claims_ok, message = _validate_claims(payload)
    if not claims_ok:
        return False, message, None

    return True, "", payload


def require_jwt(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return _unauthorized(STANDARD_TOKEN_ERROR)

        token = auth_header[len("Bearer ") :].strip()
        if not token:
            return _unauthorized(STANDARD_TOKEN_ERROR)

        ok, message, payload = verify_jwt(token, settings.JWT_SECRET)
        if not ok:
            return _unauthorized(message or STANDARD_TOKEN_ERROR)

        if not _token_registered(token):
            return _unauthorized("Token revocado o desconocido.")

        request.jwt_payload = payload
        return view_func(request, *args, **kwargs)

    return _wrapped


def create_jwt(payload, secret=None):
    secret = secret or settings.JWT_SECRET
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"
