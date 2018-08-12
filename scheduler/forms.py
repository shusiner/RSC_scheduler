from django import forms
from .models import Guard, User, Site
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django.contrib.auth.models import Permission


class NewGuardForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'placeholder': 'Tan Ah Gao'}
        ),
        max_length=200,
        help_text='e.g. Tan Ah Gao'
    )
    

    class Meta:
        model = Guard
        fields = ['name', 'age', 'position']

class GuardCreateForm(UserCreationForm):

    name = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'placeholder': 'Tan Ah Gao'}
        ),
        max_length=200,
        help_text='e.g. Tan Ah Gao'
    )

    date_of_birth = forms.DateField(
        help_text='e.g. 2018-8-11'
    )

    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        help_text='Choose a site'
    )


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_guard = True
        user.save()
        guard = Guard.objects.create(
            user=user, 
            name=self.cleaned_data.get('name'), 
            site=self.cleaned_data.get('site'),
            date_of_birth=self.cleaned_data.get('date_of_birth')
        )   

        #guard.site.add(*self.cleaned_data.get('site'))
        
        permission = Permission.objects.get(name='Guard View')     
        user.user_permissions.add(permission)
        user.save()
        #guard.interests.add(*self.cleaned_data.get('interests'))
        #guard.name.add(*self.cleaned_data.get('name'))
        return user

class SiteCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1, 'placeholder': 'Tan Ah Gao'}
        ),
        max_length=200,
        help_text='e.g. Tan Ah Gao'
    )
    

    class Meta:
        model = Site
        fields = ['name']
