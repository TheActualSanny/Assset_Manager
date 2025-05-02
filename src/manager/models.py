from django.db import models

class Agency(models.Model):
    '''
        This will simply store the agencies. The associated projects will
        be stored in a seperate table.
    '''
    agency_name = models.CharField(max_length = 50, null = False,
                                  blank = False, primary_key = True)
    def __str__(self):
        '''
            Used in response messages.
        '''
        return self.agency_name
    
class Project(models.Model):
    '''
        Stores projects and their
        relations with the agencies. The assets themselves
        will be stored seperately, in Minio.
    '''
    
    project_name = models.CharField(max_length = 70, null = False,
                                    blank = False, primary_key = True)
    associated_agency = models.ForeignKey(Agency, on_delete = models.CASCADE)