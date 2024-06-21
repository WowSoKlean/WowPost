from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class RegisterForm(UserCreationForm):
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2024)))

    class Meta:
        model = CustomUser
        fields = ["username", "nickname", "birthdate", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name in self.Meta.fields:
            if field_name not in ['nickname', 'birthdate']:
                self.fields[field_name].required = True

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['profileImage', 'backgroundImage']
        labels = {  # Add labels dictionary for clarity
            'profileImage': 'Your profile picture',
            'backgroundImage': 'Your cover picture',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserImageForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        profile_image = cleaned_data.get('profileImage')
        background_image = cleaned_data.get('backgroundImage')
        
        # If only one image is selected, keep the previous data unchanged
        if profile_image and not background_image:
            user_image = UserImage.objects.filter(owner=self.user).first()
            cleaned_data['backgroundImage'] = user_image.backgroundImage
        elif background_image and not profile_image:
            user_image = UserImage.objects.filter(owner=self.user).first()
            cleaned_data['profileImage'] = user_image.profileImage

        return cleaned_data

class UserBioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['school', 'work', 'living_at', 'born_at']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserBioForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = self.user
        # If only one field is informed, keep the previous data unchanged
        if 'school' in cleaned_data and not cleaned_data['school']:
            cleaned_data['school'] = user.school
        if 'work' in cleaned_data and not cleaned_data['work']:
            cleaned_data['work'] = user.work
        if 'living_at' in cleaned_data and not cleaned_data['living_at']:
            cleaned_data['living_at'] = user.living_at
        if 'born_at' in cleaned_data and not cleaned_data['born_at']:
            cleaned_data['born_at'] = user.born_at

        return cleaned_data

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['image', 'text']
        
        widgets = {'text': forms.Textarea(attrs={'required': True, 'maxlength': 245})}