
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Student, SubjectMarks
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum


 
def get_student(request):
    # Fetch all student objects
    queryset = Student.objects.all()
    

    # Handle search functionality
    search = request.GET.get('search', '') 
    if search:
        queryset = queryset.filter(student_name__icontains=search)

    # Add the 'STU-' prefix to each student_id
    for student in queryset:
        student.formatted_student_id = f"STU-07{student.student_id}"

    # Implement pagination
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with paginated students
    return render(request, 'student.html', {'page_obj': page_obj, 'search_query': search})



def see_marks(request, student_id):
    # Fetch the student object based on student_id
    student = get_object_or_404(Student, student_id=student_id)
    
    # Get SubjectMarks for the student
    queryset = SubjectMarks.objects.filter(student=student)
    
    # Calculate total marks using Sum
    total_marks = queryset.aggregate(total_marks=Sum('marks'))['total_marks']
    
    # Get all students' total marks and order by the total marks
    rank = Student.objects.annotate(total_marks=Sum('studentmarks__marks')).order_by('-total_marks', '-student_id')
    
    # Calculate rank for the current student by comparing total marks
    current_rank = -1
    i = 1
    for s in rank:
        if s.student_id == student.student_id:
            current_rank = i
            break
        i += 1
    
    # Pass the queryset, total_marks, and rank to the template
    return render(request, 'see_marks.html', {
        'queryset': queryset,
        'total_marks': total_marks,
        'rank': current_rank
    })

