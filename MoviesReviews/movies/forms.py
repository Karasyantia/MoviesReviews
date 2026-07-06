from django import forms
from django.core.exceptions import ValidationError
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 10:
            raise ValidationError("Текст отзыва должен содержать хотя бы 10 символов.")
        return text