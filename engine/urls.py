from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("hub/", views.hub, name="hub"),
    path("play/start/<int:adventure_id>/", views.start_run, name="start_run"),
    path("play/run/<int:run_id>/node/<int:node_id>/", views.play_node, name="play_node"),
    path("play/run/<int:run_id>/choice/<int:option_id>/", views.process_choice, name="process_choice"),
    path("play/run/<int:run_id>/restart/", views.restart_run, name="restart_run"),
]
