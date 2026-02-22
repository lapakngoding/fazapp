from django.urls import path
from .views import TeacherListView, TeacherCreateView, dashboard_akademik, ClassroomListView

app_name = 'akademik'

urlpatterns = [
    path('dashboard/', dashboard_akademik, name='dashboard_akademik'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', TeacherCreateView.as_view(), name='teacher_create'),
    path('kelas/', ClassroomListView.as_view(), name='classroom_list'),
]
