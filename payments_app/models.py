from django.db import models

# Payment Status
class PaymentStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)  # Payment status (masalan: 'paid', 'pending')

    def __str__(self):
        return self.status


# Payment Method
class PaymentMethod(models.Model):
    method = models.CharField(max_length=20, unique=True)  # Payment method (masalan: 'cash', 'click', 'card')

    def __str__(self):
        return self.method


# Month Model
class Month(models.Model):
    name = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"


# Payment Model
class Payment(models.Model):
    student = models.ForeignKey('users_app.User', on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, default='oylik')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = PaymentStatus.objects.get(status='pending')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"To‘lov: {self.amount} - {self.status.status}"
