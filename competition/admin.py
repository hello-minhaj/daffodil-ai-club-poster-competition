import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import CompetitionSettings, ResearchCategory, Team, TeamMember, AbstractSubmission

@admin.register(CompetitionSettings)
class CompetitionSettingsAdmin(admin.ModelAdmin):
    list_display = ("title", "registration_deadline", "registration_open", "phase1_fee", "phase2_fee")
    def has_add_permission(self, request):
        return not CompetitionSettings.objects.exists()
    fieldsets = (
        ("Event", {"fields": ("title", "registration_deadline", "final_event_date", "registration_open", "eligibility_text", "no_fydp_notice", "abstract_word_limit")}),
        ("Fees", {"fields": ("phase1_fee", "phase2_fee")}),
        ("Payment", {"fields": ("bkash_number", "nagad_number", "rocket_number", "payment_instructions")}),
        ("Contacts", {"fields": ("contact_primary", "contact_secondary")}),
    )

@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0
    readonly_fields = ("is_leader",)

class AbstractInline(admin.StackedInline):
    model = AbstractSubmission
    extra = 0
    readonly_fields = ("submitted_at", "word_count")

def export_teams_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="competition_teams.csv"'
    writer = csv.writer(response)
    writer.writerow(["Reference", "Team", "Leader username", "Payment method", "Transaction ID", "Payment status", "Review status", "Research title", "Category", "Abstract"])
    for team in queryset.select_related("leader").prefetch_related("abstract"):
        abstract = getattr(team, "abstract", None)
        writer.writerow([team.registration_reference, team.team_name, team.leader.username, team.payment_method, team.transaction_id, team.payment_status, team.review_status, getattr(abstract, "research_title", ""), getattr(abstract, "research_category", ""), getattr(abstract, "abstract_text", "")])
    return response
export_teams_csv.short_description = "Export selected teams and abstracts to CSV"

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("registration_reference", "team_name", "leader", "created_at", "payment_status", "review_status")
    list_filter = ("payment_status", "review_status", "payment_method", "created_at")
    search_fields = ("registration_reference", "team_name", "leader__username", "transaction_id", "abstract__research_title")
    readonly_fields = ("registration_reference", "created_at", "updated_at")
    inlines = [TeamMemberInline, AbstractInline]
    actions = [export_teams_csv]
    fieldsets = (
        ("Team", {"fields": ("leader", "team_name", "registration_reference", "created_at", "updated_at")}),
        ("Payment verification", {"fields": ("payment_method", "transaction_id", "payment_status", "payment_admin_note")}),
        ("Abstract review", {"fields": ("review_status", "admin_note")}),
    )

admin.site.site_header = "Daffodil AI Club — Competition Administration"
admin.site.site_title = "DAC Competition Admin"
admin.site.index_title = "Registration and abstract review"
