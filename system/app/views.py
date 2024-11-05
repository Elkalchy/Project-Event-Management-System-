from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .models import Event
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


# Create your views here.
def login_view(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(request,username=email,password=password)

        if user:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request,'login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # التحقق من تطابق كلمتي المرور
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # التحقق من وجود اسم المستخدم مسبقًا
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # التحقق من وجود البريد الإلكتروني مسبقًا
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('signup')

        # إنشاء المستخدم وتشفير كلمة المرور
        user = User(username=username, email=email)
        user.set_password(password1)  # تشفير كلمة المرور
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'signup.html')



def logout_view(request):
    logout(request)
    return redirect("login")


def index(request):
    events = Event.objects.filter(user=request.user)

    return render(request, 'index.html', {'events': events})


def details(request,event_id):
    events = get_object_or_404(Event, id=event_id, user=request.user)


    return render(request,'event-details.html',{'events':events})




def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        location = request.POST.get('location')
        description = request.POST.get('description')

        # Create an Event instance and associate it with the logged-in user
        event = Event(title=title, date=date, location=location, description=description, user=request.user)
        event.save()

        return redirect('index')

    return render(request, 'create_event.html')


def my_event(request):
    events = Event.objects.filter(user=request.user)
    return render(request,'my-event.html',{'events':events})


def edit_event(request,event_id):
    events = get_object_or_404(Event, user=request.user, id=event_id)
    if request.method == "POST":
        events.title = request.POST.get('title')
        events.date = request.POST.get('date')
        events.location = request.POST.get('location')
        events.description = request.POST.get('description')

        events.save()

        return redirect('my-event')

    return render(request,'edit_event.html',{'events':events})

def del_event(request, event_id):
    # Retrieve the event associated with the logged-in user and the given event ID
    event = get_object_or_404(Event, user=request.user, id=event_id)
    
    
    
    event.delete()

    

    # Optionally, you can add a confirmation page or message before deletion
    return redirect('my-event')


def my_profile(request):
    user = get_object_or_404(User, pk=request.user.pk)  # Retrieves the currently logged-in user by primary key (id)
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Update the existing user's information
        user.username = username
        user.email = email
        user.save()  # Save the changes to the database

        return redirect("my_profile")  # Redirect to the profile page after saving

    return render(request, 'my_profile.html', {'user': user})


def setting(request):
    user = get_object_or_404(User, pk=request.user.pk)
    
    if request.method == "POST":
        password_ref = request.POST.get('password_ref')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')

        
        if not check_password(password_ref, user.password):
            
            return redirect('setting')

        
        if password_1 != password_2:
            
            return redirect('setting')
        
        
        user.set_password(password_1)
        user.save()
        

        return redirect('login')

    return render(request, 'setting.html')
