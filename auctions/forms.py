from django import forms
from .models import Listings, Bids, Comments

class Create_listing(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ["name", "description", "starting_price", "img", "amount"]
        
        widgets = {
            "name" : forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder":"Name of the Product",
                }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder":"Describe your product here...",
                "rows": 4
                }),
            "starting_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g 9999.99"
                }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g 9999,99"
            })
        }
        
class Form(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ["bid_amount"]
        widgets = {
            "bid_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your bid."
            })
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write yor comment...",
                "rows": 3
            })
        }