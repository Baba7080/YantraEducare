from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .views import CustomerRegistrationView,detail_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views. ProductDetailView.as_view(), name='product-detail'),
    path('refral_code/',views.refrence,name='refral_code'),
    path('search', views.search, name='search'),
    path('withoutcode',views.withoutcode,name='withoutcode'),
    path('gallery/',views.profile_gallery,name='gallery'),
    path('detail/<int:pk>/',detail_view.as_view(),name='detail'),  
    path('category/',views.cat_sel,name='category'),
    path('training/',views.training,name='training'),
    # path('send_mail/', views.send_mail, name='send_mail'),
    path('course_home/', views.course_home, name='course_home'),
    path('course/<slug>/', views.view_course, name='course'),
    path('become_pro/', views.become_pro, name='become_pro'),
    path('charge/' , views.charge , name="charge"),
    path('payment/',views.payment_listing,name='payment'),
#CART START
    #aboutus
    path('aboutus/',views.aboutpage,name='aboutus'),
    # 1-Add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    # 2-Show data from the database
    path('cart/',views.show_cart,name='showcart'),
    #privacy policy
    path('privacypolicy/',views.PrivacyPolicy,name='privacypolicy'),
    #Terms and condition
    path('termsandconditions/',views.TermsandConditions,name='termsandconditions'),
    # 3-Plus cart
    path('pluscart/',views.plus_cart),
    # 4-Minus cart
    path('minuscart/',views.minus_cart),
    # 5-Remove cart
    path('removecart/',views.remove_cart),
#listing 

    path('listing/',views.listing,name='listing'),

#CART END

    path('buy/', views.buy_now, name='buy-now'),
#dashbord

    path('dashbord/',views.dashbord,name='dashbord'),
#PROFILE START
    path('updation/',views.profileupdation,name='updation'),
    path('address/', views.address.as_view(), name='address'),
    path('accdetail/', views.accountdetail.as_view(), name='accdetail'),
#PROFILE END

    path('profile/', views.ProfileView, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

#AUTHENTICATION START
    # 1-Registration
    
    path('registration/', views.CustomerRegistrationView, name='customerregistration'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    #path('registration/', views.CustomerRegistrationView, name="customerregistration"),
    # 2-Login
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    # 3-Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    # 4-password change
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
        form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    # 5-password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
        form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html')
        ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'
        ,form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html')
        ,name='password_reset_complete'),



#AUTHENTICATION END

    path('referal_code/', views.referal_code,name='referalcode'),
    path('<str:ref_code>/', views.referal_code,name='referalcode')

   


   
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
