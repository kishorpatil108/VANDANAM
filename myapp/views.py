from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ValidationError
from smtplib import SMTPException
from django.db import IntegrityError
from .models import LoanApplication
from django.contrib import messages
from .forms import LoanForm
from .forms import SubscriberForm
from .models import Subscriber
from .models import Contact



def index(request):
    return render(request, 'index.html')

def loan(request):
    return render(request, 'loan.html')

def about(request):
    return render(request, 'about.html')

def elements(request):
    return render(request, 'elements.html')

def blog(request):
    return render(request, 'blog.html')

def single_blog(request):
    return render(request, 'single-blog.html')

def faq(request):
    return render(request, 'faq.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        # -----------------------------
        # VALIDATION
        # -----------------------------
        if not name or not email or not subject or not message_text:
            messages.error(request, "All fields are required.")
            return redirect('contact')

        # -----------------------------
        # DUPLICATE CHECK (optional)
        # -----------------------------
        if Contact.objects.filter(email=email).exists():
            messages.error(request, "A contact request with this Email already exists!")
            return redirect('contact')

        # -----------------------------
        # SAVE TO DATABASE
        # -----------------------------
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        # -----------------------------
        # EMAIL DETAILS
        # -----------------------------
        email_subject = f"New Contact Message from {name}"
        email_message = (
            f"Contact Form Details:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Message:\n{message_text}\n\n"
            f"Check admin panel for more details."
        )

        # -----------------------------
        # SEND EMAIL
        # -----------------------------
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                ['vandanamadvisorspvtltd@gmail.com'],  # admin email
                fail_silently=False,
            )
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return render(request, "contact_success.html")

        except BadHeaderError:
            messages.error(request, "Invalid email header found.")
        except SMTPException as e:
            print("SMTP Error:", e)
            messages.error(request, "Mail server error. Please try again later.")
        except Exception as e:
            print("Unexpected error:", e)
            messages.error(request, "Something went wrong. Please try again later.")

    return render(request, "contact.html")

# def apply_loan(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         mobile = request.POST.get("mobile")
#         loan_type = request.POST.get("loan_type")

#         # Validation
#         if not mobile or len(mobile) != 10 or not mobile.isdigit():
#             messages.error(request, "Enter a valid 10-digit mobile number.")
#             return redirect("apply-loan")  # make sure 'apply-loan' exists in urls.py

#         # Duplicate check
#         if LoanApplication.objects.filter(mobile=mobile).exists():
#             messages.error(request, "This mobile number is already registered.")
#             return redirect("apply-loan")

#         # Save data
#         LoanApplication.objects.create(
#             name=name,
#             mobile=mobile,
#             loan_type=loan_type
#         )

#         messages.success(request, "Loan application submitted successfully!")
#         return redirect("apply-loan")

#     return render(request, "apply.html")


# def apply_loan(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         mobile = request.POST.get("mobile")
#         loan_type = request.POST.get("loan_type")

#         # Validation
#         if not mobile or len(mobile) != 10 or not mobile.isdigit():
#             messages.error(request, "Enter a valid 10-digit mobile number.")
#             return redirect("apply-loan")

#         # Duplicate check
#         if LoanApplication.objects.filter(mobile=mobile).exists():
#             messages.error(request, "This mobile number is already registered.")
#             return redirect("apply-loan")

#         # Save Data
#         loan = LoanApplication.objects.create(
#             name=name,
#             mobile=mobile,
#             loan_type=loan_type
#         )

#         # Send SMS Notification
#         sms_message = f"Dear {name}, your loan application for {loan_type} is received successfully!"
#         send_sms(mobile, sms_message)

#         messages.success(request, "Loan application submitted successfully!")
#         return redirect("apply-loan")

#     return render(request, "apply.html")



def apply_loan(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        loan_type = request.POST.get("loan_type")

        # Keep form data in case of error
        context = {
            "name": name,
            "mobile": mobile,
            "loan_type": loan_type
        }

        # Validate mobile number
        if len(mobile) != 10 or not mobile.isdigit():
            messages.error(request, "Please enter a valid 10-digit mobile number.")
            return render(request, "apply.html", context)

        # Validate loan type
        if not loan_type:
            messages.error(request, "Please select a loan type.")
            return render(request, "apply.html", context)

        # Try saving data
        try:
            LoanApplication.objects.create(
                name=name,
                mobile=mobile,
                loan_type=loan_type
            )
        except IntegrityError:
            messages.error(request, "This mobile number is already registered!")
            return render(request, "apply.html", context)

        # # Send SMS to admin
        # admin_mobile = "+919727721170"
        # msg = f"New Loan Application:\nName: {name}\nMobile: {mobile}\nLoan Type: {loan_type}"
        # send_sms(admin_mobile, msg)

        # Success message
        messages.success(request, "Your loan application has been submitted successfully!")

        # Clear form after success
        return render(request, "apply.html", {"name": "", "mobile": "", "loan_type": ""})

    return render(request, "apply.html", context)


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, "This email is already subscribed.")
            return redirect('subscribe')

        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect('subscribe')  # correct — redirect to same page
        else:
            messages.error(request, "Invalid email address.")
            return redirect('subscribe')

    else:
        form = SubscriberForm()

    return render(request, "base.html", {"form": form})


