from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("shows", "0002_make_tickets_url_optional"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("token_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("subject", models.CharField(blank=True, max_length=200)),
                ("issuer", models.CharField(blank=True, max_length=200)),
                ("audience", models.CharField(blank=True, max_length=200)),
                ("not_before", models.DateTimeField(blank=True, null=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("extra_claims", models.JSONField(blank=True, default=dict)),
                ("token", models.TextField(editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
