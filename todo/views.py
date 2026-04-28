from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import todos
# Create your views here.

@login_required
def todo(request):
    mytodos = todos.objects.all().values()
    template = loader.get_template('main.html')
    context = {
        'mytodos': mytodos,
    }
    return HttpResponse(template.render(context, request))
@login_required
def details(request, id):
    mytodos = todos.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mytodos': mytodos,
    }
    return HttpResponse(template.render(context, request))
@login_required
def add_todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get('description')
        # Create the new todo in the database
        todos.objects.create(title=title, description=description, user=request.user)
        return redirect('todo') # Redirect back to the main list
@login_required
def toggle_todo(request, id):
    todo = todos.objects.get(id=id)
    todo.completed = not todo.completed # Flips the boolean
    todo.save()
    return redirect('todo')
@login_required
def delete_todo(request, id):
    todo = todos.objects.get(id=id)
    todo.delete()
    return redirect('todo')
@login_required
def edit_todo(request, id):
    todo = todos.objects.get(id=id)
    if request.method == "POST":
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.save()
        return redirect('details', id=id) # Redirect back to the same details page
    return redirect('details', id=id)
@login_required
def home(request):
    todo = todos.objects.filter(user=request.user)
    return render(request, 'main.html', {"todo": todo})
def login_view(request):
    if request.method == 'POST':
        # Get the data from the 'name' attributes in your HTML
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        # Check if these credentials are correct
        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Make sure you have a URL named 'home'
        else:
            # If authentication fails
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'registration/login.html')

    # If it's a GET request, just show the page
    return render(request, 'registration/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Simple check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('login') # or wherever your login page is
        
        # Create the user in the database
        # Note: We use email as the username here for simplicity
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, "Account created successfully!")
        return redirect('login') 
    
    return render(request, 'registration/login.html')