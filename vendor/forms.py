from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review': forms.Textarea(attrs={'rows': 4}),
        }
