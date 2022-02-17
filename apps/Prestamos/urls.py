from django.urls import path, re_path
from apps.Prestamos import views as pres

urlpatterns = [
    path('', pres.index, name='home'),

    re_path(r'^borrower/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', pres.borrorwerView.as_view(),name='borrower'),
    re_path(r'^lender/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', pres.lenderView.as_view(),name='lender'),

    # Matches any html file
    re_path(r'^.*\.*', pres.pages, name='pages'),
]
