from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import CommentForm
from shop.models import Product
from orders.models import OrderItem


def create_comment(request,item_id):
	if request.method=='POST':
		comment_form=CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment=comment_form.save(commit=False)
			new_comment.user=request.user
			orderitem=get_object_or_404(OrderItem,id=item_id)
			product=orderitem.product
			new_comment.product=product
			new_comment.save()
			orderitem.commented=True
			orderitem.save()
			return render(request,'commented.html',{'comment':new_comment})
	else:
		comment_form=CommentForm()

	return render(request,'create.html',{'comment_form':comment_form,'item_id':item_id})


