

from pickle import NONE
from urllib import request
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, QueryDict
from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib import messages
from apps.Users.models import User, LenderProfile, BorrowerProfile
from django.db.models import Sum

from .forms import PrestamosForm
from .models import Prestamos
from .utils import set_pagination_borrower, set_pagination_lender, set_pagination_prestamos, set_pagination


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    if request.user.is_lander:
        lender = "/lender/"
        return redirect(lender)
    else:
        return redirect("/borrower/")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


class borrorwerView(View):
    context = {'segment': 'prestamos'}

    def get(self, request, pk=None, action=None):

        context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context,)

    def list(self, request):

        prestamos = Prestamos.objects.filter(borrowerProfile_id=request.user.borrowerprofile.id)
        
        total_price = sum(prestamos.values_list('amount_lent', flat=True))

        self.context['total_price'] = total_price

        self.context['prestamos'], self.context['info'] = set_pagination(
            request, prestamos)
        if not self.context['prestamos']:
            return False, self.context['info']

        self.context['form'] = PrestamosForm()

        return self.context, 'prestamos/borrower/list.html'


class lenderView(View):

    context = {'segment': 'prestamos'}
    msg = None

    def get(self, request, pk=None, action=None):

        context, template = self.list(request, self.msg)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context,)


    def post(self, request, pk=None, action=None):

        msg = self.update_instance(request, pk)
        if msg == None:
            return redirect('lender')

        else:
            context, template = self.list(request , msg)
            
            return render(request, template, context,)
            
            
    def list(self, request,msg):


        form = PrestamosForm()
        cursor = connection.cursor()

        queryset = ' SELECT  USER.first_name as first_name , USER.last_name as last_name,'\
                    '        need_money_for as need_money_for,                                    '\
                    '        LOWER(borrower.description) as description,                                    '\
                    '        borrower.amount_need as amount_need,                                           '\
                    '        (                                                                              '\
                    '            SELECT Sum(amount_lent)                                                    '\
                    '              FROM prestamos_prestamos pp                                              '\
                    '             WHERE pp.lenderprofile_id = pres.lenderProfile_id AND                     '\
                    '                   pp.borrowerprofile_id = pres.borrowerProfile_id                     '\
                    '        )                                                                              '\
                    '        AS totalRaised,                                                                '\
                    '        sum(pres.amount_lent)                                                          '\
                    '   FROM prestamos_prestamos AS pres                                                    '\
                    '        LEFT JOIN                                                                      '\
                    '        users_borrowerProfile AS borrower ON pres.borrowerProfile_id = borrower.id     '\
                    '        LEFT JOIN                                                                      '\
                    '        users_user AS USER ON borrower.user_id = USER.id                               '\
                    '  WHERE pres.lenderProfile_id = %s                                                     '\
                    '  GROUP BY first_name , last_name,need_money_for, description,amount_need,totalRaised;                              '\
        
        cursor.execute(queryset,[request.user.lenderprofile.id])
        prestamos_total = cursor.fetchall()

        borrowers = BorrowerProfile.objects.all()

        prestamos = Prestamos.objects.filter(lenderProfile_id=request.user.lenderprofile.id)

        prestamos_total_sum = Prestamos.objects.all().values('borrowerProfile_id',).order_by('borrowerProfile_id').annotate(amount_lent=Sum('amount_lent'))

        total_price = sum(prestamos.values_list('amount_lent', flat=True))

        val_total_disponble_lander = LenderProfile.objects.filter(user=request.user).values_list('money', flat=True)

        val_total_prestamos_saldo = int(val_total_disponble_lander[0]) - int(total_price)

        self.context['form'] = form
        self.context['msg'] = msg
                
        self.context['val_total_prestamos_saldo'] = val_total_prestamos_saldo
        
        self.context['borrowersPres'] = prestamos_total
        self.context['prestamos_total_sum'] = prestamos_total_sum

        self.context['borrowers'] = borrowers

        return self.context, 'prestamos/lender/list.html'

    def update_instance(self, request, pk, is_urlencode=False):

        form = PrestamosForm(request.POST)
        if form.is_valid():

            amount_lent =int(form.amount()) 
            
            prestamos = Prestamos.objects.filter(lenderProfile_id=request.user.lenderprofile.id)

            total_price = sum(prestamos.values_list('amount_lent', flat=True))

            val_total_disponble_lander = LenderProfile.objects.filter(user=request.user).values_list('money', flat=True)

            val_total_prestamos_saldo = int(val_total_disponble_lander[0]) - int(total_price)

            val_valido = val_total_prestamos_saldo - amount_lent
            
            if val_valido > 0:
                self.msg = None
                form.save(request, pk)
            else:
                self.msg = 'Saldo en la cuenta es insuficiente'
        
        
        else:
            self.msg = 'Valores no valido'
        return self.msg 