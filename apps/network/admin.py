from django.contrib import admin

from apps.network.models import Alert, Device, DeviceGroup, NetworkSettings, TrafficLog


@admin.register(DeviceGroup)
class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "device_type", "ip_address", "mac_address", "status", "group", "last_seen"]
    list_filter = ["status", "device_type", "group", "created_at"]
    search_fields = ["name", "mac_address", "ip_address", "manufacturer"]
    readonly_fields = ["created_at", "updated_at", "last_seen", "connected_since"]
    fieldsets = (
        ("Basic Information", {"fields": ("name", "device_type", "manufacturer", "status")}),
        ("Network Details", {"fields": ("mac_address", "ip_address", "signal_strength")}),
        ("Performance", {"fields": ("upload_speed", "download_speed")}),
        ("Organization", {"fields": ("owner", "group", "notes")}),
        (
            "Timestamps",
            {"fields": ("connected_since", "last_seen", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["title", "severity", "alert_type", "is_read", "device", "created_at"]
    list_filter = ["severity", "alert_type", "is_read", "created_at"]
    search_fields = ["title", "message"]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected alerts marked as read.")

    mark_as_read.short_description = "Mark selected alerts as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Selected alerts marked as unread.")

    mark_as_unread.short_description = "Mark selected alerts as unread"


@admin.register(TrafficLog)
class TrafficLogAdmin(admin.ModelAdmin):
    list_display = ["device", "upload_bytes", "download_bytes", "timestamp"]
    list_filter = ["timestamp", "device"]
    readonly_fields = ["timestamp"]
    date_hierarchy = "timestamp"


@admin.register(NetworkSettings)
class NetworkSettingsAdmin(admin.ModelAdmin):
    list_display = ["ssid", "security_mode", "guest_network_enabled", "dhcp_enabled", "updated_at"]
    fieldsets = (
        ("WiFi Settings", {"fields": ("ssid", "password", "security_mode", "wifi_channel")}),
        ("Guest Network", {"fields": ("guest_network_enabled", "guest_ssid", "guest_password")}),
        ("Bandwidth", {"fields": ("bandwidth_limit_mbps",)}),
        ("DHCP Settings", {"fields": ("dhcp_enabled", "dhcp_start_ip", "dhcp_end_ip")}),
        ("DNS Settings", {"fields": ("dns_primary", "dns_secondary")}),
        ("LAN Settings", {"fields": ("lan_ip",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        # Only allow one settings instance
        return not NetworkSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the settings instance
        return False
