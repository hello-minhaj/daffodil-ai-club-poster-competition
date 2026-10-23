from .models import CompetitionSettings

def competition_settings(request):
    settings_obj = CompetitionSettings.get_solo()
    return {
        "competition": settings_obj,
        "payment_numbers": {
            "bkash": settings_obj.bkash_number,
            "nagad": settings_obj.nagad_number,
            "rocket": settings_obj.rocket_number,
        },
        "USE_IMAGE_LOGO": True,
    }
