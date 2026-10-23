from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CompetitionSettings, Team, AbstractSubmission

class CompetitionSmokeTests(TestCase):
    def test_home_loads_and_has_fydp_rule(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FYDP")
        self.assertContains(response, "countdown")

    def test_word_limit_validation(self):
        from .forms import TeamSubmissionForm
        settings_obj = CompetitionSettings.get_solo()
        settings_obj.abstract_word_limit = 250
        settings_obj.save()
        text = "word " * 251
        form = TeamSubmissionForm(data={
            "team_name":"Test Team", "member_count":"1", "research_title":"Test research",
            "research_category":"AI", "abstract_text":text, "payment_method":"bkash",
            "transaction_id":"ABCD1234", "leader_diu_id":"DIU123", "leader_department":"CSE",
            "leader_phone":"0123456789", "no_fydp_confirm":"on",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("abstract_text", form.errors)

    def test_team_reference_created(self):
        user = get_user_model().objects.create_user(username="leader", password="safe-test-password")
        team = Team.objects.create(leader=user, team_name="Sample", payment_method="bkash", transaction_id="TX1234")
        self.assertTrue(team.registration_reference.startswith("DAC-RPC-"))
