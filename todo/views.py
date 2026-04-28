from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
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