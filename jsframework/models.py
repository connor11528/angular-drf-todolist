from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title