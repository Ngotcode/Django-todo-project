from django.contrib import admin
from .models import Todo

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)        #to show as viewable in django Admin database

#admin.site.register(Todo)
admin.site.register(Todo, TodoAdmin)