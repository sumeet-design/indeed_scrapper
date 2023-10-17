from django.contrib import admin

# Register your models here.
from myscrapper.models import Job
@admin.register(Job)
class StudentDetailsAdmin(admin.ModelAdmin):
    search_fields = ("title" , "company","salary","location")
    list_display = ("id","title" , "company","salary","location","date","href")
    list_filter = ("company" , "salary","location")
