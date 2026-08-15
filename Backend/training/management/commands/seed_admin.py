from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from training.models import Profile


class Command(BaseCommand):
    help = 'Seeds an initial admin user with username "admin" and password "admin".'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('admin')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            # Profile is automatically created by signal
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = 'admin'
            profile.save()
            self.stdout.write(self.style.SUCCESS('Successfully created admin user ("admin" / "admin").'))
        else:
            updated = False
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                updated = True
            profile, _ = Profile.objects.get_or_create(user=user)
            if profile.role != 'admin':
                profile.role = 'admin'
                profile.save()
                updated = True
            
            if updated:
                self.stdout.write(self.style.SUCCESS('Admin user already exists. Updated staff status and admin role.'))
            else:
                self.stdout.write(self.style.WARNING('Admin user "admin" already exists.'))
