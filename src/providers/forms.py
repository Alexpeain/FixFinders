from django import forms
from .models import ProviderProfile, Category

class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = [
            'business_name', 
            'category', 
            'township', 
            'phone_number', 
            'description',
            'verification_photo_pink_card',
            'verification_photo_smart_card'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make verification photos required only if status is not approved
        if self.instance and self.instance.verification_status == 'approved':
            self.fields['verification_photo_pink_card'].required = False
            self.fields['verification_photo_smart_card'].required = False
        else:
            self.fields['verification_photo_pink_card'].required = True
            self.fields['verification_photo_smart_card'].required = True

class ProviderUpdateForm(forms.ModelForm):
    """Form for existing providers to update basic info without re-uploading documents."""
    class Meta:
        model = ProviderProfile
        fields = ['business_name', 'category', 'township', 'phone_number', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
