from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    score_percent = models.FloatField()
    passed = models.BooleanField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Quiz {self.score_percent}% ({'Passed' if self.passed else 'Failed'})"


class SimulationResult(models.Model):
    SIMULATOR_CHOICES = [
        ('crane', 'Crane'),
        ('forklift', 'Forklift'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulation_results')
    simulator_type = models.CharField(max_length=20, choices=SIMULATOR_CHOICES)
    time_taken_seconds = models.FloatField()
    score = models.FloatField()
    passed = models.BooleanField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.simulator_type} ({'Passed' if self.passed else 'Failed'})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

