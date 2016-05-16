from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from accounts.models import UserProfile

class Recruiter(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = PhoneNumberField()
	date_of_birth = models.DateField()
	location = models.CharField(max_length=100)
	image = models.ImageField(upload_to='recruiter/%Y/%m/%d')
	thumb = models.ImageField(upload_to='recruiter/%Y/%m/%d', blank=True)

	def __str__(self):
		return self.user.email

	def save(self, *args, **kwargs):
		from recruit.utils import generate_thumbnail
		self.thumb = generate_thumbnail(self.image)
		super(Recruiter, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		from recruit.utils import delete_from_s3
		delete_from_s3([self.image, self.thumb])
		super(Recruiter, self).delete(*args, **kwargs)

def update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.filter(user=instance.user).update(user_type='Recruiter')