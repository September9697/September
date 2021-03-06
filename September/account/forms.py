from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class RegisterForm(forms.Form):
	username=forms.CharField(
		label='username',
		max_length=20,
		initial='',
		widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'}),
    )
	email=forms.EmailField(
        label='email',
        max_length=50,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control sex','placeholder':'邮箱'}),
    )
	password = forms.CharField(
    	label='password',
		min_length=6,
		max_length=18,
		widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'密码'}),
		)
	confirm_password=forms.CharField(
		label='confirm',
		min_length=6,
		max_length=18,
		widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'确认密码'}),
	)

	def clean_username(self):
		username = self.cleaned_data['username']
		if ' ' in username or '@' in username:
			raise forms.ValidationError(u'昵称中不能包含空格和@字符')
		res = User.objects.filter(username=username)
		if len(res) != 0:
			raise forms.ValidationError(u'此昵称已经注册，请重新输入')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		res = User.objects.filter(email=email)
		if len(res) != 0:
			raise forms.ValidationError(u'此邮箱已经注册，请重新输入')
		return email

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		if password and confirm_password:
			if password != confirm_password:
				raise forms.ValidationError(u'两次密码输入不一致，请重新输入')

	def save(self):
		username = self.cleaned_data['username']
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']
		user = User.objects.create_user(username, email, password)
		user.save()


class UserProfileForm(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=['avatar','sex','phone','address','postal_code','city',]
		