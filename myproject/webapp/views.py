from django.shortcuts import render
from webapp.models import Employees
from webapp.serializer import employeesSerializer,RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
@api_view(['GET','POST'])
def employeeview(request):
    if request.method=='GET':
        employees=Employees.objects.all()
        serializer=employeesSerializer(employees,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer= employeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    


@api_view(['PUT','DELETE','GET'])
def employeedetailview(request,pk):
    try:
        employee=Employees.objects.get(pk=pk)
    except Employees.DoesNotExist:
        return Response( {'message':'Employee does not exist'},status=404)  
    if request.method=="DELETE":
        employee.delete()
        return Response({'message':'Employee was deleted successfully.'},status=204) 
    elif request.method=='GET':
        serializer=employeesSerializer(employee)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=employeesSerializer(employee,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class=RegisterSerializer


class LoginView(generics.GenericAPIView):

    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)   


        if user is not None:
            refresh=RefreshToken.for_user(user) 
            user_serializer=UserSerializer(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user':user_serializer.data
            })
        else:
            return Response({'detail':'Invalid Credentials'},status=401)


#Fetch employee data with token(Only login users can fetch api data)
class EmployeeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)  #  Protected
    serializer_class = employeesSerializer
    
    def get_queryset(self):
        print("Logged in user:", self.request.user)
        return Employees.objects.all()
    
# Fetch employee data without token(Anybody can access api data)
class PublicEmpList(generics.ListAPIView):
    queryset = Employees.objects.all()
    serializer_class = employeesSerializer
    permission_classes = [AllowAny]  #  Makes it PUBLIC
