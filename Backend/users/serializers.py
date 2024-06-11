from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','role','email','password','address','contact_number','type_of_business','delivery_address','company_name','location','supply_capacity']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def create(self,validate_data):
        password = validate_data.pop('password',None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance