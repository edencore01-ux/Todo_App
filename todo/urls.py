from django.urls import path
from . import views

urlpatterns = [
    path('', home),
    path('todo/', views.todo, name='todo'),
    path('todo/details/<int:id>', views.details, name='details'),
    path('todo/add/', views.add_todo, name="add_todo"),
    path('todo/toggle/<int:id>', views.toggle_todo, name='toggle_todo'),
    path('todo/delete/<int:id>', views.delete_todo, name='delete_todo'),
    path('todo/edit/<int:id>', views.edit_todo, name='edit_todo'),
    

]