from django.db import models
from django.utils import timezone

# =========================
# USER PROFILE
# =========================
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('supervisor', 'Supervisor'),
        ('accounts_officer', 'Accounts Officer'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    last_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


# =========================
# AUDIT LOG
# =========================
class AuditLog(models.Model):
    username = models.CharField(max_length=150)
    password_check = models.BooleanField(default=False)
    face_match = models.BooleanField(default=False)
    liveness = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} | {self.timestamp}"


# =========================
# BUDGET
# =========================
class Budget(models.Model):
    name = models.CharField(max_length=200)
    total_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} - KES {self.total_amount}"


# =========================
# EXPENSE
# =========================
class Expense(models.Model):
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    description = models.TextField()
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - KES {self.amount}"


# =========================
# TRANSACTION
# =========================
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    created_by = models.ForeignKey(
        'portal.UserProfile',   # ✅ FIXED (string reference)
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.FloatField()
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.created_by.username} - {self.amount} KES - {self.status}"


# =========================
# FACE IMAGE (BIOMETRIC)
# =========================
class FaceImage(models.Model):
    user = models.ForeignKey(
        'portal.UserProfile',   # ✅ FIXED
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='faces/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} face"