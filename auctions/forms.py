from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout

from .models import Listing, Bid

class BidForm(forms.Form):

    listing = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control", "style":"width:6rem"}))
    offerent = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden", }))

class ListingForm(forms.ModelForm):  
   
    class Meta:
        model = Listing
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        # https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
        self.helper.layout = Layout(
            "name", 
            "description", 
            "price",
            "image",
            "category",
            Field("seller", type="hidden"),
            Field("active", type="hidden"),
            Field('date', type="hidden"),
            Submit('submit', 'Submit', css_class='btn btn-primary btn-lg float-end'),
        )
        
        # https://stackoverflow.com/questions/19076965/how-to-put-a-value-from-request-get-as-a-hidden-input-in-django-crispy-forms/19077186#19077186