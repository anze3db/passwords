from django.db import models

class Source(models.Model):
    name = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.name
    
class Password(models.Model):
    password = models.CharField(max_length = 1000)
    Source = models.ForeignKey(Source)
    def __unicode__(self):
        return self.password + " from " + self.Source.name
