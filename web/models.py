from django.db import models

class Source(models.Model):
    name = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.name
    
class Password(models.Model):
    
    STRONG_PASS_LENGTH = 6
        
    password = models.CharField(max_length = 1000, blank = True)
    Source = models.ForeignKey(Source)
        
    def __unicode__(self):
        return self.password + " from " + self.Source.name
    
    def pass_strength(self):
        # Matic: I should probably put this method elsewhere?
        # Smotko: Yea, this method should be part of the model ;)
        # http://stackoverflow.com/questions/75057/what-is-the-best-way-to-check-the-strength-of-a-password
        conditions_met = 0
        if len(self.password) >= self.STRONG_PASS_LENGTH: 
            if self.password.lower() != self.password: conditions_met += 1
            if len([x for x in self.password if x.isdigit()]) > 0: conditions_met += 1
            if len([x for x in self.password if not x.isalnum()]) > 0: conditions_met += 1
        
        return conditions_met
