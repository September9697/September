from django.shortcuts import render,get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

# 使用csrf_exempt装饰器来避免Django期待一个CSRF标记，
# 因为PayPal能通过POST渠道重定向用户到以下两个视图（views）
@csrf_exempt
def payment_done(request):
	order_id = request.session.get('order_id')
	order=get_object_or_404(Order,id=order_id)
	order.paid=True
	order.save()
	return render(request,'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request,'payment/canceled.html')

def payment_process(request):
	# 从当前会话中拿到order_id
	order_id = request.session.get('order_id')
	# 得到订单
	order=get_object_or_404(Order,id=order_id)
	host=request.get_host()
	paypal_dict={
		# PayPal商业账户，用来处理支付。我们使用e-mail账户，该账户定义在PAYPAL_RECEIVER_EMAIL设置那里。
		'business':settings.PAYPAL_RECEIVER_EMAIL,
		# 总价
		'amount':'%.2f' % order.get_total_cost(),
		# 正在出售的商品名，这里使用订单ID，因为一个订单中可能包含多个商品
		'item_name':'Order{}'.format(order.id),
		'invoice':str(order.id),
		# 本次支付的货币
		'currency_code': 'USD',
		# paypal发送ipn到这个url？？？
		'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
		# 支付成功后的重定向
		'return_url':'http://{}{}'.format(host,reverse('payment:done')),
		# 订单取消后的重定向
		'cancel_return':'http://{}{}'.format(host,reverse('payment:canceled')),
	}
	form=PayPalPaymentsForm(initial=paypal_dict)
	return render(request,'payment/process.html',{'order':order,'form':form})

