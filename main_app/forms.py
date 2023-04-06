from django.forms import ModelForm
from .models import Feeding

# define a new form class: FeedingForm that inherits from Django's built-in ModelForm class
class FeedingForm(ModelForm):
    # defines some metadata about the form
    class Meta:
        #  tells Django which model the form should be based on (Feeding)
        # By specifying the model attr, Django automatically generates a form based on the fields of the Feeding model 
        model = Feeding
        # & which fields from that model should be included in the form (date and meal) 
        fields = ('date', 'meal')