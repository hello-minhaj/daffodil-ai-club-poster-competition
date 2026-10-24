from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
import uuid

class CompetitionSettings(models.Model):
    title = models.CharField(max_length=200, default="Daffodil AI Club Research Poster Competition 2026")
    registration_deadline = models.DateTimeField(default=timezone.datetime(2026, 11, 2, 23, 59, tzinfo=timezone.get_current_timezone()))
    final_event_date = models.DateField(default=timezone.datetime(2026, 11, 15).date())
    phase1_fee = models.PositiveIntegerField(default=150)
    phase2_fee = models.PositiveIntegerField(default=350)
    registration_open = models.BooleanField(default=True)
    bkash_number = models.CharField(max_length=40, default="+880 1521-564540")
    nagad_number = models.CharField(max_length=40, default="+880 1521-564540")
    rocket_number = models.CharField(max_length=40, default="+880 1521-564540")
    payment_instructions = models.TextField(default="Send the Phase 1 fee to one of the official numbers above using your own mobile financial service account. Enter the transaction ID below. Organizers will verify it manually. Never share PINs or OTPs.")
    contact_primary = models.CharField(max_length=180, default="Md Latifur Rahman Rafi, President, Daffodil AI Club — +880 1856-862093")
    contact_secondary = models.CharField(max_length=180, default="Md Minhajul Islam, Vice President, Daffodil AI Club — 01630087726")
    eligibility_text = models.CharField(max_length=255, default="Open to Daffodil International University (DIU) students only.")
    no_fydp_notice = models.CharField(max_length=300, default="FYDP/thesis projects are NOT eligible for this competition.")
    abstract_word_limit = models.PositiveSmallIntegerField(default=250, validators=[MinValueValidator(50), MaxValueValidator(1000)])

    class Meta:
        verbose_name = "Competition settings"
        verbose_name_plural = "Competition settings"

    def __str__(self):
        return self.title

    @classmethod
    def get_solo(cls):
        obj = cls.objects.order_by("pk").first()
        if obj:
            return obj
        return cls.objects.create()

    @property
    def registration_closed(self):
        return (not self.registration_open) or timezone.now() > self.registration_deadline

class ResearchCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Team(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending verification"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
    class ReviewStatus(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under review"
        QUALIFIED = "qualified", "Qualified"
        NOT_QUALIFIED = "not_qualified", "Not qualified"

    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="competition_teams")
    team_name = models.CharField(max_length=120)
    registration_reference = models.CharField(max_length=24, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20, choices=[("bkash","bKash"),("nagad","Nagad"),("rocket","Rocket")])
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_admin_note = models.TextField(blank=True)
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.SUBMITTED)
    admin_note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.registration_reference:
            self.registration_reference = "DAC-RPC-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration_reference} — {self.team_name}"

    @property
    def member_count(self):
        return self.members.count()

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    full_name = models.CharField(max_length=120)
    diu_id = models.CharField(max_length=60)
    department = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    is_leader = models.BooleanField(default=False)
    class Meta:
        ordering = ["-is_leader", "id"]
    def __str__(self):
        return f"{self.full_name} ({self.diu_id})"

class AbstractSubmission(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="abstract")
    research_title = models.CharField(max_length=250)
    research_category = models.CharField(max_length=120, help_text="Enter your research field/category.")
    abstract_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    word_count = models.PositiveIntegerField(default=0)
    fy_dp_confirmed = models.BooleanField(default=False, verbose_name="Confirmed not FYDP/thesis")

    def __str__(self):
        return self.research_title
