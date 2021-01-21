import uuid

from django.db import models


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=50, unique=False)
    model = models.CharField(max_length=50, unique=False)
    year = models.PositiveIntegerField(null=False, blank=False)
    img = models.BinaryField(blank=False)
    price = models.FloatField(null=False, blank=False)
    color = models.CharField(max_length=50, unique=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.brand} {self.model}"

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "color": self.color,
            "capacity": self.capacity,
            "img": self.img
        }

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "car"
