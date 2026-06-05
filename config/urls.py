from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('branches/', include('branches.urls')),
    path('students/', include('students.urls')),
    path('groups/', include('groups.urls')),
    path('lessons/', include('lessons.urls')),
]