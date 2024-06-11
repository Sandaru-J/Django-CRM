from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from .models import Product
import jwt

class ProductControl(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user_role = payload.get('role')
        if user_role != 'Admin':
            raise AuthenticationFailed('Unauthorized User')
        
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self,request,id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user_role = payload.get('role')
        if user_role != 'Admin':
            raise AuthenticationFailed('Unauthorized User')
        
        if id:
            product = Product.objects.filter(id=id).first()
            if not product:
                return Response({'error': 'Product not found'}, status=404)
            else:
                serializer = ProductSerializer(product)
        else:            
            products = Product.objects.all()
            serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    def patch(self,request,id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user_role = payload.get('role')
        if user_role != 'Admin':
            raise AuthenticationFailed('Unauthorized User')
        
        try:
            product = Product.objects.filter(id=id).first()
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        serializer = ProductSerializer(product,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Update success", "data": serializer.data}, status=200)
        return Response({"status": "error", "data": serializer.errors}, status=400)

    def delete(self,request,id=None):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user_role = payload.get('role')
        if user_role != 'Admin':
            raise AuthenticationFailed('Unauthorized User')
        
        if id:
            product = Product.objects.filter(id=id).first()
            if not product:
                return Response({'error': 'Product not found'}, status=404)
        
        product.delete()
        return Response({"status": "success", "data": "User Data Deleted"}, status=200)
