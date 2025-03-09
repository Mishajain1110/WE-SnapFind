from django import forms
from .models import Post, PostPicture
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    date_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], label='Date and Time')
    date_time.widget.attrs = {'class' : 'form-control datetimepicker-input', 'data-target' : '#datetimepicker'}

    desc = forms.CharField(
        required=False,  # Make it optional
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'style': 'resize:none;', 
            'placeholder': 'Additional details such as characteristics, etc.'
        })
    )
    
    contact1 = forms.CharField(
        required=False,  # Make it optional
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'xxx-xxx-xxxx'
        })
    )

    contact2 = forms.EmailField(
        required=False,  # Make it optional
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@example.com'
        })
    )

    class Meta:
        model = Post
        fields = ['title','desc', 'type', 'assetType', 'location','date_time', 'contact1', 'contact2']

        widgets = {
            'desc' : forms.Textarea(attrs={'class' : 'form-control', 'style' : 'resize:none;', 'placeholder' : 'Additional details such as characteristics, etc.'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Post Title'}),
            'location' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Location (e.g., bathroom, etc.)'}),
            # 'contact1' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'xxx-xxx-xxxx'}),
            # 'contact2' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'example@example.com'}),
            'type' : forms.Select(attrs={'class' : 'form-control'}),
            'assetType' : forms.Select(attrs={'class' : 'form-control'}),
        }

        labels = {
            'desc' : 'Additional Details',
            'title' : 'Post Title',
            'location' : 'Location',
            'contact1' : 'Contact Number',
            'contact2' : 'Email',
            'type' : 'Post Type',
            'assetType' : 'Asset Type',
        }

class PostPictureForm(forms.ModelForm):
    class Meta:
        model = PostPicture
        fields = ['picture']

        widgets = {
            'picture' : forms.FileInput(attrs={'class' : 'custom-file-input'})
        }
