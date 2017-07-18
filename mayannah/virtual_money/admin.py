from django.contrib import admin
from virtual_money.models import Transaction, TransactionHistory, Branch

admin.site.register(Transaction)
admin.site.register(TransactionHistory)
admin.site.register(Branch)
