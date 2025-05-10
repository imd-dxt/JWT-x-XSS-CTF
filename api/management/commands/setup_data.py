# Step 1: Create the management command structure
# Inside your app directory (e.g., 'api'), create these directories and files:
#
# api/
# └── management/
#     └── commands/
#         └── setup_ctf_data.py

# Content for setup_ctf_data.py:
from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Sets up initial data for the JWT Payload CTF challenge'

    def handle(self, *args, **kwargs):
        self.stdout.write("Setting up initial data for JWT Payload CTF challenge...")
        self.setup_users()
        self.stdout.write(self.style.SUCCESS("Setup complete!"))

    def setup_users(self):
        """Create superuser and test accounts"""
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='suadmin').exists():
            superuser = User.objects.create_superuser(
                username='suadmin',
                email='admin@admin.com',
                password='superadmin123!'
            )
            superuser.role = 'admin'
            superuser.save()
            self.stdout.write(f"Created superuser: {superuser.username}")
        
        # Create a test admin user
        if not User.objects.filter(username='testadmin').exists():
            admin_user = User.objects.create_user(
                username='admin', 
                password='adminpass04!',
                is_staff=True
            )
            admin_user.role = 'admin'
            admin_user.save()
            self.stdout.write(f"Created admin user: {admin_user.username}")
        
        # Create a regular test user
        if not User.objects.filter(username='user3adi').exists():
            regular_user = User.objects.create_user(
                username='user3adi',
                password='userpass123!'
            )
            regular_user.role = 'user'
            regular_user.save()
            self.stdout.write(f"Created test user: {regular_user.username}")