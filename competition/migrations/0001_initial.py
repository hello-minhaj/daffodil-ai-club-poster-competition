import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="CompetitionSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Daffodil AI Club Research Poster Competition", max_length=200)),
                ("registration_deadline", models.DateTimeField(default=django.utils.timezone.datetime(2026, 11, 2, 23, 59, tzinfo=django.utils.timezone.get_current_timezone()))),
                ("final_event_date", models.DateField(default=django.utils.timezone.datetime(2026, 11, 15).date())),
                ("phase1_fee", models.PositiveIntegerField(default=150)),
                ("phase2_fee", models.PositiveIntegerField(default=350)),
                ("registration_open", models.BooleanField(default=True)),
                ("bkash_number", models.CharField(default="+880 1521-564540", max_length=40)),
                ("nagad_number", models.CharField(default="+880 1521-564540", max_length=40)),
                ("rocket_number", models.CharField(default="+880 1521-564540", max_length=40)),
                ("payment_instructions", models.TextField(default="Send the Phase 1 fee to one of the official numbers above using your own mobile financial service account. Enter the transaction ID below. Organizers will verify it manually. Never share PINs or OTPs.")),
                ("contact_primary", models.CharField(default="Md Latifur Rahman Rafi, President, Daffodil AI Club — +880 1856-862093", max_length=180)),
                ("contact_secondary", models.CharField(default="Md Minhajul Islam, Vice President, Daffodil AI Club — 01630087726", max_length=180)),
                ("eligibility_text", models.CharField(default="Open to Daffodil International University (DIU) students only.", max_length=255)),
                ("no_fydp_notice", models.CharField(default="FYDP/thesis projects are NOT eligible for this competition.", max_length=300)),
                ("abstract_word_limit", models.PositiveSmallIntegerField(default=250, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(1000)])),
            ],
            options={"verbose_name": "Competition settings", "verbose_name_plural": "Competition settings"},
        ),
        migrations.CreateModel(
            name="ResearchCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("team_name", models.CharField(max_length=120)),
                ("registration_reference", models.CharField(editable=False, max_length=24, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("payment_method", models.CharField(choices=[("bkash", "bKash"), ("nagad", "Nagad"), ("rocket", "Rocket")], max_length=20)),
                ("transaction_id", models.CharField(max_length=100)),
                ("payment_status", models.CharField(choices=[("pending", "Pending verification"), ("verified", "Verified"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("payment_admin_note", models.TextField(blank=True)),
                ("review_status", models.CharField(choices=[("submitted", "Submitted"), ("under_review", "Under review"), ("qualified", "Qualified"), ("not_qualified", "Not qualified")], default="submitted", max_length=20)),
                ("admin_note", models.TextField(blank=True)),
                ("leader", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="competition_teams", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("diu_id", models.CharField(max_length=60)),
                ("department", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=40)),
                ("is_leader", models.BooleanField(default=False)),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="members", to="competition.team")),
            ],
            options={"ordering": ["-is_leader", "id"]},
        ),
        migrations.CreateModel(
            name="AbstractSubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("research_title", models.CharField(max_length=250)),
                ("research_category", models.CharField(help_text="Enter your research field/category.", max_length=120)),
                ("abstract_text", models.TextField()),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("word_count", models.PositiveIntegerField(default=0)),
                ("fy_dp_confirmed", models.BooleanField(default=False, verbose_name="Confirmed not FYDP/thesis")),
                ("team", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="abstract", to="competition.team")),
            ],
        ),
    ]
