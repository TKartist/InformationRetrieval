from django.core.management.base import BaseCommand
from .models import Vehicle
import json


class Command(BaseCommand):
    help = "Load data from JSON file into MongoDB"

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        json_file_path = "../classic_cars/JSONS/jsonDB.json"

        # Open and load JSON data
        with open(json_file_path, "r") as json_file:
            json_data = json.load(json_file)

            # Loop through each JSON item and save it to the MongoDB collection
            for item in json_data:
                vehicle = Vehicle(
                    docno=item["docno"],
                    brand=item["brand"],
                    model=item["model"],
                    price=item["price"],
                    year=item["year"],
                    text=item["year"],
                    image_url=item["image_url"],
                    detail_url=item["detail_url"],
                )
                vehicle.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data from JSON file to MongoDB")
        )
