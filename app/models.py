from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import FieldError

# Create your models here.
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