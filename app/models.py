from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import FieldError
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.


# Create your models here.
SUBSCRIPTION = (
    ('F' , 'FREE'),
    ('M' , 'MONTHLY'),
    ('Y' , 'YEARLY'),
    )
# for profile
Catogories = (
    ('STUDENT' , 'STUDENT'),
    ('AFFILATE' , 'AFFILATE PATNERS'),
    ('TEACHER' , 'TEACHER'),
    )
# ? for courses
Catogori = (
    ('STUDENT' , 'STUDENT'),
    ('AFFILATE' , 'AFFILATE PATNERS'),
    ('TEACHER' , 'TEACHER'),
    )


DIFF_CHOICES =(
    ('easy' , 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard')
)





STATE_CHOICES = (
    ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman & Diu','Daman & Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadeep','Lakshadeep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharastra','Maharastra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
class AccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bank_Name = models.CharField(max_length=30,null=True)
    Beneficially_Name = models.CharField(max_length=50,null=True)
    Account_Number = models.CharField(max_length=30,null=True)
    Re_Enter_Account_Number = models.IntegerField(null=True)
    IFSC_Code = models.CharField(max_length=20,null=True)
    Branch_Name = models.CharField(max_length=30,null=True)
    Branch_Address = models.CharField(max_length=30,null=True)
    UPI_ID = models.EmailField(max_length=30,null=True)
    Paytm_Number = models.CharField(max_length=30,null=True)
    PhonePe_Number = models.CharField(max_length=30,null=True)
    Google_Pay_Number = models.CharField(max_length=30,null=True)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    code = models.CharField(max_length=8,blank=True)

    def __str__(self):
        return str(self.id)
    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommend_profile(self):
        qs = Profile.objects.all()
        # myrecs = [p for p in qs if p.recomended_by == self.user]
        my_recs = []
        for profile in qs:
            if profile.recomended_by == self.user:
                 my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


CATEGORY_CHOICES = (
    ("M",'Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='producting')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

#referal code
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio =models.TextField(blank=True)
    code = models.CharField(max_length=8,blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200,default='city')
    Category = models.CharField(max_length=100, null=False, default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100 , choices=SUBSCRIPTION , default='FREE')
    affiliate_income = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommend_profile(self):
        qs = Profile.objects.all()
        # myrecs = [p for p in qs if p.recomended_by == self.user]
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                 my_recs.append(profile)
        return my_recs
        for profile in qs:
            if profile.recomended_by == self.user:
                 my_recs.append(profile)
        return (my_recs,qs)

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


#Email verification otp




class videopost(models.Model):
    title = models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    categori = models.CharField(max_length=10)

    def __str__(self):
        return self.title + ": " + str(self.videofile) + ": " + self.categori

    


class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text = "duration of the quiz in minutes")
    require_score_to_pass = models.IntegerField(help_text = "required score to pass")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"


    def get_questions(self):
        return self.question_set.all()[:self.number_of_questions]


class Questions(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return str(self.text)
    
    def get_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE )
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_discription= RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='courses')
    category = models.CharField(max_length=100 , choices=Catogori , default='STUDENT')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super(Course ,  self).save(*args, **kwargs)
        # course_image = course_image.open(self.course_image.path)
    def  __str__(self):
        return self.course_name

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=100)
    course_description = RichTextField()
    video_url = models.URLField(max_length=300)
    can_view =  models.BooleanField(default=True)

class payment_refral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Total_payment = models.PositiveIntegerField(default=0)
    new_payment = models.PositiveIntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     print("started")
    #     self.Total_payment += new_payment
    #     print("new_payment",new_payment)
    #     super(payment_refral, self).save(*args, **kwargs)
    def  __str__(self):
        return f"{self.user}---{self.new_payment}----{self.Total_payment}"




