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

    # Optional: extra validation
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email


# from django import forms
# from .models import Contact

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['message', 'name', 'email', 'subject']

#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if len(name) < 3:
#             raise forms.ValidationError("Name must be at least 3 characters.")
#         return name