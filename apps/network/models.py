from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomUser
from apps.utils.models import BaseModel


class DeviceGroup(BaseModel):
    """Group for organizing devices (e.g., Office, Home, Guests, IoT)."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code for group identification")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Device Group")
        verbose_name_plural = _("Device Groups")

    def __str__(self):
        return self.name


class Device(BaseModel):
    """Network device with simulated network information."""

    class DeviceType(models.TextChoices):
        LAPTOP = "laptop", _("Laptop")
        DESKTOP = "desktop", _("Desktop")
        SMARTPHONE = "smartphone", _("Smartphone")
        TABLET = "tablet", _("Tablet")
        PRINTER = "printer", _("Printer")
        CAMERA = "camera", _("Camera")
        SMART_TV = "smart_tv", _("Smart TV")
        IOT_DEVICE = "iot_device", _("IoT Device")
        ROUTER = "router", _("Router")
        SWITCH = "switch", _("Switch")

    class Status(models.TextChoices):
        ONLINE = "online", _("Online")
        OFFLINE = "offline", _("Offline")
        BLOCKED = "blocked", _("Blocked")

    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DeviceType.choices, default=DeviceType.LAPTOP)
    manufacturer = models.CharField(max_length=100, blank=True)
    mac_address = models.CharField(max_length=17, unique=True, help_text="Format: XX:XX:XX:XX:XX:XX")
    ip_address = models.CharField(max_length=45, help_text="IPv4 or IPv6 address")
    signal_strength = models.IntegerField(default=0, help_text="Signal strength in dBm (-100 to 0)")
    upload_speed = models.FloatField(default=0.0, help_text="Upload speed in Mbps")
    download_speed = models.FloatField(default=0.0, help_text="Download speed in Mbps")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONLINE)
    last_seen = models.DateTimeField(auto_now=True)
    connected_since = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices")
    group = models.ForeignKey(DeviceGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-last_seen"]
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        indexes = [
            models.Index(fields=["mac_address"]),
            models.Index(fields=["ip_address"]),
            models.Index(fields=["status"]),
            models.Index(fields=["device_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_device_type_display()})"


class Alert(BaseModel):
    """Network alerts and notifications."""

    class Severity(models.TextChoices):
        INFO = "info", _("Info")
        WARNING = "warning", _("Warning")
        ERROR = "error", _("Error")
        CRITICAL = "critical", _("Critical")

    class AlertType(models.TextChoices):
        NEW_DEVICE = "new_device", _("New Device Connected")
        DEVICE_OFFLINE = "device_offline", _("Device Offline")
        HIGH_CPU = "high_cpu", _("High CPU Usage")
        FIRMWARE_UPDATE = "firmware_update", _("Firmware Update Available")
        WEAK_PASSWORD = "weak_password", _("Weak Password")
        HIGH_BANDWIDTH = "high_bandwidth", _("High Bandwidth Usage")

    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.INFO)
    alert_type = models.CharField(max_length=30, choices=AlertType.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True, related_name="alerts")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")
        indexes = [
            models.Index(fields=["is_read"]),
            models.Index(fields=["severity"]),
            models.Index(fields=["alert_type"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"


class TrafficLog(BaseModel):
    """Historical traffic records for devices."""

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="traffic_logs")
    upload_bytes = models.BigIntegerField(default=0, help_text="Upload in bytes")
    download_bytes = models.BigIntegerField(default=0, help_text="Download in bytes")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("Traffic Log")
        verbose_name_plural = _("Traffic Logs")
        indexes = [
            models.Index(fields=["device", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"


class NetworkSettings(BaseModel):
    """Simulated network settings."""

    ssid = models.CharField(max_length=100, default="NetVista-WiFi")
    password = models.CharField(max_length=100, default="securepassword123")
    guest_network_enabled = models.BooleanField(default=False)
    guest_ssid = models.CharField(max_length=100, default="NetVista-Guest")
    guest_password = models.CharField(max_length=100, blank=True)
    security_mode = models.CharField(
        max_length=20,
        choices=[
            ("wpa2", "WPA2"),
            ("wpa3", "WPA3"),
            ("wep", "WEP"),
        ],
        default="wpa2",
    )
    wifi_channel = models.IntegerField(default=6, help_text="WiFi channel (1-11)")
    bandwidth_limit_mbps = models.IntegerField(default=1000, help_text="Bandwidth limit in Mbps")
    dhcp_enabled = models.BooleanField(default=True)
    dhcp_start_ip = models.CharField(max_length=15, default="192.168.1.100")
    dhcp_end_ip = models.CharField(max_length=15, default="192.168.1.200")
    dns_primary = models.CharField(max_length=15, default="8.8.8.8")
    dns_secondary = models.CharField(max_length=15, default="8.8.4.4")
    lan_ip = models.CharField(max_length=15, default="192.168.1.1")

    class Meta:
        verbose_name = _("Network Settings")
        verbose_name_plural = _("Network Settings")

    def __str__(self):
        return f"Network Settings ({self.ssid})"
