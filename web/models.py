from django.db import models

class Source(models.Model):
    
    name = models.CharField(max_length = 255)
    count = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return self.name + " [" + str(self.count) + "]"
    
class Password(models.Model):
    
    STRONG_PASS_LENGTH = 6
        
    password = models.CharField(max_length = 1000, blank = True)
    Source = models.ForeignKey(Source)
        
    def __unicode__(self):
        return self.password + " from " + self.Source.name
    
    def pass_strength(self):
        # http://stackoverflow.com/questions/75057/what-is-the-best-way-to-check-the-strength-of-a-password
        conditions_met = 0
        if len(self.password) >= self.STRONG_PASS_LENGTH: 
            if self.password.lower() != self.password: conditions_met += 1
            if len([x for x in self.password if x.isdigit()]) > 0: conditions_met += 1
            if len([x for x in self.password if not x.isalnum()]) > 0: conditions_met += 1
        
        return conditions_met
    
    def save(self, *args, **kwargs):
        
        # Increment the number of passwords in the source:
        # [this could be slow for batch insert]
        self.Source.count += 1
        self.Source.save()       
        
        # Insert/increment PasswordUnique:
        pu = PasswordUnique()
        pu.password = self.password
        pu.save()
        
        super(Password, self).save(*args, **kwargs)

class PasswordUnique(models.Model):
    
    password = models.CharField(max_length = 1000)
    count    = models.IntegerField(default = 1)
    
    def __unicode__(self):
        return self.password + " [" + str(self.count) + "]"
    
    def save(self, *args, **kwargs):
        
        # If we are updating a record:
        if self.pk is not None:
            super(PasswordUnique, self).save(*args, **kwargs)
            return
        
        # If we are saving a record:        
        try:
            # We are checking if the password was already entered:
            pu = PasswordUnique.objects.get(password = self.password)
            pu.count += 1
            pu.save()
                        
        except PasswordUnique.DoesNotExist:
            # If the password is does not yet exist we insert it:
            super(PasswordUnique, self).save(*args, **kwargs)