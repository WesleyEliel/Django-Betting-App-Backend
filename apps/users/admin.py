from django.contrib import admin

# Register your models here.
from apps.users.models import User, Transaction, DepositTransaction, WithdrawTransaction, UserFinancialAccount
from commons.admin import BaseModelAdmin


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    list_filter = ('sex', 'is_active', 'is_staff')
    ordering = ('birthday', 'date_joined')


@admin.register(Transaction)
class TransactionAdmin(BaseModelAdmin):
    pass


@admin.register(DepositTransaction)
class DepositTransactionAdmin(BaseModelAdmin):
    pass


@admin.register(WithdrawTransaction)
class WithdrawTransactionAdmin(BaseModelAdmin):
    pass


@admin.register(UserFinancialAccount)
class UserFinancialAccountAdmin(BaseModelAdmin):
    pass
