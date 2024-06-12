from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .models import Record
from django.contrib import messages
from django.views.generic import DetailView
# Create your views here.
def home(request):
    return render(request, 'crm_app/index.html')
    #return HttpResponse( 'welcome home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!You can now log in')
            
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'crm_app/register.html', {'form': form})

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'form':form}
    return render(request, 'crm_app/my-login.html',context=context)

#..Dashboard
@login_required(login_url= 'login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records':my_records}
    return render(request, 'crm_app/dashboard.html',context=context)



@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'crm_app/create-record.html', context=context)

#- Update a record
@login_required(login_url='login')
def update_record(request,pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated")
            return redirect("dashboard")
    context = {'form':form}
    return render(request, 'crm_app/update-record.html',context=context)

# - View a singular record
@login_required(login_url='login')
def singular_record(request,pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'crm_app/view-record.html', context=context)

#.. user logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out succesfully')
    return redirect("login")


# - Delete a record
@login_required(login_url='login')
def delete_record(request,pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted")
    return redirect("dashboard")