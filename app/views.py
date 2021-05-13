from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail



from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Profile, AccountDetails,videopost,Quiz,Course,CourseModule, payment_refral
from .forms import CustomerRegistrationForm, CustomerProfileform, Accountform,UserUpdateForms,ProfileUpdateForm,Categoryselection
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings

import random

import time 
import datetime as dt
from datetime import datetime, timedelta

def profile_gallery(request):
    # if request.method == 'POST':
    #     img = GalleryForm(request.POST, request.FILES)
    #     if img.is_valid():
    #         img.save()
    # 'img':img,
    # img = GalleryForm()
    man = Profile.objects.all()
    return render(request, 'app/gallery.html',{'man':man ,'active':'btn-primary' })

# def updation(request):
#     return render(request, 'app/udation.html')
# detailveiws
class detail_view(DetailView):
    model = Profile
    template_name = 'app/detail.html'

# def updation(request):
#     return render(request, 'app/udation.html')

#about us
def aboutpage(request):
    return render(request, 'app/aboutus.html')



def send_mail(request):
    all = Profile.get_all_mail()
    if request.method =="POST":
        data = Profile.get_all_mail()
        print(data)
        list_of_emails = list(data)
        print(list_of_emails)
        form = time_mail_sender(request.POST)
        if form.is_valid():
            s=form['hour']
            print("s",s)
            form.save()
            unix = int(time.time())
            
            year = form.cleaned_data.get('year')
            month = form.cleaned_data.get('month')
            date = form.cleaned_data.get('date')
            hour = form.cleaned_data.get('hour')
            minutes = form.cleaned_data.get('minutes')
            sec = form.cleaned_data.get('sec')
            tt = time_mail.objects.all().last()
            stt = dt.datetime(year,month,date,hour,minutes,sec)
            x = stt.timestamp()-unix
            print("xxxxx",x)
        try:
            print("startttttttttt")
            server = sm.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("yantraimmigration2@gmail.com","biiaxlfnfarhtrxw")
            from_ = "yantraimmigration2@gmail.comss"
            to_ = list_of_emails
            message = MIMEMultipart("alternative")
            message['subject'] = request.POST['subject']
            message['from'] = "Yantraeducare"

            # html = '''

            # <head>
            # <body>

            # here you message will be in html form
            # </body>
            # </head>

            # '''
            html = request.POST['message']
            text = MIMEText(html, "html")
            message.attach(text)
            print("sending..............wait for",x,"seconds ")
            p = time.sleep(x)
            server.sendmail(from_, to_, message.as_string())
            print("send")


        except Exception as e:
            print(e)
        print("done1")
        print("some")
    return render(request, 'app/send_mail.html',{'form':form})

#signup
def CustomerRegistrationView(request):
    profile_id = request.session.get('ref_profile')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                print('profile',recommended_by_profile)
                instance = form.save()
                register_user = User.objects.get(id=instance.id)
                register_profile = Profile.objects.get(user =register_user)
                register_profile.recommended_by = recommended_by_profile.user
                register_profile.save()
            else:
                form.save()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form': form})

def refrence(request, *args, **kwargs):
    return render(request,'app/refral_id.html',{})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('category')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')





#Home page
class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        add =    Profile.objects.all
        return render(request,'app/home.html',{'add':add,'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles})

#Product Details
class  ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
       
        return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
#CART Start
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user) 
        amount = 0.0
        shipping_amount = 40.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temporary_amount = (p.quantity * p.product.discounted_price)
                amount += temporary_amount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


@login_required
def  plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
            
        
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def  minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
            
        
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


@login_required
def  remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount =40.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
            
        
        data = {
            
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)
#CART End
        
        
def buy_now(request):
    return render(request, 'app/buynow.html')

#Customer Profile
@method_decorator(login_required, name='dispatch')
class address(View):
    # code = request.GET.get(code)
    def get(self,request):
        form = CustomerProfileform()

        return render(request,'app/address.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            usr = request.user
            usr.save()
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'congratualation! Profile Updated successfully')
        return render(request, 'app/address.html',{'form':form,'active':'btn-primary'})

#Account details
class accountdetail(View):
    # code = request.GET.get(code)
    def get(self,request):
        form = Accountform()

        return render(request,'app/account.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = Accountform(request.POST)
        if form.is_valid():
            usr = request.user
            usr.save()
            name = form.cleaned_data['name']
            Bank_Name = form.cleaned_data['Bank_Name']
            Beneficially_Name = form.cleaned_data['Benficially_Name']
            Account_No = form.cleaned_data['Account_No']
            Re_Enter_Account_No = form.cleaned_data['Re_Enter_Account_No']
            IFSC_Code = form.cleaned_data['IFSC_Code']
            Branch_Name = form.cleaned_data['Brnach_Name']
            Branch_Address = form.cleaned_data['Brnach_Address']
            UPI_ID = form.cleaned_data['UPI_ID']
            Paytm_No= form.cleaned_data['Paytm_No']
            PhonePe_No = form.cleaned_data['PhonePe_No']
            Google_Pay = form.cleaned_data['Google_Pay']

            rege = Customer(user=usr,name=name, Bank_Name=Bank_Name, Benficially_Name=Benficially_Name, Account_No=Account_No,
            Re_Enter_Account_No=Re_Enter_Account_No,  Name_of_Bank=Name_of_Bank,IFSC_Code=IFSC_Code,
            Branch_Name=Branch_Name, Branch_Address=Branch_Address, UPI_ID=UPI_ID, Paytm_No=Paytm_No,
            PhonePe_No=Phonepe_No, Google_Pay=Google_Pay) 

            rege.save()

            messages.success(request,'congratualation! Account Updated successfully')
        return render(request, 'app/account.html',{'form':form,'active':'btn-primary'})

#Address
@login_required
def ProfileView(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/profile.html', {'add':add, 'active':'btn-primary'})


@login_required
def profileupdation(request):

    if request.method =='POST':
            u_form = UserUpdateForms(request.POST,instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES , instance = request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,f'Your Account Has Been Updated')
                return redirect('updation')
    else:
        u_form = UserUpdateForms(instance=request.user)
        p_form =  ProfileUpdateForm(instance=request.user.profile)
    context = {
                'u_form' : u_form,
                'p_form': p_form
                }
    return render(request, 'app/updation.html',context)

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op, 'active':'btn-primary'})





#Mobile Details
def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data =='Redmi'or data == 'samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=7000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=7000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})





#Sign Up
'''class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratualations! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})'''


'''def CustomerRegistrationView(View):
    def post(self, request):
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserRegistrationOtp.objects.filter(user=user).last().otp:
                # messages.success(request,f'You have Registered successfully {username}, Please Login')
                return redirect('login')
            else:
                messages.error(request, f'You entered wrong OTP')
                return render(request, 'app/customerregistration.html', {'otp': otp, 'user': user})

        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # user = User.objects.get(username='username', password='password')
            user.is_active = False
            user.save()
            user_otp = random.randint(100000, 999999)
            UserRegistrationOtp.objects.create(user=user, otp=user_otp)
            mssg = f"Hello {username},\n You otp is {user_otp}\n Thanks!"

            send_mail(
                " Welcome to Yantra educare - Please verify your Email",
                mssg,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return render(request, 'app/customerregistration.html', {'otp': True, 'user': user})


        else:
            form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})'''


'''class CustomerRegistrationView(View):
    def post(self,request):
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserRegistrationOtp.objects.filter(user=user).last().otp:
                #messages.success(request,f'You have Registered successfully {username}, Please Login')
                return redirect('login')
            else:
                messages.error(request,f'You entered wrong OTP')
                return render(request,'app/customerregistration.html',{'otp':otp, 'user':user})

        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            #user = User.objects.get(username='username', password='password')
            user.is_active = False
            user.save()
            user_otp = random.randint(100000, 999999)
            UserRegistrationOtp.objects.create(user=user,otp=user_otp)
            mssg = f"Hello {username},\n You otp is {user_otp}\n Thanks!"

            send_mail(
                " Welcome to Yantra educare - Please verify your Email",
                mssg,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
            )
            return render(request,'app/customerregistration.html',{'otp':True, 'user':user})


        else:
            form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})'''





'''class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        profile_id = request.session.get('ref_code')
        print('profile_id', profile_id)
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                instance = form.save()
                registered_user = User.objects.get(id=instance.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                print(registered_profile)
                registered_profile.save()
            else:
                form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Your Account Has Been Created for {username} Please LogIn')
            return redirect('app/login.html')
        context = {'form': form, 'message':messages}
        return render(request, 'app/customerregistration.html', context)'''








@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 40.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temporary_amount = (p.quantity * p.product.discounted_price)
            amount += temporary_amount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


def referal_code(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile_id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request,'app/referal_code.html',{})

def dashbord(request):
    add = Profile.objects.all

    return render(request, 'app/dashboard.html',{'add':add,'active':'btn-primary'})

def listing(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommend_profile()
    obj = Profile.objects.all
    return render(request, 'app/list.html',{'my_recs' : my_recs,'obj':obj, 'active':'btn-primary'})
def search(request,*args, **kwargs):
    print("start")
    code = str(kwargs.get('ref_code'))
    print("code")
    print("code",code)
    try:
        print("tryyy")
        profile = Profile.objects.get(code=code)
        print("profile")
        profile("profile",profile)
        request.session['ref_profile'] = profile.id
        print("profileid")
        print("pro",profile.id)
        # return(pro)
    except:
        pass
    print("search fuv=nt start")
    if request.method =='GET':
        print("tttt")
        query = request.GET.get('search')
        profile = Profile.objects.get(code=query)
        request.session['ref_profile'] = profile.id
        print('profileId',profile.id)
        print("query",query)
        print("query",query)
        post = Profile.objects.all().filter(code=query)
        print("query------------",query)
        return render(request,'app/referal.html',{'post':post})
    else:
        return render(request,'app/home.html')




def withoutcode(request):
    return render(request, 'app/withoutcade.html')

#Privacy Policy
def PrivacyPolicy(request):
    return render(request, 'app/privacypolicy.html')


#Terms & Conditions
def TermsandConditions(request):
    return render(request, 'app/termsandconditions.html')


# @login_required
def cat_sel(request):

    if request.method =='POST':
            c_form = Categoryselection(request.POST, instance = request.user.profile)

            if c_form.is_valid():
                # usr = request.user
                # usr.save()
                # First_Name = p_form.cleaned_data['First_Name']
                # Second_Name = p_form.cleaned_data['Second_Name']
                # Category = p_form.cleaned_data['Category']
                # Phone_Number = p_form.cleaned_data['Phone_Number']
                # image = p_form.cleaned_data['image']
                # reg = Profile(First_Name=First_Name,Second_Name=Second_Name,Category=Category,Phone_Number=Phone_Number,image=image)
                # reg.save()
                c_form.save()
                messages.success(request,f'Your Account Has Been Updated')
                print("valid")
                return redirect('profile')

    else:
        c_form = Categoryselection(instance=request.user.profile)
        # p_form =  ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'app/category.html',{'c_form': c_form,})
@login_required
def training(request):
    vid = videopost.objects.all()
    print("vid type",type(vid))
    cat = request.user.profile.Category
    print('category ---', cat)
    my_vid = []
    for v in vid:
        print("videocate",v.categori)
        if v.categori == cat:
            
            print("cat matches")
            my_vid.append(v.videofile)
            print("list",my_vid)
        else:
            print("None")
    
    return render(request, 'app/training.html',{'my_vid': my_vid ,'active':'btn-primary' })



# purchasing the subscription
def course_home(request):
    s = request.user.profile.Category
    print("s",s)

    courses = Course.objects.filter(category = request.user.profile.Category)
    # if 
    # p = Course.objects.get.GET(category)
    # print("P",p)
    print("courses---",courses)
    course = Course.objects.all()
    context = {'courses': courses}
    for i in course:
        print("categori",i.category)
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        request.session['profile'] = profile.is_pro
        print("profile.is_pro",profile.is_pro)
    return render(request, 'app/course_home.html',context)

def view_course(request, slug):
    
    course = Course.objects.filter(slug =slug).first()
    course_modules = CourseModule.objects.filter(course=course)
    context = {'course':course , 'course_modules':course_modules}
    return render(request, 'app/course.html' , context)

    # course = Course.objects.filter(category = slug).first()
    # print("course",course)
    # course_modules = CourseModule.objects.filter(course = course)
    # print("course_modules",course_modules)
    # context = {'course':course , 'course_modules':course_modules}
    # return render(request , 'app/course.html',context)
def become_pro(request):
    profile = Profile.objects.filter(user = request.user).first()
    print("Profile ",profile)
    if request.method == 'POST':
        membership = request.POST.get('membership' , 'MONTHLY')
        amount = 1000
        if membership == 'YEARLY':
            amount = 11000
        stripe.api_key = 'sk_test_qu7ivgHp9WRHlHJjs2QHugIA00hKFbC5qc'
        # stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        customer = stripe.Customer.create(
            email = "abhijeetg40@gmail.com",
			name=request.user.username,
            source=request.POST['stripeToken']
			)
            
        charge = stripe.Charge.create(
			customer=customer,
			amount=amount,
			currency='inr',
			description="Membership",
		)
        print("charge")
        print(charge['amount'])
        if charge['paid'] == True:
            charr = []
            amount_ref = payment_refral.objects.filter(user = request.user).first()
            print('amount_ref',amount_ref)
            profile = Profile.objects.filter(user = request.user).first()
            # rec = Profile.objects.filter(user=recommended_by)
            rec = request.user.profile.recommended_by

            affi_profile = Profile.objects.filter(user = request.user.profile.recommended_by).first()

            print("afiillllll",affi_profile)
            print("recommended_by",rec)
            
            # recom_user = Profile.objects.filter(recommended_by = recommended_by)
            # print("recomended user ",recom_user)
            if charge['amount'] == 100000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                

                profile.save()
                amount_ref.save()
            elif charge['amount'] == 110000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_expiry_date = expiry
                profile.save()
                amount_ref.save()
            # affiliate profile income genertion
            print("charge['amount']",charge['amount'])
            amount_ref.new_payment = charge['amount']
            affilate = ((5*charge['amount'])/100)
            print("affilate------",affilate)
            after_ad = affi_profile.affiliate_income + affilate
            print("after_ad",after_ad)
            print("sab",affi_profile.affiliate_income)
            affi_profile.affiliate_income = after_ad
            print("hope done")
            affi_profile.save()
            print("saved----------")
            # login user income that has been done
      
        print("ho gya  ")

        return redirect('/charge/')
   
    return render(request, 'app/become_pro.html')

def charge(request):
    return render(request, 'app/charge.html')

def payment_listing(request):
    # us = request.user
    pro = Profile.objects.filter(user = request.user)
    affiliate = payment_refral.objects.filter(user = request.user)
    print(charging)
    
    context = {
        "pro":pro,
        'affiliate':affiliate
    }
    return render(request, "app/payment.html", context)