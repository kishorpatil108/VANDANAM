from django import forms
from .models import LoanApplication
from .models import Subscriber

class LoanForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['name', 'mobile', 'loan_type']

    # Custom validations
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")

        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits.")

        return mobile
    


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your mail', 'required': True})
        }
