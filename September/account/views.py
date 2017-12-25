from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required  
from django.views.generic.edit import FormView
from .forms import RegisterForm,UserProfileForm
from cart.models import Cart
from .models import UserProfile

@login_required
def profile_view(request):
	return render(request,'profile.html',{'user':request.user})


def user_login(request):
	if request.method=='GET':
		return render(request,'login.html')

	username=request.POST.get('username','')
	password=request.POST.get('password','')
	user=authenticate(request,username=username,password=password)
	if user is not None:
		login(request,user)
		return redirect(reverse('shop:product_list'))
	else:
		error='用户不存在或者密码错误！'
		return render(request,'login.html',{
			'username':username,
			'password':password,
			'error':error
			})


@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('shop:product_list'))


class RegisterView(FormView):
	template_name='register.html'
	form_class=RegisterForm
	success_url='/account/profile/'

	def form_valid(self,form):
		# 新用户存入数据库
		form.save()
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username,password=password)
		Cart.objects.create(user=user)
		# 登录用户
		login(self.request,user)
		UserProfile.objects.create(user=user)
		return super(RegisterView,self).form_valid(form)


def ChangeProfile(request):
	if request.method=='POST':
		form=UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect(reverse('account:profile_view'))
	else:
		form=UserProfileForm(instance=request.user.profile)
	return render(request,'changeprofile.html',{'form':form})

