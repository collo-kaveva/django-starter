from django.test import Client, TestCase
from django.urls import reverse

from apps.network.models import Alert, Device, DeviceGroup
from apps.users.models import CustomUser


class DashboardViewTest(TestCase):
    """Test dashboard view."""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123", role=CustomUser.Role.TECHNICIAN
        )

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication."""
        response = self.client.get(reverse("network:dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_authenticated(self):
        """Test dashboard with authenticated user."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")


class DeviceListViewTest(TestCase):
    """Test device list view."""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123", role=CustomUser.Role.TECHNICIAN
        )
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group,
        )

    def test_device_list_requires_login(self):
        """Test that device list requires authentication."""
        response = self.client.get(reverse("network:device_list"))
        self.assertEqual(response.status_code, 302)

    def test_device_list_authenticated(self):
        """Test device list with authenticated user."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:device_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Device")

    def test_device_list_search(self):
        """Test device list search functionality."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:device_list"), {"search": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Device")

    def test_device_list_filter_by_status(self):
        """Test device list filter by status."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:device_list"), {"status": "online"})
        self.assertEqual(response.status_code, 200)


class DeviceDetailViewTest(TestCase):
    """Test device detail view."""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123", role=CustomUser.Role.TECHNICIAN
        )
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group,
        )

    def test_device_detail_requires_login(self):
        """Test that device detail requires authentication."""
        response = self.client.get(reverse("network:device_detail", args=[self.device.id]))
        self.assertEqual(response.status_code, 302)

    def test_device_detail_authenticated(self):
        """Test device detail with authenticated user."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:device_detail", args=[self.device.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Device")


class DeviceCreateViewTest(TestCase):
    """Test device create view."""

    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username="adminuser", email="admin@example.com", password="adminpass123", role=CustomUser.Role.ADMINISTRATOR
        )
        self.tech_user = CustomUser.objects.create_user(
            username="techuser", email="tech@example.com", password="techpass123", role=CustomUser.Role.TECHNICIAN
        )
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")

    def test_device_create_requires_admin(self):
        """Test that device creation requires admin role."""
        self.client.login(email="tech@example.com", password="techpass123")
        response = self.client.get(reverse("network:device_create"))
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_device_create_admin_access(self):
        """Test that admin can access device creation."""
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.get(reverse("network:device_create"))
        self.assertEqual(response.status_code, 200)

    def test_device_create_post(self):
        """Test device creation via POST."""
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.post(
            reverse("network:device_create"),
            {
                "name": "New Device",
                "device_type": Device.DeviceType.LAPTOP,
                "mac_address": "AA:BB:CC:DD:EE:FF",
                "ip_address": "192.168.1.200",
                "status": Device.Status.ONLINE,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Device.objects.filter(name="New Device").exists())


class AlertListViewTest(TestCase):
    """Test alert list view."""

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123", role=CustomUser.Role.TECHNICIAN
        )
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group,
        )
        self.alert = Alert.objects.create(
            severity=Alert.Severity.WARNING,
            alert_type=Alert.AlertType.DEVICE_OFFLINE,
            title="Test Alert",
            message="Test message",
            device=self.device,
        )

    def test_alert_list_requires_login(self):
        """Test that alert list requires authentication."""
        response = self.client.get(reverse("network:alert_list"))
        self.assertEqual(response.status_code, 302)

    def test_alert_list_authenticated(self):
        """Test alert list with authenticated user."""
        self.client.login(email="test@example.com", password="testpass123")
        response = self.client.get(reverse("network:alert_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Alert")


class NetworkSettingsViewTest(TestCase):
    """Test network settings view."""

    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username="adminuser", email="admin@example.com", password="adminpass123", role=CustomUser.Role.ADMINISTRATOR
        )
        self.tech_user = CustomUser.objects.create_user(
            username="techuser", email="tech@example.com", password="techpass123", role=CustomUser.Role.TECHNICIAN
        )

    def test_network_settings_requires_admin(self):
        """Test that network settings requires admin role."""
        self.client.login(email="tech@example.com", password="techpass123")
        response = self.client.get(reverse("network:network_settings"))
        self.assertEqual(response.status_code, 403)  # Permission denied

    def test_network_settings_admin_access(self):
        """Test that admin can access network settings."""
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.get(reverse("network:network_settings"))
        self.assertEqual(response.status_code, 200)


class RoleBasedAccessControlTest(TestCase):
    """Test role-based access control."""

    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username="adminuser", email="admin@example.com", password="adminpass123", role=CustomUser.Role.ADMINISTRATOR
        )
        self.tech_user = CustomUser.objects.create_user(
            username="techuser", email="tech@example.com", password="techpass123", role=CustomUser.Role.TECHNICIAN
        )
        self.group = DeviceGroup.objects.create(name="Test Group", color="#FF0000")
        self.device = Device.objects.create(
            name="Test Device",
            device_type=Device.DeviceType.LAPTOP,
            mac_address="00:11:22:33:44:55",
            ip_address="192.168.1.100",
            group=self.group,
        )

    def test_admin_can_delete_device(self):
        """Test that admin can delete devices."""
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.get(reverse("network:device_delete", args=[self.device.id]))
        self.assertEqual(response.status_code, 200)

    def test_technician_cannot_delete_device(self):
        """Test that technician cannot delete devices."""
        self.client.login(email="tech@example.com", password="techpass123")
        response = self.client.get(reverse("network:device_delete", args=[self.device.id]))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_block_device(self):
        """Test that admin can block devices."""
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.get(reverse("network:device_block", args=[self.device.id]))
        self.assertEqual(response.status_code, 200)

    def test_technician_cannot_block_device(self):
        """Test that technician cannot block devices."""
        self.client.login(email="tech@example.com", password="techpass123")
        response = self.client.get(reverse("network:device_block", args=[self.device.id]))
        self.assertEqual(response.status_code, 403)
