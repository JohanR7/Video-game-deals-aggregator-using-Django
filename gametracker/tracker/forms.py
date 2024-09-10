from django import forms

class GameForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Game Name Black Myth: Wukong',
            'class': 'form-control', 
        })
    )
