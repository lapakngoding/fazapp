from django import forms
from .models import Banner, Post, Category
from django_ckeditor_5.widgets import CKEditor5Widget

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'description', 'image', 'url', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menambahkan class form-control secara manual ke field yang bukan CKEditor
        # agar tampilan tetap seragam dengan SB Admin 2
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        
        self.fields["content"].required = False

    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'content', 'is_published']
        widgets = {
            "content": CKEditor5Widget(config_name="default"),
        }
