from .models import Agency, Project
from rest_framework import serializers


class ValidationMixin:
    '''
        Considering that both asset serializers will
        need to validate the Agency and Project records,
        that logic will be written here.
    '''
    def validate(self, attrs):
        agency, project = self.context.get('agency'), self.context.get('project')

        if not all((Agency.objects.filter(agency_name = agency).exists(), 
                   Project.objects.prefetch_related('associated_agency').filter(associated_agency__pk = agency, 
                                                                                project_name = project).exists())):
            return 
        return True

class AgencySerializer(serializers.ModelSerializer):
    '''
        Used to create Agency records.
        Will typecast the names, if possible of course.
    '''
    agency_name = serializers.CharField(validators = [])
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
        request_type = self.context.get('request_type')
        print(request_type)
        if Agency.objects.filter(agency_name = passed_agency_name).exists():
            if request_type == 'GET':
                return attrs
            else:
                raise serializers.ValidationError(f'Agency {passed_agency_name} already exists!')
        elif request_type == 'POST':
            return attrs
        else:
            raise serializers.ValidationError(f'Agency {passed_agency_name} doesnt exist!')
    
class ProjectSerializer(serializers.ModelSerializer):
    associated_agency = serializers.CharField(validators = [])
    project_name = serializers.CharField(validators = [])

    class Meta:
        model = Project
        fields = '__all__'
    
    def validate(self, attrs):
        '''
            Will check if an agency and the respective project
            already exist. If they do, it will raise a ValueError. 
        '''
        passed_agency_name = attrs.get('associated_agency')
        passed_project_name = attrs.get('project_name')
        request_type = self.context.get('request_type')
        print(request_type)
        if not Agency.objects.filter(agency_name = passed_agency_name).exists():
            raise serializers.ValidationError('The passed agency doesnt exist!')
        if Project.objects.filter(project_name = passed_project_name).exists():
            if request_type == 'GET':
                return attrs
            else:
                raise serializers.ValidationError('Record/s with the passed names already exist!')
        elif request_type == 'POST':
            return attrs
        else:
            raise serializers.ValidationError('Project with the passed name doesnt exist!')
    
    def save(self, **kwargs):
        
        associated_agency_record = Agency.objects.get(agency_name = self.validated_data.get('associated_agency'))
        return Project.objects.create(project_name = self.validated_data.get('project_name'),
                                      associated_agency = associated_agency_record)
        
class AssetSerializer(ValidationMixin, serializers.Serializer):
    asset = serializers.FileField()
    asset_type = serializers.ChoiceField(choices = ('video', 'image', 'voice', 'music', 'logo'))
    
    def validate(self, attrs):
        '''
                We check if the uploaded file's content type
                is correct and it matches the chosen field.
        '''
        result = super().validate(attrs)
        if not result:
            raise serializers.ValidationError('Make sure to pass correct a agency/project!')
        asset = attrs.get('asset')         
        if asset.content_type.split('/')[0] == attrs.get('asset_type'):
            return attrs
        else: 
            raise serializers.ValidationError('Make sure to pass a correct content type!')

    
class DetailedAsssetSerializer(ValidationMixin, serializers.Serializer):
    asset_type = serializers.ChoiceField(choices = ('video', 'image', 'voice', 'music', 'logo'))

    def validate(self, attrs):
        result = super().validate(attrs)
        if not result:
            raise serializers.ValidationError('Make sure to pass correct a agency/project!')
        return attrs