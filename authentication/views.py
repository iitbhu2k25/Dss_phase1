from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Login attempt - Username: {username}, Password length: {len(password)}")
        
        # Hardcoded credentials check
        if username == 'admin' and password == 'password123':
            print("Credentials matched!")
            # Create or get a user object for session auth
            try:
                user = User.objects.get(username='admin')
            except User.DoesNotExist:
                # Create user if it doesn't exist
                user = User.objects.create_user(
                    username='admin',
                    password='password123',
                    is_staff=True,
                    is_superuser=True
                )
            
            # Log the user in
            login(request, user)
            
            # Get the next URL parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            # If no next parameter, redirect to confident by default
            return redirect('/confident/')
        else:
            print(f"Credentials did not match. Expected 'admin'/'password123', got '{username}'/[hidden]")
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'authentication/login.html')