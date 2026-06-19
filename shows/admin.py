from django.contrib import admin
from django.utils.html import format_html

from .models import ApiToken, Show

admin.site.site_header = ""
admin.site.site_title = ""
admin.site.index_title = "Administración de Shows"
admin.site.site_url = "https://dangerous.cl"


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "time",
        "country",
        "city",
        "venue",
        "archived",
    )
    list_filter = ("archived", "date", "country", "city")
    search_fields = ("country", "city", "venue")


@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "issuer",
        "audience",
        "expires_at",
        "created_at",
        "short_token",
    )
    list_filter = ("issuer", "audience", "expires_at", "created_at")
    search_fields = ("name", "subject", "issuer", "audience", "token_id", "token")
    readonly_fields = ("token_copy", "created_at", "token_id")
    fieldsets = (
        (None, {"fields": ("name", "subject")}),
        (
            "Claims",
            {
                "fields": (
                    "issuer",
                    "audience",
                    "not_before",
                    "expires_at",
                    "extra_claims",
                    "token_id",
                    "token_copy",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    def token_copy(self, obj):
        if not obj.token:
            return ""
        return format_html(
            '<code class="token-code js-copy-token" data-token="{}" title="Copiar token" role="button" tabindex="0">{}</code>',
            obj.token,
            obj.token,
        )

    token_copy.short_description = "Token"

    def short_token(self, obj):
        if not obj.token:
            return ""
        return format_html(
            '<code class="token-code js-copy-token" data-token="{}" title="Copiar token" role="button" tabindex="0">{}...{}</code>',
            obj.token,
            obj.token[:12],
            obj.token[-8:],
        )

    short_token.short_description = "Token"
