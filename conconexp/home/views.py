# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, math
from forms import SignUpForm
from models import ConflictTypes
from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, ListView
from create_conflicts import ConflictCreator, remove_norm
from django.http import HttpResponse, HttpResponseRedirect
from scripts import insert_conflicts, Contract, embedding_model
from models import AuthUser, Contracts, Clauses, Conflicts, Classifiers
from scripts import insert_contract, cnn_model, msc_model, save_contract
from django.http import JsonResponse

BACKUP_FOLDER = os.path.join(settings.BASE_DIR, 'media/backup_contracts')
CONF_TYPES = {
    'simple': 1,
    'context': 2,
    'conditional': 3
}


class IndexView(TemplateView):

    template_name = "home/index.html"


def submit_conf(request):

    # Insert new conflict from user.

    if request.is_ajax():

        try:
            # Get info sent via ajax.
            con_id = request.GET.get('con_id', None)
            clause_id_1 = request.GET.get('clause_id_1', None)
            clause_id_2 = request.GET.get('clause_id_2', None)
            added_by = request.GET.get('added_by', None)
            confidence = request.GET.get('confidence', None)

            # Get the objects from each element.
            con_id = Contracts.objects.get(con_id=con_id)
            clause_id_1 = Clauses.objects.get(clause_id=int(clause_id_1))
            clause_id_2 = Clauses.objects.get(clause_id=int(clause_id_2))
            added_by = AuthUser.objects.get(id=int(added_by))

            # Add conflict to database.
            ins = Conflicts(con=con_id, clause_id_1=clause_id_1,
                clause_id_2=clause_id_2, added_by=added_by,
                confidence=int(confidence))

            ins.save()

            return JsonResponse({'done': True})
        except:
            return JsonResponse({'done': False})
        
    else:
        return JsonResponse({'done': False})



def delete_conf(request):

    if request.is_ajax():

        conf_id = request.GET.get('conf_id', None)
        
        # Delete conflict.
        try:
            Conflicts.objects.filter(conf_id=conf_id).delete()
            done = True
        except:
            return HttpResponse("This route only handles AJAX requests")

        data = {
            'done': done
        }

        return JsonResponse(data)


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/concon')
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
        queryset = Contracts.objects.filter(added_by=user_id).order_by(
            'reg_date')
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, self.paginate_by)

        try:
            file_contracts = paginator.page(page)
        except PageNotAnInteger:
            file_contracts = paginator.page(1)
        except EmptyPage:
            file_contracts = paginator.page(paginator.num_pages)

        context['contracts'] = file_contracts
        # Variable that stores the numberOfContractsOfTheUser division
        # how many contacts per page
        context['contracts_per_page'] = math.ceil(len(queryset
        )/self.paginate_by)


        return context


def delete_contract(request, con_id):

    # Find the path to reach the contract.
    del_contract = Contracts.objects.get(con_id=con_id)
    contract_path = del_contract.path_to_file
    filename = os.path.basename(contract_path)

    # Move the contract to a backup folder.
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
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

    return HttpResponseRedirect(reverse('home:contract_2', args=[con_id,
     model_name]))


def contract(request, con_id, model_name=[]):

    # Get contract information.
    contract = Contracts.objects.get(con_id=con_id)
    contract_name = contract.con_name

    if request.method == 'POST' or model_name:
        # Deal the information receive by POST.

        # Get selected model.
        if not model_name:
            model_name = request.POST.get('select_model', '')

        # Find conflicts using the selected model.
        if model_name == "cnn":

            # Get classifier id.
            classifier_obj = Classifiers.objects.get(
                classifier_name='CNN Model')

            # Check if exists a previous set of annotated conflicts.
            conflicts_query = Conflicts.objects.filter(con_id=con_id,
                classifier=classifier_obj.pk)
            
            if conflicts_query:

                cntrct = Contract(con_id)
                cntrct.process_clauses()
                cls_obj = cntrct.clause_ranges
                clauses = cntrct.clauses

                conflicts = []

                for conflict in conflicts_query:

                    conflicts.append((conflict.conf_id,
                        conflict.clause_id_1.clause_id,
                        conflict.clause_id_2.clause_id, conflict.confidence))

            else:
                cls_obj, clauses, conflicts = cnn_model(con_id)
                conflicts = insert_conflicts(con_id, conflicts,
                    classifier_obj)

        elif model_name == "msc":

            # Get classifier id.
            classifier_obj = Classifiers.objects.get(
                classifier_name='Rule-Based Model')

            # Check if exists a previous set of annotated conflicts.
            conflicts_query = Conflicts.objects.filter(con_id=con_id,
                classifier=classifier_obj.pk)
            
            if conflicts_query:

                cntrct = Contract(con_id)
                cntrct.process_clauses()
                cls_obj = cntrct.clause_ranges
                clauses = cntrct.clauses

                conflicts = []

                for conflict in conflicts_query:

                    conflicts.append((conflict.conf_id,
                        conflict.clause_id_1.clause_id,
                        conflict.clause_id_2.clause_id, conflict.confidence))

            else:
                cls_obj, clauses, conflicts = msc_model(con_id)
                conflicts = insert_conflicts(con_id, conflicts,
                    classifier_obj)
    
        elif model_name == "emb":

            # Get classifier id.
            classifier_obj = Classifiers.objects.get(
                classifier_name='Embedding Model')

            # Check if exists a previous set of annotated conflicts.
            conflicts_query = Conflicts.objects.filter(con_id=con_id,
                classifier=classifier_obj.pk)

            print "Conflicts_query", conflicts_query

            if conflicts_query:

                cntrct = Contract(con_id)
                cntrct.process_clauses()
                cls_obj = cntrct.clause_ranges
                clauses = cntrct.clauses

                conflicts = []

                for conflict in conflicts_query:

                    conflicts.append((conflict.conf_id,
                        conflict.clause_id_1.clause_id,
                        conflict.clause_id_2.clause_id, conflict.confidence))

            else:
                cls_obj, clauses, conflicts = embedding_model(con_id)
                conflicts = insert_conflicts(con_id, conflicts,
                    classifier_obj)

        conflicts.sort(key=lambda conf: conf[3], reverse=True)

        conf_type_elems = get_conf_types()

        context = {
                    'con_name': contract_name,
                    'cls_obj': cls_obj,
                    'clauses': clauses,
                    'conflicts': conflicts,
                    'selected_model': model_name,
                    'conf_types': conf_type_elems,
                    }

        # Return context.
        return render(request, 'home/contract.html', context)

    context = {'contract': contract, 'con_name': contract_name}    

    # Return context.
    return render(request, 'home/contract.html', context)


def get_user_obj(request):
    # Get info to insert contract into table.
    user_id = request.user.id
    return AuthUser.objects.get(id=user_id).pk


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
        user_obj = get_user_obj(request)
        path = settings.BASE_DIR + string

        # Insert into table.
        con_id = insert_contract(path, user_obj)

        # Send to profile/contract.
        return HttpResponseRedirect(reverse('home:contract_2', args=[con_id,
            model_name]))
        
    return render(request, 'home/conflict.html')


def get_conf_types():

    conf_type_query = ConflictTypes.objects.all()
    conf_type_elems = dict()
    for conf_type in conf_type_query:
        conf_type_name = conf_type.type
        conf_type_name = conf_type_name.replace('_', ' ')
        conf_type_name = conf_type_name[0].upper() + conf_type_name[1:]
        conf_type_elems[conf_type.type_id] = conf_type_name

    return conf_type_elems


def new_conflicts(request):

    context = dict()

    if request.method == 'POST':

        conf_type_elems = get_conf_types()

        if request.POST.get('sel_norm') or request.POST.get('chng_cntrct'):
            # Process a contract and select a norm.
       	    cc = ConflictCreator()
            cc.select_contract()
            cc.get_norms()
            norm_id = cc.get_a_norm()
            norm = cc.norms[norm_id]
            context = {'norm': norm, 'con_id':cc.contract_id,
                'norm_id':norm_id, 'con_name':cc.contract_name,
                'conf_types': conf_type_elems}
            
        elif request.POST.get('sel_n_norm') or request.POST.get('not_a_norm'):
            # Select a new norm from the same contract, if possible.
            ids = request.POST.get('norm_text', '').split('_')
            con_id, norm_id = int(ids[0]), int(ids[1])
            cc = ConflictCreator()
            if request.POST.get('not_a_norm'):
                remove_norm(norm_id)
            cc.get_contract(con_id)
            cc.get_norms()
            norm_id = cc.get_a_norm(norm_id=norm_id)
            norm = cc.norms[norm_id]
            context = {'norm': norm, 'con_id':con_id, 'norm_id':norm_id,
                'con_name':cc.contract_name,
                'conf_types': conf_type_elems}

        elif request.POST.get('sub_conf'):
            # Submit the new norm.
            new_norm = request.POST.get('new_norm')    # Get text.
            ids = request.POST.get('norm_text', '').split('_')
            conf_type = int(request.POST.get('select_type', ''))
            con_id, norm_id = int(ids[0]), int(ids[1])
            cc = ConflictCreator()
            cc.set_user_id(request.user.id)
            cc.get_contract(con_id)
            cc.get_norms()
            # Add conflict.
            # First write the new norm on the existing contract.
            new_norm_id = cc.save_new_norm(new_norm)
            # Then save the new conflict to database.
            cc.save_conflict(norm_id, new_norm_id, conf_type)
            # Build context.
            norm_id = cc.get_a_norm(norm_id=norm_id)
            norm = cc.norms[norm_id]
            context = {'norm': norm, 'con_id':con_id, 'norm_id':norm_id,
                'con_name':cc.contract_name,
                'conf_types': conf_type_elems}

        elif request.POST.get('finish'):
            # Save all conflicts and leave.
            context = {'thanks': True}

    return render(request, 'home/new_conflicts.html', context)


def export_contract(request):

    if request.method == 'POST':

        # Get text.
        con_id = request.POST.get('con_id')
        text = export.get_text(con_id)

        # Annotate text.
        export.annotate()

        # Generate the link to download.

    pass