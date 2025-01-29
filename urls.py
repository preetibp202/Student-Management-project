
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views
urlpatterns = [

    path('get_student/',views.get_student,name='get_student'),
    path('see_marks/<str:student_id>/', views.see_marks, name='see_marks'),
 
]


