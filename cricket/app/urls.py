from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
#------ To incude Media file ---------------
from django.conf import settings
from django.conf.urls.static import static
#=================================================================================================
urlpatterns = [
    # path('', views.home),
    path('',views.ProductView.as_view(),name='home'),
    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:id>',views.ProductDetailView.as_view(),name="product-detail"),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),
    path('types/', views.types, name='mobile'),
    path('types/<slug:data>', views.types, name='mobiledata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout',views.log_out,name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
