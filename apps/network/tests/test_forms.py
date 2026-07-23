from django.test import TestCase

from apps.network.forms import DeviceForm, DeviceGroupForm, NetworkSettingsForm
from apps.network.models import Device, DeviceGroup
from apps.users.models import CustomUser


class DeviceFormTest(TestCase):
    """Test Device form."""

    def setUp(self):
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_device_form_valid_data(self):
        """Test device form with valid data."""
        form_data = {
            "name": "Test Device",
            "device_type": Device.DeviceType.LAPTOP,
            "manufacturer": "Test Manufacturer",
            "mac_address": "00:11:22:33:44:55",
            "ip_address": "192.168.1.100",
            "signal_strength": -50,
            "upload_speed": 10.5,
            "download_speed": 50.0,
            "status": Device.Status.ONLINE,
            "group": self.group.id,
            "owner": self.user.id,
            "notes": "Test notes",
        }
        form = DeviceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_device_form_missing_required_fields(self):
        """Test device form with missing required fields."""
        form_data = {
            "name": "Test Device",
            # Missing required fields
        }
        form = DeviceForm(data=form_data)
        self.assertFalse(form.is_valid())


class DeviceGroupFormTest(TestCase):
    """Test DeviceGroup form."""

    def test_device_group_form_valid_data(self):
        """Test device group form with valid data."""
        form_data = {"name": "Test Group", "description": "Test description", "color": "#FF0000"}
        form = DeviceGroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_device_group_form_missing_name(self):
        """Test device group form with missing name."""
        form_data = {"description": "Test description", "color": "#FF0000"}
        form = DeviceGroupForm(data=form_data)
        self.assertFalse(form.is_valid())


class NetworkSettingsFormTest(TestCase):
    """Test NetworkSettings form."""

    def test_network_settings_form_valid_data(self):
        """Test network settings form with valid data."""
        form_data = {
            "ssid": "TestWiFi",
            "password": "testpass123",
            "security_mode": "wpa2",
            "wifi_channel": 6,
            "guest_network_enabled": False,
            "bandwidth_limit_mbps": 1000,
            "dhcp_enabled": True,
            "dhcp_start_ip": "192.168.1.100",
            "dhcp_end_ip": "192.168.1.200",
            "dns_primary": "8.8.8.8",
            "dns_secondary": "8.8.4.4",
            "lan_ip": "192.168.1.1",
        }
        form = NetworkSettingsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_network_settings_form_missing_ssid(self):
        """Test network settings form with missing SSID."""
        form_data = {"password": "testpass123", "security_mode": "wpa2"}
        form = NetworkSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
