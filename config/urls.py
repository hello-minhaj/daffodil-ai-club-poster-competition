from django.contrib import admin
from django.urls import path
from competition import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("competition-rules/", views.rules, name="rules"),
    path("prize-pool/", views.prizes, name="prizes"),
    path("developer/", views.developer, name="developer"),
]
