from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import Profile

# ----------------- LOGIN -----------------
def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'message': 'All fields are required'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'message': 'Account not activated'})
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})

    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

# ----------------- SIGNUP -----------------
def mysignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            return render(request, 'signup.html', {'message': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'signup.html', {'message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'message': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'message': 'Email already exists'})

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Create profile
        Profile.objects.create(user=user)

        # Activation link
        activation_link = request.scheme + '://' + request.get_host() + '/activate/' + str(user.id) + '/'
        email_message = EmailMessage(
            'Profila Portal Account Activation',
            f'Click the link to activate your account:\n{activation_link}',
            'S2023065020@umt.edu.pk',
            [email]
        )
        try:
            email_message.send()
        except:
            user.delete()
            return render(request, 'signup.html', {'message': 'Email could not be sent'})

        return redirect('login')

    return render(request, 'signup.html')

# ----------------- HOME -----------------
@login_required(login_url='login')
def myhome(request):
    return render(request, 'home.html', {
        'user': request.user
    })

# ----------------- PROFILE -----------------
@login_required(login_url='login')
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image'):
            user_profile.profile_picture = request.FILES.get('image')
        user_profile.bio = request.POST.get('bio', '')
        user_profile.save()

    return render(request, 'profile.html', {'profile': user_profile})

# ----------------- LOGOUT -----------------
def mylogout(request):
    logout(request)
    return redirect('login')

# ----------------- ACCOUNT ACTIVATION -----------------
def activate(request, id):
    try:
        user = User.objects.get(pk=id)
        user.is_active = True
        user.save()
        return render(request, 'activate.html', {'message': 'Your account has been activated!'})
    except User.DoesNotExist:
        return render(request, 'activate.html', {'message': 'Activation failed. User not found.'})
