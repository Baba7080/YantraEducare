from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Profile,
    AccountDetails,
    videopost,
    Quiz,
    Questions,
    Answer,
    Result,
    Course,
    CourseModule,
    payment_refral
)

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']

admin.site.register(Profile)

@admin.register(AccountDetails)
class AccountDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['id','Bank_Name','Beneficially_Name','Account_Number', 'Re_Enter_Account_Number',
    'IFSC_Code','Branch_Name','Branch_Address', 'UPI_ID','Paytm_Number', 'PhonePe_Number', 'Google_Pay_Number' ]
       
  

admin.site.register(videopost)
admin.site.register(Quiz)
admin.site.register(Result)
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionsAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answer)
admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(payment_refral)