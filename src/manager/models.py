from django.db import models

class Agency(models.Model):
    '''
        This will simply store the agencies. The associated projects will
        be stored in a seperate table.
    '''
    model_name = models.CharField(max_length = 50, null = False,
                                  blank = False, primary_key = True)
    
class Project(models.Model):
    '''
        Stores projects and their
        relations with the agencies. The assets themselves
        will be stored seperately, in Minio.
    '''
    
    project_name = models.CharField(max_length = 70, null = False,
                                    blank = False, primary_key = True)
    associated_agency = models.ForeignKey(Agency, on_delete = models.CASCADE)