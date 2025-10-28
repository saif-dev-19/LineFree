from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    ORG_TYPES = [
        ("Hospital", "Hospital"),
        ("Bank", "Bank"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=100)
    org_type = models.CharField(max_length=20, choices=ORG_TYPES)

    def __str__(self):
        return f"{self.name} . ({self.org_type})"



class Service(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

    class Meta:
        unique_together = ['organization', 'name']  # Prevent duplicate service names within same organization


class UserToken(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Serving", "Serving"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.name} - Token {self.token_number}"
