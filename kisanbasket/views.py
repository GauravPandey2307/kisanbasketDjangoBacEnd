# myapp/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.http import QueryDict
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            print('Received data:', email, password)

            # Check if user already exists
            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'User already exists'}, status=400)

            # Create a new user
            user = User.objects.create_user(username=email, password=password)

            # Assuming user creation is successful
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            print('Error signing up:', e)
            return JsonResponse({'error': 'Sign up failed. Please try again.'}, status=400)
    else:
        # Return a JSON response indicating method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_csrf_token(request):
   if request.method == 'GET':
        csrf_token = get_token(request)
        
        print('CSRF Token:', csrf_token)
        return JsonResponse({'csrf_token': csrf_token})
   else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            print("data is :",email," ",password)

            if email and password:
                # Authenticate the user
                user = authenticate(username=email, password=password)

                if user is not None:
                    # Return a success response if authentication is successful
                    return JsonResponse({'message': 'Login successful'}, status=200)
                else:
                    # Return an error response if authentication fails
                    return JsonResponse({'error': 'Invalid email or password'}, status=401)
            else:
                return JsonResponse({'error': 'Email and password are required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return a JSON response indicating method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
class RegisterUser(APIView):
    def post(self, request):
        # Extract user data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Create a new user in Django
        user = User.objects.create_user(username=username, password=password)

        # Create a token for the user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@csrf_exempt
class LoginUser(APIView):
    def post(self, request):
        # Extract user data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # If authentication is successful, create a token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
