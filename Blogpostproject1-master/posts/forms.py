from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'overview', 'content', 'thumbnail', 'categories', 'tags', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded'}),
            'overview': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }