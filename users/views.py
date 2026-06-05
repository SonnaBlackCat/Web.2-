from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from lessons.models import Lesson
from groups.models import Group


@login_required
def dashboard(request):
    context = {
        'total_students': Student.objects.filter(branch=request.user.branch).count() if request.user.branch else 0,
        'total_groups': Group.objects.filter(branch=request.user.branch).count() if request.user.branch else 0,
        'recent_lessons': Lesson.objects.filter(teacher=request.user).order_by('-date')[:5] if request.user.is_teacher else [],
    }
    return render(request, 'users/dashboard.html', context)