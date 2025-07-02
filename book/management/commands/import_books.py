# books/management/commands/import_books.py

import csv
from django.core.management.base import BaseCommand, CommandError
from book.models import Book
import os # Import os module to construct file paths

class Command(BaseCommand):
    help = 'Imports books from a CSV file into the database.'

    def add_arguments(self, parser):
        # Add an argument to specify the path to the CSV file
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        # Get the CSV file path from the command line arguments
        csv_file_path = options['csv_file']

        # Construct the full path to the CSV file, assuming it's in the project root
        # This makes it easier to run the command from the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_csv_path = os.path.join(project_root, csv_file_path)

        # Check if the file exists
        if not os.path.exists(full_csv_path):
            raise CommandError(f'File "{full_csv_path}" does not exist.')

        self.stdout.write(self.style.SUCCESS(f'Attempting to import data from: {full_csv_path}'))

        try:
            with open(full_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file) # Use DictReader to read rows as dictionaries
                
                # Check if all required fields are in the CSV header
                required_fields = ['name', 'publisher', 'provider', 'price', 'category']
                if not all(field in reader.fieldnames for field in required_fields):
                    raise CommandError(f"CSV file must contain all required headers: {', '.join(required_fields)}")

                books_created_count = 0
                for row in reader:
                    try:
                        # Convert price to Decimal
                        price = float(row['price'])

                        # Ensure category is one of the valid choices, default to 'other' if not
                        valid_categories = [choice[0] for choice in Book.CATEGORY_CHOICES]
                        category = row['category'].lower() # Convert to lowercase for case-insensitivity
                        if category not in valid_categories:
                            self.stdout.write(self.style.WARNING(f"Warning: Invalid category '{row['category']}' for book '{row['name']}'. Defaulting to 'other'."))
                            category = 'other'

                        # Create or get the book. Using get_or_create to avoid duplicates based on name and publisher.
                        # You might want a more robust unique identifier if names/publishers aren't unique.
                        book, created = Book.objects.get_or_create(
                            name=row['name'],
                            publisher=row['publisher'],
                            defaults={ # These fields are set only if a new object is created
                                'provider': row['provider'],
                                'price': price,
                                'category': category,
                            }
                        )
                        if created:
                            books_created_count += 1
                            self.stdout.write(self.style.SUCCESS(f'Successfully created book: "{book.name}"'))
                        else:
                            self.stdout.write(self.style.NOTICE(f'Book "{book.name}" by "{book.publisher}" already exists. Skipping.'))

                    except ValueError as ve:
                        self.stdout.write(self.style.ERROR(f"Error processing row for book '{row.get('name', 'N/A')}': {ve} - Skipping this row."))
                    except KeyError as ke:
                        self.stdout.write(self.style.ERROR(f"Missing expected column in CSV: {ke} - Skipping this row."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"An unexpected error occurred for row '{row.get('name', 'N/A')}': {e} - Skipping this row."))

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {books_created_count} new books.'))

        except FileNotFoundError:
            raise CommandError(f'File "{full_csv_path}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error during import: {e}')
