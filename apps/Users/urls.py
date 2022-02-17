from django.urls import path
from .views import login_view, register_user_lander,register_user_borrower,logout_view

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/lender/', register_user_lander, name="registerLender"),
    path('register/borrower/', register_user_borrower, name="registerBorrower"),
    path('logout/', logout_view, name='logout')  ,
]
