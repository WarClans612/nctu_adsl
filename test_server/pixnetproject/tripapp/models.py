from django.db import models

# Create your models here.

class Result(models.Model):
    Search = models.CharField(max_length=15) 
    

    def __str__(self):
        return self.Search