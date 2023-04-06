from django.db import models
from django.urls import reverse

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100) # varchar datatype
    breed = models.CharField(max_length=100) # varchar datatype
    description = models.TextField(max_length=250) # text datatype
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    # this instance method returns a url for the detail pg for each instance
    # this concept is based on "fat models skinny controllers"
    def get_absolute_url(self):
        return reverse('cats_detail', kwargs={'cat_id': self.id})
    

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'toy_id': self.id})
    
class Feeding(models.Model):
    MEALS = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    )
    date = models.DateField('feeding date')
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}" 
    # NOTE: when a field has choices kwarg, can use get_<fieldname>_display()
    # method to display the single char value, so Breakfast instead of B 
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/0

    # Meta: specify metadata about the model, is a class attr of the Model class in Django, part of the framework 
    # change the default sort
    class Meta: 
        ordering ='-date',

    def fed_for_today(self):
        # When a FK field is defined in a model, Django creates a reverse relation on the other side of the relationship. 
        # it means that the Cat model has a related name of feeding_set, it gives access to all the Feeding objects related to a specific Cat instance using the feeding_set attr
        return self.feeding_set.filter(date=date.today().count()>= len(MEALS))