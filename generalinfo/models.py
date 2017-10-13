from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=40)
    accepting = models.BooleanField(default=True)
    active = models.BooleanField(default=False)

    def getContext(self):
    	return {
    		"accepting":self.accepting
    	}

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
