from django.contrib import admin
from .models import UserProfile, Transaction, Budget, Expense, AuditLog
from .models import UserProfile, FaceImage

admin.site.register(FaceImage)

admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(AuditLog)