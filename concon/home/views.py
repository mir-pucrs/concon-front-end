# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse    # HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SignUpForm
from scripts import insert_contract, get_conflicts
from models import AuthUser, Contracts, Clauses
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


class IndexView(TemplateView):

    template_name = "home/index.html"


def conflict(request):

    if request.method == 'POST' and request.FILES['up_file']:
        # Save file to a defined path.
        up_file = request.FILES['up_file']
        fs = FileSystemStorage()
        filename = fs.save(up_file.name, up_file)

        # Get info to insert contract into table.
        uploaded_file_url = fs.url(filename)
        user_id = request.user.id
        user_obj = AuthUser.objects.get(id=user_id).pk
        path = settings.BASE_DIR + uploaded_file_url

        # Insert into table.
        con_id = insert_contract(path, user_obj)

        # Create new view.
        clauses = get_conflicts(con_id)

        context = {
            'uploaded_file_url': uploaded_file_url,
            'clauses': clauses
        }

        return render(request, 'home/conflict.html', context)

    return render(request, 'home/conflict.html')


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
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
        queryset = Contracts.objects.filter(added_by=user_id)

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_contracts = paginator.page(page)
        except PageNotAnInteger:
            file_contracts = paginator.page(1)
        except EmptyPage:
            file_contracts = paginator.page(paginator.num_pages)

        context['contracts'] = file_contracts

        return context


def delete_contract(request, contract_name):

    # Delete clauses from contract.
    get_id = Contracts.objects.get(con_name=contract_name)
    # del_clauses.delete()

    contract_id = get_id.con_id

    del_clauses = Clauses.objects.filter(con=contract_id)
    del_clauses.delete()

    # Delete contract.
    del_contract = Contracts.objects.get(con_id=contract_id)
    del_contract.delete()

    render(request, 'home/profile.html', {})

# def profile(request):
#
#     # Get user id.
#     user_id = request.user.id
#
#     # Get user contracts.
#     contracts = Contracts.objects.filter(added_by=user_id)
#
#     # Define context.
#     context = {'contracts': contracts}
#
#     return render(request, 'home/profile.html', context)
