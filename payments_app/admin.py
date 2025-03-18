from django.contrib import admin

from payments_app.models import Payment, Month, PaymentStatus, PaymentMethod

admin.site.register([Payment, Month, PaymentStatus, PaymentMethod])
