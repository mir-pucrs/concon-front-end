# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SignUpForm
from scripts import insert_contract, cnn_model, msc_model, save_contract
from models import AuthUser, Contracts, Clauses
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse

BACKUP_FOLDER = os.path.join(settings.BASE_DIR, 'media/backup_contracts')


class IndexView(TemplateView):

    template_name = "home/index.html"


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/conconexp')
    else:
        form = SignUpForm()
    return render(request, 'home/register.html', {'form': form})


class ProfileView(ListView):

    model = Contracts
    template_name = 'home/profile.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        queryset = Contracts.objects.filter(added_by=user_id).order_by('reg_date')

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        print paginator.count, paginator.num_pages, paginator.page_range

        try:
            file_contracts = paginator.page(page)
        except PageNotAnInteger:
            file_contracts = paginator.page(1)
        except EmptyPage:
            file_contracts = paginator.page(paginator.num_pages)

        context['contracts'] = file_contracts

        return context


def delete_contract(request, con_id):

    # Find the path to reach the contract.
    del_contract = Contracts.objects.get(con_id=con_id)
    contract_path = del_contract.path_to_file
    filename = os.path.basename(contract_path)

    # Move the contract to a backup folder.
    os.rename(contract_path, os.path.join(BACKUP_FOLDER, filename))

    # Delete clauses from contract.
    del_clauses = Clauses.objects.filter(con=con_id)
    del_clauses.delete()

    # Delete contract.
    del_contract.delete()

    return HttpResponseRedirect(reverse('home:profile'))

def contract(request, con_id):

    # Get contract information.
    contract = Contracts.objects.get(con_id=con_id)

    if request.method == 'POST':
        # Deal the information receive by POST.

        # Get selected model.
        model_name = request.POST.get('select_model', '')

        # Find conflicts using the selected model.
        if model_name == "cnn":
            cls_obj, clauses, conflicts = cnn_model(con_id)
        elif model_name == "msc":
            cls_obj, clauses, conflicts = msc_model(con_id)
    
        context = {
                    'cls_obj': cls_obj,
                    'clauses': clauses,
                    'conflicts': conflicts
                  }

        # Return context.
        return render(request, 'home/contract.html', context)

    context = {'contract': contract}    

    # Return context.
    return render(request, 'home/contract.html', context)


def conflict(request):

    if request.method == 'POST' and request.FILES['up_file']:

        # Get selected model.
        model_name = request.POST.get('select_model', '')

        # Save file to a defined path.
        up_file = request.FILES['up_file']
        code, string = save_contract(up_file, request.user.id)

        if code == 'ERROR' or code == 'WARNING':

            context = {
                'message': string
            }
            return render(request, 'home/conflict.html', context)

        # Get info to insert contract into table.
        user_id = request.user.id
        user_obj = AuthUser.objects.get(id=user_id).pk
        path = settings.BASE_DIR + string

        # Insert into table.
        con_id = insert_contract(path, user_obj)

        # Create new view.
        if model_name == "cnn":
            sel, clauses, conflicts = cnn_model(con_id)
        elif model_name == "msc":
            sel, clauses, conflicts = msc_model(con_id)

        context = {
            'cls_obj': sel,
            'clauses': clauses,
            'conflicts': conflicts,
        }

        return render(request, 'home/conflict.html', context)

    return render(request, 'home/conflict.html')
