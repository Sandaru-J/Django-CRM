from rest_framework.views import APIView
from serializers import UserSerializer
from rest_framework.response import Response
from models import User


# def add_user(data):
#     serializer = UserSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return {"status": "success", "data": serializer.data, "Message": "User Added Successfully!"}
class UserControl(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                        {"status": "success", 
                         "data": serializer.data,
                         "Message": "User Added Sucessfully!"})
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)

        return Response(serializer.data)