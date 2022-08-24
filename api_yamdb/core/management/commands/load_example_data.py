import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
# from polls.models import Question as Poll


Title = None
User = None
Category = None
Genre = None

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the example data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables."""

class Command(BaseCommand):
    """Provide loading example data form /static/data to DB."""

    help = "Loads example data from /static/data"

    def handle(self, *args, **options):
        if Title.objects.exists():
            self.stdout.write(self.style.ERROR(ALREDY_LOADED_ERROR_MESSAGE))
            return

        self.stdout.write(self.style.NOTICE('Start loading...'))

        files = [
            ('users.csv', User, False),
            ('category.csv', Category, True),
            ('genre.csv', Genre, True),
            ('titles.csv', Title, True),
            ('genre_title.csv', GenreTitle, True),
            ('review.csv', Review, True),
            ('comments.csv', Comments, True),
        ]

        for filename, model, bulk_load in files:
            path = os.path.join(settings.BASE_DIR, 'static', 'data', filename)

            with open(path, newline='') as csvfile:
                try:
                    reader = csv.DictReader(csvfile)

                    if bulk_load:
                        obj_list = [model(**row) for row in reader]
                        model.objects.bulk_create(objs=obj_list)
                    else:
                        for row in reader:
                            obj = model(**row)
                            obj.save()

                    self.stdout.write(self.style.NOTICE(f'{filename} done...'))

                except Exception as err:
                    raise CommandError(
                        f'Failed load {filename}, reason: {err}')

        self.stdout.write(self.style.SUCCESS('Loading done.'))
