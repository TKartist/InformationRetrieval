from djongo import models

class Vehicle(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    price = models.IntegerField()
    image_url = models.URLField(max_length=200)
    detail_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"