from django.contrib.auth.models import AbstractUser
from django.db import models

class Society(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    registration_number = models.CharField(max_length=50, unique=True)
    total_flats = models.IntegerField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    established_date = models.DateField()
    logo = models.ImageField(upload_to='society/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Societies"

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='owner')
    phone = models.CharField(max_length=15, blank=True)
    flat_number = models.CharField(max_length=10, blank=True)
    wing = models.CharField(max_length=5, blank=True)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

    @property
    def full_address(self):
        return f"Flat {self.flat_number}, Wing {self.wing}" if self.flat_number and self.wing else "Address not set"