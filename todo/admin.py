from django.contrib import admin
from .models import todos
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
admin.site.register(todos, MemberAdmin)
