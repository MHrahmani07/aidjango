# blog/management/commands/import_blogs.py

import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from blog.models import BlogPost
from book.models import Book # To link related books
import os
import random # For random author if needed

class Command(BaseCommand):
    help = 'Imports blog posts from a CSV file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        full_csv_path = os.path.join(project_root, csv_file_path)

        if not os.path.exists(full_csv_path):
            raise CommandError(f'File "{full_csv_path}" does not exist.')

        self.stdout.write(self.style.SUCCESS(f'Attempting to import blog posts from: {full_csv_path}'))

        try:
            with open(full_csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                required_fields = ['title', 'content', 'author_username']
                if not all(field in reader.fieldnames for field in required_fields):
                    raise CommandError(f"CSV file must contain all required headers: {', '.join(required_fields)}")

                posts_created_count = 0
                for row in reader:
                    try:
                        title = row['title']
                        content = row['content']
                        author_username = row['author_username']
                        related_book_id = row.get('related_book_id') # Optional field

                        # Get or create author user (if needed, though typically it's an existing admin)
                        try:
                            author_user = User.objects.get(username=author_username)
                        except User.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Warning: Author user '{author_username}' not found for post '{title}'. Skipping this post."))
                            continue # Skip post if author is not found

                        # Get related book (optional)
                        related_book = None
                        if related_book_id:
                            try:
                                related_book = Book.objects.get(id=related_book_id)
                            except Book.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f"Warning: Related book with ID '{related_book_id}' not found for post '{title}'. Creating post without linked book."))
                                # Continue without setting related_book

                        # Create the blog post
                        # Using get_or_create to avoid duplicates based on title and author
                        blog_post, created = BlogPost.objects.get_or_create(
                            title=title,
                            author=author_user, # Ensure author is matched
                            defaults={
                                'content': content,
                                'related_book': related_book,
                            }
                        )
                        if created:
                            posts_created_count += 1
                            self.stdout.write(self.style.SUCCESS(f'Successfully created blog post: "{blog_post.title}"'))
                        else:
                            self.stdout.write(self.style.NOTICE(f'Blog post "{blog_post.title}" by "{blog_post.author.username}" already exists. Skipping.'))

                    except ValueError as ve:
                        self.stdout.write(self.style.ERROR(f"Error processing row for blog post '{row.get('title', 'N/A')}': {ve} - Skipping this row."))
                    except KeyError as ke:
                        self.stdout.write(self.style.ERROR(f"Missing expected column in CSV: {ke} - Skipping this row."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"An unexpected error occurred for row '{row.get('title', 'N/A')}': {e} - Skipping this row."))

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {posts_created_count} new blog posts.'))

        except FileNotFoundError:
            raise CommandError(f'File "{full_csv_path}" does not exist.')
        except Exception as e:
            raise CommandError(f'Error during import: {e}')

