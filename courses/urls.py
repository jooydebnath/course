from django.urls import path

from courses.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view() , name = 'home'),
    path('logout/', signout , name = 'logout'),
    path('signup/', SignupView.as_view() , name = 'signup'),
    path('login/', LoginView.as_view() , name = 'login'),
    path('course/<str:slug>', coursePage , name = 'courses'),
    path('check-out/<str:slug>', checkOut , name = 'checkout'),
    path('verify_payment/', verifyPayment , name = 'verify_payment'),
    path('my-courses/', MyCoursesList.as_view() , name = 'my-courses'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)