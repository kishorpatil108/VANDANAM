from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('loan/', views.loan, name='Loan'),
    path('about/', views.about, name='about'),
    path("apply-loan/", views.apply_loan, name="apply-loan"),
    path('elements/', views.elements, name='elements'),
    path('blog/', views.blog, name='blog'),
    path('single-blog/', views.single_blog, name='single-blog'),
    path('faq/', views.faq, name='FAQ'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscriber, name='subscribe'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
