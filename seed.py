
from faker import Faker
import random
from django.db.models import Sum
from shop.models import Department, Student, StudentID ,Subject,SubjectMarks # Adjust import path if necessary

fake = Faker()       
def create_subject_marks(num_students):
    try:
        student_objs = Student.objects.all()
        for student in student_objs[:num_students]:
            subjects = Subject.objects.all()
            for subject in subjects:
                # Check if the record already exists
                if not SubjectMarks.objects.filter(student=student, subject=subject).exists():
                    SubjectMarks.objects.create(
                        subject=subject,
                        student=student,
                        marks=random.randint(0, 100)
                    )
    except Exception as e:
        print(f"Error occurred: {e}")

# Call the function
create_subject_marks(50)   


def seed_db(n=10) -> None:
    try:
        for i in range(n):
            departments_objs = Department.objects.all()
            
            # Ensure there are departments to choose from
            if not departments_objs.exists():
                print("No departments found! Add some departments first.")
                return

            random_index = random.randint(0, len(departments_objs) - 1)  # Ensure valid index
            department = departments_objs[random_index]
            student_id = f"STU-0{random.randint(100, 999)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            # Create StudentID object
            student_id_obj = StudentID.objects.create(student_id=student_id)

            # Create Student object
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )

            print(f"Created Student: {student_obj.student_name}, ID: {student_obj.student_id}")
    except Exception as e:
        print(f"Error occurred: {e}")

