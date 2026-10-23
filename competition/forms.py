from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Team, TeamMember, AbstractSubmission, CompetitionSettings

User = get_user_model()

class LeaderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, label="Team leader full name")
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

class LeaderLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or account username")

class MemberForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    diu_id = forms.CharField(max_length=60, label="DIU ID")
    department = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40)

class TeamSubmissionForm(forms.Form):
    team_name = forms.CharField(max_length=120)
    member_count = forms.ChoiceField(choices=[("1","Leader only"),("2","Leader + 1 member"),("3","Leader + 2 members")], initial="3")
    research_title = forms.CharField(max_length=250)
    research_category = forms.CharField(max_length=120, help_text="Enter your research field/category.")
    abstract_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 8, "maxlength": 10000}))
    payment_method = forms.ChoiceField(choices=[("bkash","bKash"),("nagad","Nagad"),("rocket","Rocket")])
    transaction_id = forms.CharField(max_length=100)
    leader_diu_id = forms.CharField(max_length=60, label="Leader DIU ID")
    leader_department = forms.CharField(max_length=120, label="Leader department")
    leader_phone = forms.CharField(max_length=40, label="Leader phone")
    no_fydp_confirm = forms.BooleanField(required=True, label="I confirm this is NOT an FYDP/thesis project.")
    def clean_abstract_text(self):
        text = self.cleaned_data["abstract_text"].strip()
        limit = CompetitionSettings.get_solo().abstract_word_limit
        if len(text.split()) > limit:
            raise ValidationError(f"Abstract must be {limit} words or fewer.")
        if len(text.split()) < 20:
            raise ValidationError("Please provide an abstract of at least 20 words.")
        return text
    def clean_transaction_id(self):
        val = self.cleaned_data["transaction_id"].strip()
        if len(val) < 4:
            raise ValidationError("Enter the transaction ID from your payment receipt.")
        return val
    def clean(self):
        cleaned = super().clean()
        settings_obj = CompetitionSettings.get_solo()
        if settings_obj.registration_closed:
            raise ValidationError("Registration is closed.")
        if self.data.get("no_fydp_confirm") not in ("on", "true", "True", "1"):
            raise ValidationError("FYDP/thesis projects are not eligible.")
        return cleaned
