from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    favorite_food_set = models.ManyToManyField(
        to='app_food.Food',
        through='app_user.UserFavoriteFood',
        related_name='favorited_user_set'
    )



class Profile(models.Model):
    address = models.TextField(default='')
    phone = models.CharField(max_length=15,default='')
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    

class UserFavoriteFood(models.Model):
    LEVELS=[
        (1,'Like'),
        (2,'Love'),
        (3,'Insane')
    ]
    level = models.IntegerField(choices=LEVELS, default=1)
    user = models.ForeignKey(
        'app_user.CustomUser',
        on_delete=models.CASCADE,
        related_name='favorite_food_pivot_set'
    )
    food = models.ForeignKey(
        'app_food.Food',
        on_delete=models.CASCADE,
        related_name='favorited_food_pivot_set'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','food'],
                name='unique_user_food'
            )
        ]


    def level_label(self):
        selected_level = [l for l in self.LEVELS if l[0]==self.level][0]
        return selected_level[1]
