from django.db import models


from apps.Users.models import BorrowerProfile,LenderProfile


# Create your models here.

class Prestamos(models.Model):
    borrowerProfile = models.ForeignKey(BorrowerProfile, on_delete=models.CASCADE)
    lenderProfile = models.ForeignKey(LenderProfile, on_delete=models.CASCADE)
    amount_lent = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        verbose_name = 'prestamo'
        verbose_name_plural = 'prestamos'

