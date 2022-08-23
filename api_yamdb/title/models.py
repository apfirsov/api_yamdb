from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(max_length=4)
    description = models.TextField()
    genre = models.ManyToManyField(Genres, through='GenresTitles')
    category = models.ForeignKey(Categories, related_name='titles')

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres)
    title = models.ForeignKey(Titles)

    def __str__(self):
        return f'{self.genre} {self.title}'
# Реализовать удаление всего при удалении Тайтла
