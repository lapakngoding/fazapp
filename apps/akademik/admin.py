from django.contrib import admin
from .models import Teacher, Classroom

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nip', 'specialization')
    search_fields = ('full_name', 'nip')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    raw_id_fields = ('teacher',) # Supaya enak nyari gurunya kalau datanya banyak
