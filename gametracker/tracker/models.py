from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    steam_appid = models.IntegerField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
