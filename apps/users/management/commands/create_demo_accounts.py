from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Create demo accounts for development and testing"

    def handle(self, *args, **options):
        self.stdout.write("Creating demo accounts...")

        # Ensure groups exist
        admin_group, _ = Group.objects.get_or_create(name="Administrators")
        tech_group, _ = Group.objects.get_or_create(name="Technicians")

        # Create or update Administrator account
        admin_user, created = CustomUser.objects.update_or_create(
            username="admin",
            defaults={
                "email": "admin@netvista.local",
                "is_staff": True,
                "is_superuser": True,
                "role": CustomUser.Role.ADMINISTRATOR,
            },
        )
        admin_user.set_password("Admin123!")
        admin_user.save()
        admin_user.groups.add(admin_group)

        if created:
            self.stdout.write(self.style.SUCCESS("Created Administrator account"))
        else:
            self.stdout.write("Administrator account already exists, password updated")

        # Create or update Technician/User account
        user_user, created = CustomUser.objects.update_or_create(
            username="user",
            defaults={
                "email": "user@netvista.local",
                "is_staff": False,
                "is_superuser": False,
                "role": CustomUser.Role.TECHNICIAN,
            },
        )
        user_user.set_password("User123!")
        user_user.save()
        user_user.groups.add(tech_group)

        if created:
            self.stdout.write(self.style.SUCCESS("Created Technician account"))
        else:
            self.stdout.write("Technician account already exists, password updated")

        self.stdout.write(self.style.SUCCESS("Demo accounts setup complete!"))
        self.stdout.write("\nDemo Accounts:")
        self.stdout.write("  Administrator:")
        self.stdout.write("    Username: admin")
        self.stdout.write("    Email: admin@netvista.local")
        self.stdout.write("    Password: Admin123!")
        self.stdout.write("    Role: Network Administrator (full access)")
        self.stdout.write("\n  Technician:")
        self.stdout.write("    Username: user")
        self.stdout.write("    Email: user@netvista.local")
        self.stdout.write("    Password: User123!")
        self.stdout.write("    Role: Network Technician (limited access)")
        self.stdout.write("\nNote: These accounts are for local development/demo purposes only.")
