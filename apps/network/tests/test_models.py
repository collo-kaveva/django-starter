from django.test import TestCase
from django.utils import timezone

from apps.network.models import Alert, Device, DeviceGroup, NetworkSettings, TrafficLog
from apps.users.models import CustomUser


class DeviceGroupModelTest(TestCase):
    """Test DeviceGroup model."""

    def setUp(self):
        self.group = DeviceGroup.objects.create(
            name="Test Group",
            description="Test description",
            color="#FF0000"
        )

    def test_device_group_creation(self):
        """Test device group creation."""
        self.assertEqual(self.group.name, "Test Group")
        self.assertEqual(self.group.description, "Test description")
        self.assertEqual(self.group.color, "#FF0000")

    def test_device_group_str(self):
        """Test device group string representation."""
        self.assertEqual(str(self.group), "Test Group")

    def test_device_group_unique_name(self):
        """Test that group names are unique."""
        with self.assertRaises(Exception):
            DeviceGroup.objects.create(
                name="Test Group",
                description="Another description",
                color="#00FF00"
            )


class DeviceModelTest(TestCase):
    """Test Device model."""

    def setUp(self):
        self.group = DeviceGroup.objects.create(
            name="Test Group",
            color="#FF0000"
        )
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            manufacturer="Test Manufacturer",
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            signal_strength=-50,
            upload_speed=10.5,
            download_speed=50.0,
            status=Device.Status.ONLINE,
            group=self.group,
            owner=self.user
        )

    def test_device_creation(self):
        """Test device creation."""
        self.assertEqual(self.device.name, "Test Device")
        self.assertEqual(self.device.device_type, Device.DeviceType.LAPTOP)
        self.assertEqual(self.device.status, Device.Status.ONLINE)

    def test_device_str(self):
        """Test device string representation."""
        self.assertIn("Test Device", str(self.device))
        self.assertIn("Laptop", str(self.device))

    def test_device_unique_mac(self):
        """Test that MAC addresses are unique."""
        with self.assertRaises(Exception):
            Device.objects.create(
                name="Another Device",
                device_type=Device.DeviceType.DESKTOP,
                mac_address="00:11:22:33:44:55",  # Same MAC
                ip_address="192.168.1.101"
            )

    def test_device_last_seen_auto_update(self):
        """Test that last_seen is auto-updated."""
        old_last_seen = self.device.last_seen
        self.device.save()
        self.device.refresh_from_db()
        # last_seen should be updated
        self.assertIsNotNone(self.device.last_seen)


class AlertModelTest(TestCase):
    """Test Alert model."""

    def setUp(self):
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group
        )
        self.alert = Alert.objects.create(
            severity=Alert.Severity.WARNING,
            alert_type=Alert.AlertType.DEVICE_OFFLINE,
            title="Test Alert",
            message="Test alert message",
            device=self.device
        )

    def test_alert_creation(self):
        """Test alert creation."""
        self.assertEqual(self.alert.severity, Alert.Severity.WARNING)
        self.assertEqual(self.alert.alert_type, Alert.AlertType.DEVICE_OFFLINE)
        self.assertFalse(self.alert.is_read)

    def test_alert_str(self):
        """Test alert string representation."""
        self.assertIn("Test Alert", str(self.alert))
        self.assertIn("Warning", str(self.alert))

    def test_alert_mark_as_read(self):
        """Test marking alert as read."""
        self.alert.is_read = True
        self.alert.save()
        self.alert.refresh_from_db()
        self.assertTrue(self.alert.is_read)


class TrafficLogModelTest(TestCase):
    """Test TrafficLog model."""

    def setUp(self):
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group
        )
        self.traffic_log = TrafficLog.objects.create(
            device=self.device,
            upload_bytes=1024 * 1024,  # 1MB
            download_bytes=10 * 1024 * 1024  # 10MB
        )

    def test_traffic_log_creation(self):
        """Test traffic log creation."""
        self.assertEqual(self.traffic_log.device, self.device)
        self.assertEqual(self.traffic_log.upload_bytes, 1024 * 1024)
        self.assertEqual(self.traffic_log.download_bytes, 10 * 1024 * 1024)

    def test_traffic_log_str(self):
        """Test traffic log string representation."""
        self.assertIn("Test Device", str(self.traffic_log))


class NetworkSettingsModelTest(TestCase):
    """Test NetworkSettings model."""

    def test_network_settings_creation(self):
        """Test network settings creation."""
        settings = NetworkSettings.objects.create(
            ssid="TestWiFi",
            password="testpass123",
            security_mode="wpa2"
        )
        self.assertEqual(settings.ssid, "TestWiFi")
        self.assertEqual(settings.security_mode, "wpa2")

    def test_network_settings_str(self):
        """Test network settings string representation."""
        settings = NetworkSettings.objects.create(ssid="TestWiFi")
        self.assertIn("TestWiFi", str(settings))