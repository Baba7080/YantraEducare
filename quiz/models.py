from django.db import models
from django.contrib.auth.models import User
from app.models import Profile
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class schoo_dashbored(models.Model):
    school_admin = models.OneToOneField(User , on_delete=models.CASCADE,default='')
    School_name = models.CharField(max_length=20,default='')
    Best_edu = models.CharField(max_length=100,default='')
    Top_management =models.CharField(max_length=100,default='')
    Quality_meeting = models.CharField(max_length=8,blank=True)
    About = models.CharField(max_length=1000,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200,default='city')
    Phone_Number = models.CharField(max_length=10,null=True)
    class_pic1 = models.ImageField(default='deafault.jpeg', upload_to='school_dashborrd_pic')
    class_pic2 = models.ImageField(default='deafault.jpeg', upload_to='school_dashborrd_pic')
    class_pic3 = models.ImageField(default='deafault.jpeg', upload_to='school_dashborrd_pic')
    class_pic4 = models.ImageField(default='deafault.jpeg', upload_to='school_dashborrd_pic')
    reading_books_pic = models.ImageField(default='deafault.jpeg', upload_to='school_dashborrd_pic')
    def __str__(self):
        return f"{self.School_name } - {self.school_admin}"
    
    # 'created','city','Phone_Number','class_pic1','class_pic2','class_pic3','class_pic4'