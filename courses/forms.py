from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ListeCourses, Article

class ListeForm(forms.ModelForm):
    class Meta:
        model = ListeCourses
        fields = ['nom']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article 
        fields = ['nom', 'quantite']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'EX: Lait'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'exemple@domaine.com'}),
        label="Adresse email"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "Nom d'utilisateur"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Mot de passe"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Confirmer le mot de passe"})