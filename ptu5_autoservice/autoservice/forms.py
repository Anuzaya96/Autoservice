from django.contrib.auth import get_user_model
from django import forms 
from . models import OrderReview 

class OrderReviewForm(forms.ModelForm):
    class Meta():
        model = OrderReview
        fields = ('notes', 'user', 'order') 
        widgets = { 
            'user': forms.HiddenInput(),
            'order': forms.HiddenInput(),
        }


