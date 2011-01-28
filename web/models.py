from django.db import models

class Source(models.Model):
    
    name = models.CharField(max_length = 255)
    count = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return self.name + " [" + str(self.count) + "]"
    
    # Updates the count value:
    def update_count(self):
        
        c = Password.objects.all().filter(source = self.pk).count()        
        self.count = c
       
        
class Strength(models.Model):
    
    name  = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    count = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return self.name + " [" + str(self.count) + "]"
    
class Password(models.Model):
    
    STRONG_PASS_LENGTH = 6
    
    STRENGTH_UNIQUE = 1
    STRENGTH_LENGTH = 2
    STRENGTH_CASE   = 3
    STRENGTH_CHARS  = 4
        
    password = models.CharField(max_length = 1000)
    source = models.ForeignKey(Source)
    strength = models.ManyToManyField(Strength, editable = False)
        
    def __unicode__(self):
        return self.password + " from " + self.source.name
    
    def pass_strength(self):
        # http://stackoverflow.com/questions/75057/what-is-the-best-way-to-check-the-strength-of-a-password
        conditions_met = 0
        if len(self.password) >= self.STRONG_PASS_LENGTH:
            self.strength.add(self.STRENGTH_LENGTH)
            conditions_met += 1
        if self.password.lower() != self.password: 
            conditions_met += 1
            self.strength.add(self.STRENGTH_CASE)
        if len([x for x in self.password if not x.isalnum()]) > 0: 
            conditions_met += 1
            self.strength.add(self.STRENGTH_CHARS)
        
        pu = PasswordUnique.objects.get(password = self.password)
        if pu.count == 1:
            conditions_met += 1
            self.strength.add(self.STRENGTH_UNIQUE)
        
        return conditions_met
    
    def save(self, *args, **kwargs):
        
        if self.pk is None:        
            # Increment the number of passwords in the source:
            # [this could be slow for batch insert]
            
            if 'batch' not in kwargs.keys():
                
                self.source.count += 1
                self.source.save()  
            else:
                del kwargs['batch']        
                
            # Insert/increment PasswordUnique:
            pu = PasswordUnique()
            pu.password = self.password
            pu.save()

            # Insert password strengths:
            
        
            super(Password, self).save(*args, **kwargs)
            self.pass_strength()
        
        # Editing passwords is currently not supported

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
                 