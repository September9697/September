from django.shortcuts import render,redirect,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.models import Cart,CartItem
from .tasks import order_created
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import logging
def order_create(request):
	if request.user.is_authenticated(): 
		cart=get_object_or_404(Cart,user=request.user)
		total_price=0
		items=[]
		quantity=request.session['quantity']
		for idd in request.session['items']:
			q=quantity.pop(0)
			item=get_object_or_404(CartItem,id=idd)
			items.append(item)
			item.item_quantity=q
			item.save()
			total_price+=item.item.price*int(q)


		if request.method=='POST':
			form=OrderCreateForm(request.POST)
			if form.is_valid():
				
				# 创建一个新的Order实例，先将它保存进数据库中，再保存进order变量里面
				order=form.save()
				order.userid=request.user.username
				order.save()
				for item in items:
					OrderItem.objects.create(order=order,
						product=item.item,
						price=item.item.price,
						quantity=item.item_quantity)
					item.delete()

				# 调用任务的 delay() 方法并异步地执行它。
				# 之后任务将会被添加进队列中，将会尽快被一个 worker 执行。
				order_created.delay(order.id)
				
				request.session['order_id'] = order.id # redirect to the payment
				return redirect(reverse('payment:process'))
		else:
			form=OrderCreateForm()
			return render(request,'orders/order/create.html',{'cart':cart,'form':form,"items":items,"total_price":total_price})
	else:
		return redirect(reverse('account:login'))


@login_required
def order_list(request):
	orders=Order.objects.filter(userid=request.user.username)
	return render(request,'orders/orderlist.html',{'orders':orders})

def order_detail(request,id):
	order=get_object_or_404(Order,
		id=id)
	return render(request,'orders/order/detail.html',{'order':order})

# staff_member_required装饰器检查用户请求这个页面的is_active以及is_staff字段是被设置为True			
@staff_member_required
def admin_order_detail(request,order_id):
	order=get_object_or_404(Order,id=order_id)
	return render(request,'admin/orders/order/detail.html',{'order':order})


def VerifyOrder(request,order_id):
	order=get_object_or_404(Order,id=order_id)
	order.verified=True
	order.save()
	return redirect(reverse('orders:order_list'))