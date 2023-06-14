from django.contrib import admin

# Register your models here.
from apps.users.models import User, Transaction, DepositTransaction, WithdrawTransaction, UserFinancialAccount


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('sex', 'is_active', 'is_staff')
    ordering = ('birthday', 'date_joined')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(DepositTransaction)
class DepositTransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(WithdrawTransaction)
class WithdrawTransactionAdmin(admin.ModelAdmin):
    pass

@admin.register(UserFinancialAccount)
class UserFinancialAccountAdmin(admin.ModelAdmin):
    pass
