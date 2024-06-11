from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
import jwt,datetime

class UserControl(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()
        
        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')
        
        if id:
            user = User.objects.filter(id=id).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)
            if requesting_user.role != 'Admin' and requesting_user.id != user.id:
                return Response({'error': 'Permission denied'}, status=403)
            serializer = UserSerializer(user)
        else:
            if requesting_user.role == 'Admin':
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
            else:
                serializer = UserSerializer(requesting_user)
        
        return Response(serializer.data)
    
    def patch(self, request, id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')

        # Non-admin users should only update their own data
        if requesting_user.role != 'Admin' and requesting_user.id != id:
            raise PermissionDenied('Permission denied.')

        try:
            item = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=404)
        
        serializer = UserSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Update success", "data": serializer.data}, status=200)
        return Response({"status": "error", "data": serializer.errors}, status=400)
        
    def delete(self, request, id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        admin_user = User.objects.filter(id=payload['id']).first()
        
        if admin_user.role != 'Admin':
            raise PermissionDenied('Permission Denied!')

        if not id:
            return Response({"status": "error", "message": "User ID is required"}, status=400)
        
        item = User.objects.filter(id=id).first()
        if not item:
            return Response({"status": "error", "message": "User not found"}, status=404)
        
        item.delete()
        return Response({"status": "success", "data": "User Data Deleted"}, status=200)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorect Password!')
        
        payload = {
            'id':user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'role':user.role
        }

        token = jwt.encode(payload,'secret', algorithm='HS256')

        response =  Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Success',
            'jwt':token,
            # 'role': user.role
        }

        return response
    
class UserView(APIView):
    def get(self, request, id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        if id:
            user = User.objects.filter(id=id).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)
            serializer = UserSerializer(user)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response