from datetime import datetime, timedelta
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class ShowQuerySet(models.QuerySet):
    def archive_expired(self, now=None):
        now = now or timezone.now()
        expired_ids = []
        for show in self.filter(archived=False).only("id", "date", "time"):
            show_datetime = show.get_show_datetime()
            if show_datetime + timedelta(hours=12) <= now:
                expired_ids.append(show.id)
        if expired_ids:
            self.filter(id__in=expired_ids).update(archived=True)
        return expired_ids


class Show(models.Model):
    date = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    time = models.TimeField()
    tickets_url = models.URLField(max_length=500, blank=True, null=True)
    instagram_post_url = models.URLField(max_length=500)
    archived = models.BooleanField(default=False)

    objects = ShowQuerySet.as_manager()

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.city} - {self.date} {self.time}"

    def get_show_datetime(self):
        combined = datetime.combine(self.date, self.time)
        if settings.USE_TZ:
            return timezone.make_aware(combined, timezone.get_current_timezone())
        return combined


class ApiToken(models.Model):
    name = models.CharField(max_length=200)
    token_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subject = models.CharField(max_length=200, blank=True)
    issuer = models.CharField(max_length=200, blank=True)
    audience = models.CharField(max_length=200, blank=True)
    not_before = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    extra_claims = models.JSONField(default=dict, blank=True)
    token = models.TextField(unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Api Token"
        verbose_name_plural = "Api Tokens"

    def __str__(self):
        return self.name

    def _to_timestamp(self, value):
        if value is None:
            return None
        if timezone.is_naive(value) and settings.USE_TZ:
            value = timezone.make_aware(value, timezone.get_current_timezone())
        return int(value.timestamp())

    def build_payload(self):
        payload = {"jti": str(self.token_id)}

        if self.subject:
            payload["sub"] = self.subject

        issuer = self.issuer or settings.JWT_ISSUER
        if issuer:
            payload["iss"] = issuer

        audience = self.audience or settings.JWT_AUDIENCE
        if audience:
            payload["aud"] = audience

        nbf = self._to_timestamp(self.not_before)
        if nbf is not None:
            payload["nbf"] = nbf

        exp = self._to_timestamp(self.expires_at)
        if exp is not None:
            payload["exp"] = exp

        if self.extra_claims:
            for key, value in self.extra_claims.items():
                if key not in payload:
                    payload[key] = value

        return payload

    def save(self, *args, **kwargs):
        from .auth import create_jwt

        self.token = create_jwt(self.build_payload())
        super().save(*args, **kwargs)
