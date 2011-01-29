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

class PasswordUnique(models.Model):

    STRONG_PASS_LENGTH = 6
    
    STRENGTH_LENGTH = 1
    STRENGTH_CASE   = 2
    STRENGTH_CHARS  = 3
        
    unique = models.CharField(max_length = 1000)
    count    = models.IntegerField(default = 1)
    strength = models.ManyToManyField(Strength, editable = False)
      
    def __unicode__(self):
        return self.unique + " [" + str(self.count) + "]"
    
    #def save(self, *args, **kwargs):
        
        # If we are updating a record:
        #if self.pk is not None:
        #    super(PasswordUnique, self).save(*args, **kwargs)
        #    return
                    
    def pass_strength(self):
        # http://stackoverflow.com/questions/75057/what-is-the-best-way-to-check-the-strength-of-a-password
        conditions_met = 0
        if len(self.unique) >= self.STRONG_PASS_LENGTH:
            self.strength.add(self.STRENGTH_LENGTH)
            conditions_met += 1
        if self.unique.lower() != self.unique: 
            conditions_met += 1
            self.strength.add(self.STRENGTH_CASE)
        if len([x for x in self.unique if not x.isalnum()]) > 0: 
            conditions_met += 1
            self.strength.add(self.STRENGTH_CHARS)
        
        return conditions_met
    
class Password(models.Model):
    
     
    password = models.CharField(max_length = 1000)
    source = models.ForeignKey(Source)
    unique = models.ForeignKey(PasswordUnique)
    
        
    def __unicode__(self):
        return self.password + " from " + self.source.name
    
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
            
                    # If we are saving a record:        
            try:
                # We are checking if the password was already entered:            
                pu = PasswordUnique.objects.get(unique = self.password)
                pu.count += 1            
                pu.save()
                self.unique = pu             
                
                           
            except PasswordUnique.DoesNotExist:
                # If the password is does not yet exist we insert it:
                pu = PasswordUnique()
                pu.unique = self.password
                pu.save()
                pu.pass_strength()
                self.unique = pu

            super(Password, self).save(*args, **kwargs)
            
            
        
        # Editing passwords is currently not supported                 