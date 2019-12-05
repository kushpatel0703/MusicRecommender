from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length = 200)
    mbid = models.CharField(max_length = 200)
    image = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length = 200)
    mbid = models.CharField(max_length = 200)
    image = models.CharField(max_length = 200)
    primary_artist = models.ForeignKey(Artist, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class ArtistTag(models.Model):
    art = models.ForeignKey(Artist, on_delete = models.CASCADE)
    tag = models.CharField(max_length = 200)

    def __str__(self):
        return self.art.name

class AlbumTag(models.Model):
    al = models.ForeignKey(Album, on_delete = models.CASCADE)
    tag = models.CharField(max_length = 200)

    def __str__(self):
        return self.al.name
