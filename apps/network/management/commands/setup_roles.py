from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.network.models import Alert, Device, DeviceGroup, NetworkSettings


class Command(BaseCommand):
    help = "Set up administrator and technician groups with appropriate permissions"

    def handle(self, *args, **options):
        self.stdout.write("Setting up user roles and permissions...")

        # Create or get Administrator group
        admin_group, created = Group.objects.get_or_create(name="Administrators")
        if created:
            self.stdout.write(self.style.SUCCESS("Created Administrators group"))
        else:
            self.stdout.write("Administrators group already exists")

        # Create or get Technician group
        tech_group, created = Group.objects.get_or_create(name="Technicians")
        if created:
            self.stdout.write(self.style.SUCCESS("Created Technicians group"))
        else:
            self.stdout.write("Technicians group already exists")

        # Get content types for network models
        device_ct = ContentType.objects.get_for_model(Device)
        group_ct = ContentType.objects.get_for_model(DeviceGroup)
        alert_ct = ContentType.objects.get_for_model(Alert)
        settings_ct = ContentType.objects.get_for_model(NetworkSettings)

        # Administrator permissions (full access)
        admin_permissions = [
            # Device permissions
            *Permission.objects.filter(content_type=device_ct),
            # DeviceGroup permissions
            *Permission.objects.filter(content_type=group_ct),
            # Alert permissions
            *Permission.objects.filter(content_type=alert_ct),
            # NetworkSettings permissions
            *Permission.objects.filter(content_type=settings_ct),
        ]

        for permission in admin_permissions:
            admin_group.permissions.add(permission)

        self.stdout.write(f"Added {len(admin_permissions)} permissions to Administrators group")

        # Technician permissions (read-only + limited write)
        tech_permissions = [
            # Device view permissions
            Permission.objects.get(codename="view_device", content_type=device_ct),
            Permission.objects.get(codename="change_device", content_type=device_ct),
            # DeviceGroup view permissions
            Permission.objects.get(codename="view_devicegroup", content_type=group_ct),
            # Alert view permissions
            Permission.objects.get(codename="view_alert", content_type=alert_ct),
            Permission.objects.get(codename="change_alert", content_type=alert_ct),
            # NetworkSettings view permissions
            Permission.objects.get(codename="view_networksettings", content_type=settings_ct),
        ]

        for permission in tech_permissions:
            tech_group.permissions.add(permission)

        self.stdout.write(f"Added {len(tech_permissions)} permissions to Technicians group")

        self.stdout.write(self.style.SUCCESS("Role setup complete!"))
        self.stdout.write("\nGroups created:")
        self.stdout.write("  - Administrators (full access)")
        self.stdout.write("  - Technicians (read-only + limited device management)")
        self.stdout.write("\nTo assign a user to a group:")
        self.stdout.write("  python manage.py shell")
        self.stdout.write("  >>> from django.contrib.auth.models import User, Group")
        self.stdout.write('  >>> user = User.objects.get(email="user@example.com")')
        self.stdout.write('  >>> group = Group.objects.get(name="Administrators")')
        self.stdout.write("  >>> user.groups.add(group)")
