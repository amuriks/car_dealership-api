import uuid
from car.models import Car
from user_profile.models import UserProfile
from django.db import models


class Order(models.Model):
    def set_total_price(self):
        return self.car.price * self.number

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='car')
    number = models.PositiveIntegerField(null=False, blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveIntegerField(default=set_total_price, null=False, blank=False)

    def to_dict(self):
        return {
            "id": self.id,
            "car": self.car.to_dict(),
            "number": self.number,
            "total_price": self.total_price
        }

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "order"
