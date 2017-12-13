from django.db import models
from django.contrib.auth.models import User
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import RegexValidator


class UserProfile(models.Model):
	SEX_CHOICES=(
		('M','man'),
		('W','woman'),
	)
	user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='profile')
	avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/default.png', 
                                 verbose_name='头像',
                                 #图片将处理成85x85的尺寸
                                 processors=[ResizeToFill(85,85)],)
	sex=models.CharField(max_length=1,choices=SEX_CHOICES)
	address=models.CharField(max_length=250)
	postal_code=models.CharField(max_length=20)
	city=models.CharField(max_length=100)
	phone=models.CharField(max_length=11,
							validators=[RegexValidator(regex=r'^\d{11}$',message='Phone number must be 11 digits.',code='invalid phone number')])


	def __str__(self):
		return self.user.username
