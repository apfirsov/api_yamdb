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
    name = models.CharField()
    year = models.IntegerField(max_length=4)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitles',
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
