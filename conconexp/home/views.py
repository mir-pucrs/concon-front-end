# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, math
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SignUpForm
from scripts import insert_contract, cnn_model, msc_model, save_contract, insert_conflicts, Contract
from models import AuthUser, Contracts, Clauses, Conflicts, Classifiers
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
    paginate_by = 10.0 #this number has to be in double due to math.ceil

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        queryset = Contracts.objects.filter(added_by=user_id).order_by('reg_date')
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, self.paginate_by)

        try:
            file_contracts = paginator.page(page)
        except PageNotAnInteger:
            file_contracts = paginator.page(1)
        except EmptyPage:
            file_contracts = paginator.page(paginator.num_pages)

        context['contracts'] = file_contracts
        context['contracts_per_page'] = math.ceil(len(queryset)/self.paginate_by) #variable that stores the numberOfContractsOfTheUser division how many contacts per page

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


def delete_conflict(request, conf_id, model_name):

    # Find conflict and remove it.
    del_conflict = Conflicts.objects.get(conf_id=conf_id)
    con_id = del_conflict.con.con_id
    del_conflict.delete()

    return HttpResponseRedirect(reverse('home:contract_2', args=[con_id, model_name]))


def contract(request, con_id, model_name=[]):

    # Get contract information.
    contract = Contracts.objects.get(con_id=con_id)

    if request.method == 'POST' or model_name:
        # Deal the information receive by POST.

        # Get selected model.
        if not model_name:
            model_name = request.POST.get('select_model', '')

        # Find conflicts using the selected model.
        if model_name == "cnn":

            # Get classifier id.
            classifier_obj = Classifiers.objects.get(classifier_name='CNN Model')

            # Check if exists a previous set of annotated conflicts.
            conflicts_query = Conflicts.objects.filter(con_id=con_id, classifier=classifier_obj.pk)
            
            if conflicts_query:

                cntrct = Contract(con_id)
                cntrct.process_clauses()
                cls_obj = cntrct.clause_ranges
                clauses = cntrct.clauses

                conflicts = []

                for conflict in conflicts_query:

                    conflicts.append((conflict.conf_id, conflict.clause_id_1.clause_id, conflict.clause_id_2.clause_id, conflict.confidence))

            else:
                cls_obj, clauses, conflicts = cnn_model(con_id)
                conflicts = insert_conflicts(con_id, conflicts, classifier_obj)

        elif model_name == "msc":

            # Get classifier id.
            classifier_obj = Classifiers.objects.get(classifier_name='Rule-Based Model')

            # Check if exists a previous set of annotated conflicts.
            conflicts_query = Conflicts.objects.filter(con_id=con_id, classifier=classifier_obj.pk)
            
            if conflicts_query:

                cntrct = Contract(con_id)
                cntrct.process_clauses()
                cls_obj = cntrct.clause_ranges
                clauses = cntrct.clauses

                conflicts = []

                for conflict in conflicts_query:

                    conflicts.append((conflict.conf_id, conflict.clause_id_1.clause_id, conflict.clause_id_2.clause_id, conflict.confidence))

            else:
                cls_obj, clauses, conflicts = msc_model(con_id)
                conflicts = insert_conflicts(con_id, conflicts, classifier_obj)
    
        context = {
                    'cls_obj': cls_obj,
                    'clauses': clauses,
                    'conflicts': conflicts,
                    'selected_model': model_name,
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

        # Send to profile/contract.
        return HttpResponseRedirect(reverse('home:contract_2', args=[con_id, model_name]))
        
    return render(request, 'home/conflict.html')


#created by Catarina Nogueira 23/06/2017
