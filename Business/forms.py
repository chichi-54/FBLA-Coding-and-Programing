from django.db.models.base import Model
from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Business, Review, BusinessImage


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'image', 'description', 'email', 'phone_number', 'address', 'website']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }
        widgets ={
            'businessImage'
        }

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_rating', 'review_message']

        labels = {
            'review_rating': 'Place your vote',
            'review_message': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class BusinessImageForm(forms.ModelForm):
    class Meta:
        model = BusinessImage
        fields = ['image']

BusinessImageFormSet = inlineformset_factory(
    Business,
    BusinessImage,
    form=BusinessImageForm,
    extra=3,  # Show 3 image fields by default
    can_delete=True
)