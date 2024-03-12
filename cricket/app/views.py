from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from . models import Customer,Cart,Product,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
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
	user = request.user
	product = request.GET.get('prod_id')
	product_title = Product.objects.get(id=product)
	Cart(user=user, product=product_title).save()
	messages.success(request, 'Product Added to Cart Successfully !!' )
	return redirect('/cart')

def show_cart(request):
	if request.user.is_authenticated:
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount})
		else:
			return render(request, 'app/emptycart.html')
	else:
		return render(request, 'app/emptycart.html')

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary',})

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


@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})

def log_out(request):
 logout(request)
 return redirect('/accounts/login/')

class ProfileView(View):
	def get(self, request):
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
		
	def post(self, request):
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    


  
