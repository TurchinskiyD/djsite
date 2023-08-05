from django.contrib import admin
from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'content')
    list_editable = ('is_published',)
    list_filter = ('time_create', 'is_published')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )



admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
