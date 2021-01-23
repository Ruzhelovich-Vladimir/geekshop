from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.utils.timezone import now

from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() < self.activation_key_expires:
            return False
        return True


class ShopUserProfile(models.Model):

    MALE = 'M'
    FEMALE = "W"

    GENDER_CHOICES = {
        (MALE, 'M'),
        (FEMALE, 'Ж')
    }

    user = models.OneToOneField(
        ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)

    tagline = models.CharField(blank=True, max_length=255, verbose_name='тэги')

    about_me = models.CharField(
        blank=True, max_length=512, verbose_name='обо мне')

    gender = models.CharField(blank=True, max_length=1,
                              choices=GENDER_CHOICES, verbose_name='пол')
    avatar = models.URLField(
        blank=True, max_length=100, verbose_name='аватар')

    url = models.URLField(
        blank=True, max_length=100, verbose_name='адрес личной страницы в VK')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwards):
        if created:
            ShopUserProfile.objects.create(user=instance)
            # Выше тоже самое, что и
            # shop_user_profile = ShopUserProfile(user=instance)
            # shop_user_profile.save()

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
