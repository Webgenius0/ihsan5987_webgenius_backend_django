import os
from django.core.management.base import BaseCommand
from apps.home.models import Category, Subcategory
import pandas as pd






class Command(BaseCommand):
    help = "Initial data for the app"

    def handle(self, *args, **options):
        # create categories from the categories.xlsx file
        categories_file = 'Categories.xlsx' # folter is in /apps/home/categories.xlsx
        file_path = os.path.join(os.path.dirname(__file__), categories_file)
        df = pd.read_excel(file_path)
        subcategories = df['Subcategory'].dropna().tolist()
        categories = df['Category'].dropna().tolist()

        for category in categories:
            Category.objects.get_or_create(category_name=category, is_main=True)
        for index, subcategory in enumerate(subcategories):
            category_name = categories[index]
            category = Category.objects.get(category_name=category_name)
            Subcategory.objects.get_or_create(
                category=category,
                subcategory_name=subcategory
            )
        self.stdout.write(self.style.SUCCESS('Initial category and subcategory data created successfully.'))
        