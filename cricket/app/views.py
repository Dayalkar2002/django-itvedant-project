from django.shortcuts import render,redirect
from django.views import View
from . models import Customer,Cart,Product,OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
  kashmir_willow=Product.objects.filter(category='KW')
  english_willow=Product.objects.filter(category='EW')
  return render(request,'app/home.html',{'kashmirwillow':kashmir_willow,'englishwillow':english_willow})
 
 
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
 
class ProductDetailView(View):
  def get(self,request,id):
   product=Product.objects.get(pk=id)
   return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')


def types(request, data=None):
 if data==None:
  types=Product.objects.all()
 elif data=='English':
  types=Product.objects.filter(category='EW') 
 elif data=='Kashmir':
  types=Product.objects.filter(category='KW')
 elif data=='below':
  types=Product.objects.all().filter(discounted_price__lt=20000) 
 elif data=='above':
  types=Product.objects.all().filter(discounted_price__gt=20000) 
 return render(request, 'app/types.html',{'types':types})


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Succesfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')

def log_out(request):
 logout(request)
 return redirect('/accounts/login/')