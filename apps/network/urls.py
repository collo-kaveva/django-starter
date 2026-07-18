from django.shortcuts import render
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    
    # Devices
    path("devices/", views.device_list, name="device_list"),
    path("devices/<int:device_id>/", views.device_detail, name="device_detail"),
    path("devices/create/", views.device_create, name="device_create"),
    path("devices/<int:device_id>/update/", views.device_update, name="device_update"),
    path("devices/<int:device_id>/delete/", views.device_delete, name="device_delete"),
    path("devices/<int:device_id>/disconnect/", views.device_disconnect, name="device_disconnect"),
    path("devices/<int:device_id>/block/", views.device_block, name="device_block"),
    path("devices/<int:device_id>/unblock/", views.device_unblock, name="device_unblock"),
    
    # Alerts
    path("alerts/", views.alert_list, name="alert_list"),
    path("alerts/<int:alert_id>/mark-read/", views.alert_mark_read, name="alert_mark_read"),
    path("alerts/mark-all-read/", views.alert_mark_all_read, name="alert_mark_all_read"),
    
    # Network Settings
    path("settings/", views.network_settings, name="network_settings"),
    
    # Device Groups
    path("groups/", views.device_group_list, name="device_group_list"),
    path("groups/create/", views.device_group_create, name="device_group_create"),
    path("groups/<int:group_id>/update/", views.device_group_update, name="device_group_update"),
    path("groups/<int:group_id>/delete/", views.device_group_delete, name="device_group_delete"),
    
    # Offline page for PWA
    path("offline/", views.offline_page, name="offline"),
]
