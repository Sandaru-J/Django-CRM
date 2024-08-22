from rest_framework.views import APIView
from .serializers import UserSerializer,ProductSerializer,OrderSerializer,StockSerializer,SupplierSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from .models import User,Product,Order,Stock
import jwt,datetime
from django.shortcuts import get_object_or_404
# import view
# from view import user_views

class UserControl(APIView):
    def post(self,request):
        data = request.data.copy()
        data['status'] = "Not verified"
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                        {"status": "success", 
                         "data": serializer.data,
                         "Message": "User Added Sucessfully!"})
    
    def get(self,request, id=None):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()
        
        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')
        
        if id:
            if id == 100:
                users = User.objects.filter(role='supplier')
                serializer = SupplierSerializer(users, many=True)
                return Response(serializer.data)
            else:
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
    
    def patch(self, request, email=None):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]        

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
        if requesting_user.role != 'Admin' and requesting_user.email != email:
            raise PermissionDenied('Permission denied.')

        try:
            item = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=404)

        serializer = UserSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Update success", "data": serializer.data}, status=200)
        return Response({"status": "error", "data": serializer.errors}, status=400)
        
        
    def delete(self, request, email=None):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')

        if requesting_user.role != 'Admin':
            return Response({'error': 'Permission denied'}, status=403)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=204)
    

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
            'email': user.email,
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
            'load': payload
            # 'role': user.role
        }

        return response

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
      

class ProductControl(APIView):
    def post(self,request):
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
        
        if requesting_user.role == 'Admin':
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                    {"status": "success", 
                        "data": serializer.data,
                        "Message": "Product Added Sucessfully!"})
        else:
            return Response({'error': 'Permission denied'}, status=403)      
    
    def get(self,request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    
    def patch(self, request, id=None):
        
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!dsf')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user.role != 'Admin':
            raise PermissionDenied('Permission denied.')
        else:
            try:
                item = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({"status": "error", "message": "Product not found"}, status=404)
            
            serializer = ProductSerializer(item, data=request.data, partial=True)
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
            return Response({"status": "error", "message": "Product ID is required"}, status=400)
        
        item = Product.objects.filter(id=id).first()
        if not item:
            return Response({"status": "error", "message": "Product not found"}, status=404)
        
        item.delete()
        return Response({"status": "success", "data": "Product Data Deleted"}, status=200)
    

class OrderControl(APIView):
    def changeQuantity():
        pass

    def post(self, request):

        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')
        
        if requesting_user.status != 'approved':
            return Response({'error': 'User status is not approved'}, status=403)

        email = User.objects.filter(email=payload['email']).first()
        if email is None:
            raise AuthenticationFailed('Unauthenticated!')
        
        data = request.data.copy()
        data["useremail"] = email.email
        data['status'] = "In que"
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {"status": "success", 
             "data": serializer.data,
             "Message": "Order Added Successfully!"})

    def get(self,request):
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        print(user)

        if user.role == 'Admin':
            order = Order.objects.all()
        else:
            order = Order.objects.filter(useremail = user.email)
        
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    
    def patch(self, request, id=None):
        
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user.role != 'Admin':
            raise PermissionDenied('Permission denied.')
        else:
            try:
                item = Order.objects.get(id=id)
            except Order.DoesNotExist:
                return Response({"status": "error", "message": "Order not found"}, status=404)
            
            serializer = OrderSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # if updated_order.status == 'delivered':
                #     item = get_object_or_404(Stock, id=updated_order.product_ID.id)

                #     if item.quantity >= updated_order.quantity:
                #         item.quantity -= updated_order.quantity
                #         item.save()
                #     else:
                #         return Response({"status": "error", "message": "Insufficient stock"}, status=400)
                return Response({"status": "Update success", "data": serializer.data}, status=200)
            return Response({"status": "error", "data": serializer.errors}, status=400)
    
    def delete(self, request, id=None):
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        
        if user.role != 'Admin':
            raise PermissionDenied('Permission Denied!')

        if not id:
            return Response({"status": "error", "message": "Order ID is required"}, status=400)
        
        item = Order.objects.filter(id=id).first()
        if not item:
            return Response({"status": "error", "message": "Product not found"}, status=404)
        
        item.delete()
        return Response({"status": "success", "data": "Order Deleted Success"}, status=200)
    
class StockControl(APIView):
    def post(self,request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()
        
        if requesting_user is None:
            raise AuthenticationFailed('Unauthenticated!')
        
        if requesting_user.role == 'Admin':
            data = request.data.copy()
            data['status'] = "Pending"
            serializer = StockSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                    {"status": "success", 
                        "data": serializer.data,
                        "Message": "Stock Request Added Sucessfully!"})
        else:
            return Response({'error': 'Permission denied'}, status=403)  
    
    def get(self,request):
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()

        if user.role == 'Admin':
            stock = Stock.objects.all()
        else:
            stock = Stock.objects.filter(supplier_email = user.email)
        
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)
    
    def patch(self, request, id=None):
        
        print("Headers:", request.headers)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        requesting_user = User.objects.filter(id=payload['id']).first()

        if requesting_user.role != 'supplier':
            raise PermissionDenied('Permission denied only for suppliers.')
        else:
            try:
                item = Stock.objects.get(id=id)
            except Stock.DoesNotExist:
                return Response({"status": "error", "message": "Stock not found"}, status=404)
            
            serializer = StockSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "Update success", "data": serializer.data}, status=200)
            return Response({"status": "error", "data": serializer.errors}, status=400)
        
    def delete(self, request, id=None):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Unauthenticated!')

        token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        stock = Stock.objects.filter(status='Accepted').first()

        if user.role != 'Admin':
            raise PermissionDenied('Permission Denied!')

        if not id:
            return Response({"status": "error", "message": "Stock Request ID is required"}, status=400)
        
        # if stock:
        #     raise PermissionDenied('Can not remove accepted request')

        item = Stock.objects.filter(id=id).first()
        if not item:
            return Response({"status": "error", "message": "Stock not found"}, status=404)
        
        item.delete()
        return Response({"status": "success", "data": "Stock Deleted Success"}, status=200)