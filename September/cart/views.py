from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import Cart,CartItem
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

# 用require_POST来只响应POST请求
@require_POST
@login_required(login_url='/account/login')
def cart_add(request,product_id):
	cart=get_object_or_404(Cart,user=request.user)
	product=get_object_or_404(Product,id=product_id)
	form=CartAddProductForm(request.POST)
	if form.is_valid():
		cd=form.cleaned_data
		item=CartItem.objects.filter(cart=cart,item=product)
		if not item:
			CartItem.objects.create(cart=cart,item=product,item_quantity=cd['quantity'])
		else:
			item[0].item_quantity+=cd['quantity']
			item[0].save()
	return redirect('cart:cart_detail')

def cart_change_num(request,product_id):
	form=CartAddProductForm(request.POST)
	if form.is_valid():
		cd=form.cleaned_data
		cart=get_object_or_404(Cart,user=request.user)
		product=get_object_or_404(Product,id=product_id)
		item=get_object_or_404(CartItem,cart=cart,item=product)
		item.item_quantity=cd['quantity']
		item.save()
	return redirect('cart:cart_detail')



def cart_remove(request,product_id):
	cart=get_object_or_404(Cart,user=request.user)
	product=get_object_or_404(Product,id=product_id)
	item=get_object_or_404(CartItem,cart=cart,item=product)
	item.delete()
	return redirect('cart:cart_detail')

# 获取当前的购物车并展现它
@login_required(login_url='/account/login')
def cart_detail(request):
	cart=get_object_or_404(Cart,user=request.user)
	items=CartItem.objects.filter(cart=cart)
	cart_product_form=CartAddProductForm()
	return render(request,'cart/detail.html',{'cart':cart,'items':items,'cart_product_form':cart_product_form})


def checkout(request):
	if 'checkbox' in request.GET:
		itemlist=request.GET.getlist('checkbox')
		if not itemlist:
			redirect(reverse('cart:cart_detail'))
		else:
			if 'quantity' in request.GET and request.GET['quantity']:
				quantity=request.GET['quantity']
				request.session['quantity']=[]
				for q in quantity:
					request.session['quantity'].append(q)

				request.session['items']=[]
				for idd in itemlist:
					request.session['items'].append(idd)
				return redirect(reverse('orders:order_create'))
			else:
				redirect(reverse('cart:cart_detail'))
	return redirect(reverse('cart:cart_detail'))

	
