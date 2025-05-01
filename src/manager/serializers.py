from .models import Agency, Project
from rest_framework import serializers

class AgencySerializer(serializers.ModelSerializer):
    '''
        Used to create Agency records.
        Will typecast the names, if possible of course.
    '''
    class Meta:
        model = Agency
        fields = '__all__'

    def validate(self, attrs):
        '''
            If possible, this will typecast a different class object
            into a valid string, so that we can save it into the table
            directly.
        '''

        passed_agency_name = attrs.get('agency_name')
            
        if Agency.objects.filter(agency_name = passed_agency_name).exists():
            raise ValueError(f'Agency {passed_agency_name} already exists!')
        
        return attrs
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
    
    def validate(self, attrs):
        '''
            Will check if an agency and the respective project
            already exist. If they do, it will raise a ValueError. 
        '''
        passed_agency_name = attrs.get('agency_name')
        passed_project_name = attrs.get('project_name')
                            
        if any((Agency.objects.filter(agency_name = passed_agency_name).exists(),
               Project.objects.filter(project_name = passed_project_name).exists())):
            raise ValueError('Record/s with the passed names already exist!')

        return attrs
        