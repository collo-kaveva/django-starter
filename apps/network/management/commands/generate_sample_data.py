import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.network.models import Alert, Device, DeviceGroup, NetworkSettings, TrafficLog


class Command(BaseCommand):
    help = "Generate sample data for NetVista dashboard"

    def handle(self, *args, **options):
        self.stdout.write("Generating sample data for NetVista...")

        # Create device groups
        self.stdout.write("Creating device groups...")
        groups_data = [
            {"name": "Office", "description": "Office devices", "color": "#3B82F6"},
            {"name": "Home", "description": "Home devices", "color": "#10B981"},
            {"name": "Guests", "description": "Guest devices", "color": "#F59E0B"},
            {"name": "Security", "description": "Security cameras", "color": "#EF4444"},
            {"name": "IoT", "description": "IoT devices", "color": "#8B5CF6"},
            {"name": "Gaming", "description": "Gaming devices", "color": "#EC4899"},
        ]

        groups = []
        for group_data in groups_data:
            group, created = DeviceGroup.objects.get_or_create(
                name=group_data["name"],
                defaults={"description": group_data["description"], "color": group_data["color"]},
            )
            if created:
                groups.append(group)
                self.stdout.write(f"  Created group: {group.name}")
            else:
                groups.append(group)

        # Create network settings if not exists
        self.stdout.write("Creating network settings...")
        if not NetworkSettings.objects.exists():
            NetworkSettings.objects.create()
            self.stdout.write("  Created network settings")
        else:
            self.stdout.write("  Network settings already exist")

        # Create devices
        self.stdout.write("Creating devices...")
        device_types = Device.DeviceType.choices
        manufacturers = ["Apple", "Samsung", "Dell", "HP", "Lenovo", "Asus", "TP-Link", "Netgear", "Cisco", "Google"]

        devices = []
        for i in range(50):
            device_type = random.choice(device_types)[0]
            manufacturer = random.choice(manufacturers)
            group = random.choice(groups)

            # Generate realistic data
            mac_address = ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])
            ip_address = f"192.168.1.{random.randint(2, 254)}"
            signal_strength = random.randint(-80, -30)
            upload_speed = random.uniform(0.1, 50.0)
            download_speed = random.uniform(1.0, 100.0)
            status = random.choice(Device.Status.choices)[0]

            device = Device.objects.create(
                name=f"{manufacturer} {device_type.replace('_', ' ').title()} {i + 1}",
                device_type=device_type,
                manufacturer=manufacturer,
                mac_address=mac_address,
                ip_address=ip_address,
                signal_strength=signal_strength,
                upload_speed=upload_speed,
                download_speed=download_speed,
                status=status,
                group=group,
                notes="Sample device" if random.random() > 0.7 else "",
            )
            devices.append(device)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"  Created {i + 1} devices...")

        self.stdout.write(f"  Total devices created: {len(devices)}")

        # Create traffic logs (simplified - fewer logs to avoid performance issues)
        self.stdout.write("Creating traffic logs...")
        now = timezone.now()
        for device in devices:
            # Create fewer traffic logs for better performance
            for day in range(3):  # Last 3 days instead of 7
                for hour in range(8, 20, 4):  # Every 4 hours during daytime
                    if random.random() > 0.2:  # 80% chance of traffic
                        timestamp = now - timedelta(days=day, hours=hour)
                        upload_bytes = random.randint(1024, 10 * 1024 * 1024)  # 1KB to 10MB
                        download_bytes = random.randint(1024, 100 * 1024 * 1024)  # 1KB to 100MB

                        TrafficLog.objects.create(
                            device=device, upload_bytes=upload_bytes, download_bytes=download_bytes, timestamp=timestamp
                        )

        self.stdout.write("  Traffic logs created")

        # Create alerts
        self.stdout.write("Creating alerts...")
        alert_types = Alert.AlertType.choices
        severities = Alert.Severity.choices

        for _ in range(20):  # Reduced from 30 to 20
            alert_type = random.choice(alert_types)[0]
            severity = random.choice(severities)[0]
            device = random.choice(devices) if random.random() > 0.3 else None

            alert_titles = {
                "new_device": "New Device Connected",
                "device_offline": "Device Went Offline",
                "high_cpu": "High CPU Usage Detected",
                "firmware_update": "Firmware Update Available",
                "weak_password": "Weak Password Detected",
                "high_bandwidth": "High Bandwidth Usage",
            }

            alert_messages = {
                "new_device": f"{device.name if device else 'Unknown device'} has connected to the network.",
                "device_offline": f"{device.name if device else 'Unknown device'} has gone offline.",
                "high_cpu": f"{device.name if device else 'Unknown device'} is experiencing high CPU usage.",
                "firmware_update": f"Firmware update available for {device.name if device else 'device'}.",
                "weak_password": f"Weak password detected on {device.name if device else 'device'}.",
                "high_bandwidth": f"{device.name if device else 'Unknown device'} is using excessive bandwidth.",
            }

            is_read = random.random() > 0.5  # 50% chance of being read

            Alert.objects.create(
                severity=severity,
                alert_type=alert_type,
                title=alert_titles.get(alert_type, "Network Alert"),
                message=alert_messages.get(alert_type, "Something happened on the network."),
                is_read=is_read,
                device=device,
            )

        self.stdout.write("  Alerts created")

        self.stdout.write(self.style.SUCCESS("Sample data generation complete!"))
        self.stdout.write("Summary:")
        self.stdout.write(f"  - Device Groups: {DeviceGroup.objects.count()}")
        self.stdout.write(f"  - Devices: {Device.objects.count()}")
        self.stdout.write(f"  - Traffic Logs: {TrafficLog.objects.count()}")
        self.stdout.write(f"  - Alerts: {Alert.objects.count()}")
        self.stdout.write(f"  - Network Settings: {NetworkSettings.objects.count()}")
