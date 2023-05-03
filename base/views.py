from calendar import monthrange
from datetime import datetime, timedelta
import random, calendar
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import userTime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def register(request):

    users = User.objects.all()
    data = userTime.objects.all()

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        middle_initial = request.POST.get('middleInitial')


        myuser = User.objects.create_user(username=username, password=password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        new_user_time = userTime(user=myuser)
        new_user_time.first_name = first_name
        new_user_time.last_name = last_name
        new_user_time.middle_initial = middle_initial
        new_user_time.username = username
        new_user_time.save()
        myuser = authenticate(username=username, password=password)

        return render(request, 'adminpanel.html', {'users':users, 'data':data})
    return render(request, 'adminpanel.html', {'users':users, 'data':data})

def deactivate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")
    
    user.is_active = False
    user.save()
    
    return redirect('adminpanel')

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    
    user.is_active = True
    user.save()
    
    return redirect('adminpanel')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_superuser:
                login(request, user)
                return redirect('saveTimes')
            else:
                login(request, user)
                return redirect('adminpanel')
        else:
            messages.error(request, "Invalid employee ID or password. Please try again.", extra_tags='login_error')
            return redirect('login')
    return render(request, 'login.html')

def searchBar(request):
    users = User.objects.filter(is_superuser=False)  # Only get non-superuser employees
    data = userTime.objects.all()

    if request.method == 'POST':
        search = request.POST.get('search')
        employees = users.filter(username__icontains=search).values('id','username', 'first_name', 'last_name', 'is_active')
        return render(request, 'adminpanel.html', {'search': search, 'employees': employees, 'users': users, 'data': data})
    else:
        search = None  # Define search as None when request.method is not 'POST'
        employees = None  # Define employees as None when request.method is not 'POST'
        return render(request, 'adminpanel.html', {'users': users, 'data': data})


def signout(request):
    logout(request)
    return redirect('login')

def change_password(request, user_id):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = get_object_or_404(User, id=user_id)

        if not user.check_password(old_password):
            messages.error(request, 'Old password does not match.', extra_tags='oldPasswordError')
            return redirect('change-password', user_id=user_id)

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.', extra_tags="newAndOldPassError")
            return redirect('change-password', user_id=user_id)

        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password has been changed.')
        return redirect('saveTimes')
    messages.error(request, 'Old password is incorrect, please check again.')
    return render(request, 'change_password.html')




def form(request):
  return render(request, 'form.html')

def home(request):
  return render(request, 'homepage.html')

def preview(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    data = get_object_or_404(userTime, user=user)
    context ["data"] = data
    if request.method == 'POST':
        month = data.month
        month_name = calendar.month_name[month]
        middle_initial = data.middle_initial
        monday_time_in_morning = data.monday_morning_time_in
        monday_time_out_morning = data.monday_morning_time_out
        monday_time_in_afternoon = data.monday_afternoon_time_in
        monday_time_out_afternoon = data.monday_afternoon_time_out

        tuesday_time_in_morning = data.tuesday_morning_time_in
        tuesday_time_out_morning = data.tuesday_morning_time_out
        tuesday_time_in_afternoon = data.tuesday_afternoon_time_in
        tuesday_time_out_afternoon = data.tuesday_afternoon_time_out

        wednesday_time_in_morning = data.wednesday_morning_time_in
        wednesday_time_out_morning = data.wednesday_morning_time_out
        wednesday_time_in_afternoon = data.wednesday_afternoon_time_in
        wednesday_time_out_afternoon = data.wednesday_afternoon_time_out

        thursday_time_in_morning = data.thursday_morning_time_in
        thursday_time_out_morning = data.thursday_morning_time_out
        thursday_time_in_afternoon = data.thursday_afternoon_time_in
        thursday_time_out_afternoon = data.thursday_afternoon_time_out

        friday_time_in_morning = data.friday_morning_time_in
        friday_time_out_morning = data.friday_morning_time_out
        friday_time_in_afternoon = data.friday_afternoon_time_in
        friday_time_out_afternoon = data.friday_afternoon_time_out

        saturday_time_in_morning = data.saturday_morning_time_in
        saturday_time_out_morning = data.saturday_morning_time_out
        saturday_time_in_afternoon = data.saturday_afternoon_time_in
        saturday_time_out_afternoon = data.saturday_afternoon_time_out

        sunday_time_in_morning = data.sunday_morning_time_in
        sunday_time_out_morning = data.sunday_morning_time_out
        sunday_time_in_afternoon = data.sunday_afternoon_time_in
        sunday_time_out_afternoon = data.sunday_afternoon_time_out

        monday_time_in_morning_undergrad_overload = data.monday_time_in_morning_overload_undergrad
        monday_time_out_morning_undergrad_overload = data.monday_time_out_morning_overload_undergrad
        monday_time_in_afternoon_undergrad_overload = data.monday_time_in_afternoon_overload_undergrad
        monday_time_out_afternoon_undergrad_overload = data.monday_time_out_afternoon_overload_undergrad

        monday_time_in_morning_grad_overload = data.monday_time_in_morning_overload_grad
        monday_time_out_morning_grad_overload = data.monday_time_out_morning_overload_grad
        monday_time_in_afternoon_grad_overload = data.monday_time_in_afternoon_overload_grad
        monday_time_out_afternoon_grad_overload = data.monday_time_out_afternoon_overload_grad

        tuesday_time_in_morning_undergrad_overload = data.tuesday_time_in_morning_overload_undergrad
        tuesday_time_out_morning_undergrad_overload = data.tuesday_time_out_morning_overload_undergrad
        tuesday_time_in_afternoon_undergrad_overload = data.tuesday_time_in_afternoon_overload_undergrad
        tuesday_time_out_afternoon_undergrad_overload = data.tuesday_time_out_afternoon_overload_undergrad

        tuesday_time_in_morning_grad_overload = data.tuesday_time_in_morning_overload_grad
        tuesday_time_out_morning_grad_overload = data.tuesday_time_out_morning_overload_grad
        tuesday_time_in_afternoon_grad_overload = data.tuesday_time_in_afternoon_overload_grad
        tuesday_time_out_afternoon_grad_overload = data.tuesday_time_out_afternoon_overload_grad

        wednesday_time_in_morning_undergrad_overload = data.wednesday_time_in_morning_overload_undergrad
        wednesday_time_out_morning_undergrad_overload = data.wednesday_time_out_morning_overload_undergrad
        wednesday_time_in_afternoon_undergrad_overload = data.wednesday_time_in_afternoon_overload_undergrad
        wednesday_time_out_afternoon_undergrad_overload = data.wednesday_time_out_afternoon_overload_undergrad

        wednesday_time_in_morning_grad_overload = data.wednesday_time_in_morning_overload_grad
        wednesday_time_out_morning_grad_overload = data.wednesday_time_out_morning_overload_grad
        wednesday_time_in_afternoon_grad_overload = data.wednesday_time_in_afternoon_overload_grad
        wednesday_time_out_afternoon_grad_overload = data.wednesday_time_out_afternoon_overload_grad

        thursday_time_in_morning_undergrad_overload = data.thursday_time_in_morning_overload_undergrad
        thursday_time_out_morning_undergrad_overload = data.thursday_time_out_morning_overload_undergrad
        thursday_time_in_afternoon_undergrad_overload = data.thursday_time_in_afternoon_overload_undergrad
        thursday_time_out_afternoon_undergrad_overload = data.thursday_time_out_afternoon_overload_undergrad

        thursday_time_in_morning_grad_overload = data.thursday_time_in_morning_overload_grad
        thursday_time_out_morning_grad_overload = data.thursday_time_out_morning_overload_grad
        thursday_time_in_afternoon_grad_overload = data.thursday_time_in_afternoon_overload_grad
        thursday_time_out_afternoon_grad_overload = data.thursday_time_out_afternoon_overload_grad

        friday_time_in_morning_undergrad_overload = data.friday_time_in_morning_overload_undergrad
        friday_time_out_morning_undergrad_overload = data.friday_time_out_morning_overload_undergrad
        friday_time_in_afternoon_undergrad_overload = data.friday_time_in_afternoon_overload_undergrad
        friday_time_out_afternoon_undergrad_overload = data.friday_time_out_afternoon_overload_undergrad

        friday_time_in_morning_grad_overload = data.friday_time_in_morning_overload_grad
        friday_time_out_morning_grad_overload = data.friday_time_out_morning_overload_grad
        friday_time_in_afternoon_grad_overload = data.friday_time_in_afternoon_overload_grad
        friday_time_out_afternoon_grad_overload = data.friday_time_out_afternoon_overload_grad

        saturday_time_in_morning_undergrad_overload = data.saturday_time_in_morning_overload_undergrad
        saturday_time_out_morning_undergrad_overload = data.saturday_time_out_morning_overload_undergrad
        saturday_time_in_afternoon_undergrad_overload = data.saturday_time_in_afternoon_overload_undergrad
        saturday_time_out_afternoon_undergrad_overload = data.saturday_time_out_afternoon_overload_undergrad

        saturday_time_in_morning_grad_overload = data.saturday_time_in_morning_overload_grad
        saturday_time_out_morning_grad_overload = data.saturday_time_out_morning_overload_grad
        saturday_time_in_afternoon_grad_overload = data.saturday_time_in_afternoon_overload_grad
        saturday_time_out_afternoon_grad_overload = data.saturday_time_out_afternoon_overload_grad
        
        sunday_time_in_morning_undergrad_overload = data.sunday_time_in_morning_overload_undergrad
        sunday_time_out_morning_undergrad_overload = data.sunday_time_out_morning_overload_undergrad
        sunday_time_in_afternoon_undergrad_overload = data.sunday_time_in_afternoon_overload_undergrad
        sunday_time_out_afternoon_undergrad_overload = data.sunday_time_out_afternoon_overload_undergrad

        sunday_time_in_morning_grad_overload = data.sunday_time_in_morning_overload_grad
        sunday_time_out_morning_grad_overload = data.sunday_time_out_morning_overload_grad
        sunday_time_in_afternoon_grad_overload = data.sunday_time_in_afternoon_overload_grad
        sunday_time_out_afternoon_grad_overload = data.sunday_time_out_afternoon_overload_grad

        times = generate_random_times(month, monday_time_in_morning, monday_time_out_morning, monday_time_in_afternoon, monday_time_out_afternoon,
                                        tuesday_time_in_morning, tuesday_time_out_morning, tuesday_time_in_afternoon, tuesday_time_out_afternoon,
                                        wednesday_time_in_morning, wednesday_time_out_morning, wednesday_time_in_afternoon, wednesday_time_out_afternoon,
                                        thursday_time_in_morning, thursday_time_out_morning, thursday_time_in_afternoon, thursday_time_out_afternoon,
                                        friday_time_in_morning, friday_time_out_morning, friday_time_in_afternoon, friday_time_out_afternoon,
                                        saturday_time_in_morning, saturday_time_out_morning, saturday_time_in_afternoon, saturday_time_out_afternoon,
                                        sunday_time_in_morning, sunday_time_out_morning, sunday_time_in_afternoon, sunday_time_out_afternoon, 
                                        monday_time_in_morning_undergrad_overload, monday_time_out_morning_undergrad_overload, monday_time_in_afternoon_undergrad_overload, monday_time_out_afternoon_undergrad_overload,
                                        tuesday_time_in_morning_undergrad_overload, tuesday_time_out_morning_undergrad_overload, tuesday_time_in_afternoon_undergrad_overload, tuesday_time_out_afternoon_undergrad_overload,
                                        wednesday_time_in_morning_undergrad_overload, wednesday_time_out_morning_undergrad_overload, wednesday_time_in_afternoon_undergrad_overload, wednesday_time_out_afternoon_undergrad_overload,
                                        thursday_time_in_morning_undergrad_overload, thursday_time_out_morning_undergrad_overload, thursday_time_in_afternoon_undergrad_overload, thursday_time_out_afternoon_undergrad_overload,
                                        friday_time_in_morning_undergrad_overload, friday_time_out_morning_undergrad_overload, friday_time_in_afternoon_undergrad_overload, friday_time_out_afternoon_undergrad_overload,
                                        saturday_time_in_morning_undergrad_overload, saturday_time_out_morning_undergrad_overload, saturday_time_in_afternoon_undergrad_overload, saturday_time_out_afternoon_undergrad_overload,
                                        sunday_time_in_morning_undergrad_overload, sunday_time_out_morning_undergrad_overload, sunday_time_in_afternoon_undergrad_overload, sunday_time_out_afternoon_undergrad_overload,
                                        monday_time_in_morning_grad_overload, monday_time_out_morning_grad_overload, monday_time_in_afternoon_grad_overload, monday_time_out_afternoon_grad_overload,
                                        tuesday_time_in_morning_grad_overload, tuesday_time_out_morning_grad_overload, tuesday_time_in_afternoon_grad_overload, tuesday_time_out_afternoon_grad_overload,
                                        wednesday_time_in_morning_grad_overload, wednesday_time_out_morning_grad_overload, wednesday_time_in_afternoon_grad_overload, wednesday_time_out_afternoon_grad_overload,
                                        thursday_time_in_morning_grad_overload, thursday_time_out_morning_grad_overload, thursday_time_in_afternoon_grad_overload, thursday_time_out_afternoon_grad_overload,
                                        friday_time_in_morning_grad_overload, friday_time_out_morning_grad_overload, friday_time_in_afternoon_grad_overload, friday_time_out_afternoon_grad_overload,
                                        saturday_time_in_morning_grad_overload, saturday_time_out_morning_grad_overload, saturday_time_in_afternoon_grad_overload, saturday_time_out_afternoon_grad_overload,
                                        sunday_time_in_morning_grad_overload, sunday_time_out_morning_grad_overload, sunday_time_in_afternoon_grad_overload, sunday_time_out_afternoon_grad_overload)
        
        context = {
            'month_name':month_name,
            'middle_initial':middle_initial,
        }
        context["times"] = times

        return render(request, 'preview.html', context)
    #Add warning message if the inputted data is wrong.
    return render(request, 'preview.html', context)

def undergradpreview(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    data = get_object_or_404(userTime, user=user)
    context ["data"] = data
    if request.method == 'POST':
        month = data.month
        month_name = calendar.month_name[month]
        middle_initial = data.middle_initial
        monday_time_in_morning = data.monday_morning_time_in
        monday_time_out_morning = data.monday_morning_time_out
        monday_time_in_afternoon = data.monday_afternoon_time_in
        monday_time_out_afternoon = data.monday_afternoon_time_out

        tuesday_time_in_morning = data.tuesday_morning_time_in
        tuesday_time_out_morning = data.tuesday_morning_time_out
        tuesday_time_in_afternoon = data.tuesday_afternoon_time_in
        tuesday_time_out_afternoon = data.tuesday_afternoon_time_out

        wednesday_time_in_morning = data.wednesday_morning_time_in
        wednesday_time_out_morning = data.wednesday_morning_time_out
        wednesday_time_in_afternoon = data.wednesday_afternoon_time_in
        wednesday_time_out_afternoon = data.wednesday_afternoon_time_out

        thursday_time_in_morning = data.thursday_morning_time_in
        thursday_time_out_morning = data.thursday_morning_time_out
        thursday_time_in_afternoon = data.thursday_afternoon_time_in
        thursday_time_out_afternoon = data.thursday_afternoon_time_out

        friday_time_in_morning = data.friday_morning_time_in
        friday_time_out_morning = data.friday_morning_time_out
        friday_time_in_afternoon = data.friday_afternoon_time_in
        friday_time_out_afternoon = data.friday_afternoon_time_out

        saturday_time_in_morning = data.saturday_morning_time_in
        saturday_time_out_morning = data.saturday_morning_time_out
        saturday_time_in_afternoon = data.saturday_afternoon_time_in
        saturday_time_out_afternoon = data.saturday_afternoon_time_out

        sunday_time_in_morning = data.sunday_morning_time_in
        sunday_time_out_morning = data.sunday_morning_time_out
        sunday_time_in_afternoon = data.sunday_afternoon_time_in
        sunday_time_out_afternoon = data.sunday_afternoon_time_out

        monday_time_in_morning_undergrad_overload = data.monday_time_in_morning_overload_undergrad
        monday_time_out_morning_undergrad_overload = data.monday_time_out_morning_overload_undergrad
        monday_time_in_afternoon_undergrad_overload = data.monday_time_in_afternoon_overload_undergrad
        monday_time_out_afternoon_undergrad_overload = data.monday_time_out_afternoon_overload_undergrad

        monday_time_in_morning_grad_overload = data.monday_time_in_morning_overload_grad
        monday_time_out_morning_grad_overload = data.monday_time_out_morning_overload_grad
        monday_time_in_afternoon_grad_overload = data.monday_time_in_afternoon_overload_grad
        monday_time_out_afternoon_grad_overload = data.monday_time_out_afternoon_overload_grad

        tuesday_time_in_morning_undergrad_overload = data.tuesday_time_in_morning_overload_undergrad
        tuesday_time_out_morning_undergrad_overload = data.tuesday_time_out_morning_overload_undergrad
        tuesday_time_in_afternoon_undergrad_overload = data.tuesday_time_in_afternoon_overload_undergrad
        tuesday_time_out_afternoon_undergrad_overload = data.tuesday_time_out_afternoon_overload_undergrad

        tuesday_time_in_morning_grad_overload = data.tuesday_time_in_morning_overload_grad
        tuesday_time_out_morning_grad_overload = data.tuesday_time_out_morning_overload_grad
        tuesday_time_in_afternoon_grad_overload = data.tuesday_time_in_afternoon_overload_grad
        tuesday_time_out_afternoon_grad_overload = data.tuesday_time_out_afternoon_overload_grad

        wednesday_time_in_morning_undergrad_overload = data.wednesday_time_in_morning_overload_undergrad
        wednesday_time_out_morning_undergrad_overload = data.wednesday_time_out_morning_overload_undergrad
        wednesday_time_in_afternoon_undergrad_overload = data.wednesday_time_in_afternoon_overload_undergrad
        wednesday_time_out_afternoon_undergrad_overload = data.wednesday_time_out_afternoon_overload_undergrad

        wednesday_time_in_morning_grad_overload = data.wednesday_time_in_morning_overload_grad
        wednesday_time_out_morning_grad_overload = data.wednesday_time_out_morning_overload_grad
        wednesday_time_in_afternoon_grad_overload = data.wednesday_time_in_afternoon_overload_grad
        wednesday_time_out_afternoon_grad_overload = data.wednesday_time_out_afternoon_overload_grad

        thursday_time_in_morning_undergrad_overload = data.thursday_time_in_morning_overload_undergrad
        thursday_time_out_morning_undergrad_overload = data.thursday_time_out_morning_overload_undergrad
        thursday_time_in_afternoon_undergrad_overload = data.thursday_time_in_afternoon_overload_undergrad
        thursday_time_out_afternoon_undergrad_overload = data.thursday_time_out_afternoon_overload_undergrad

        thursday_time_in_morning_grad_overload = data.thursday_time_in_morning_overload_grad
        thursday_time_out_morning_grad_overload = data.thursday_time_out_morning_overload_grad
        thursday_time_in_afternoon_grad_overload = data.thursday_time_in_afternoon_overload_grad
        thursday_time_out_afternoon_grad_overload = data.thursday_time_out_afternoon_overload_grad

        friday_time_in_morning_undergrad_overload = data.friday_time_in_morning_overload_undergrad
        friday_time_out_morning_undergrad_overload = data.friday_time_out_morning_overload_undergrad
        friday_time_in_afternoon_undergrad_overload = data.friday_time_in_afternoon_overload_undergrad
        friday_time_out_afternoon_undergrad_overload = data.friday_time_out_afternoon_overload_undergrad

        friday_time_in_morning_grad_overload = data.friday_time_in_morning_overload_grad
        friday_time_out_morning_grad_overload = data.friday_time_out_morning_overload_grad
        friday_time_in_afternoon_grad_overload = data.friday_time_in_afternoon_overload_grad
        friday_time_out_afternoon_grad_overload = data.friday_time_out_afternoon_overload_grad

        saturday_time_in_morning_undergrad_overload = data.saturday_time_in_morning_overload_undergrad
        saturday_time_out_morning_undergrad_overload = data.saturday_time_out_morning_overload_undergrad
        saturday_time_in_afternoon_undergrad_overload = data.saturday_time_in_afternoon_overload_undergrad
        saturday_time_out_afternoon_undergrad_overload = data.saturday_time_out_afternoon_overload_undergrad

        saturday_time_in_morning_grad_overload = data.saturday_time_in_morning_overload_grad
        saturday_time_out_morning_grad_overload = data.saturday_time_out_morning_overload_grad
        saturday_time_in_afternoon_grad_overload = data.saturday_time_in_afternoon_overload_grad
        saturday_time_out_afternoon_grad_overload = data.saturday_time_out_afternoon_overload_grad
        
        sunday_time_in_morning_undergrad_overload = data.sunday_time_in_morning_overload_undergrad
        sunday_time_out_morning_undergrad_overload = data.sunday_time_out_morning_overload_undergrad
        sunday_time_in_afternoon_undergrad_overload = data.sunday_time_in_afternoon_overload_undergrad
        sunday_time_out_afternoon_undergrad_overload = data.sunday_time_out_afternoon_overload_undergrad

        sunday_time_in_morning_grad_overload = data.sunday_time_in_morning_overload_grad
        sunday_time_out_morning_grad_overload = data.sunday_time_out_morning_overload_grad
        sunday_time_in_afternoon_grad_overload = data.sunday_time_in_afternoon_overload_grad
        sunday_time_out_afternoon_grad_overload = data.sunday_time_out_afternoon_overload_grad

        times = generate_random_times(month, monday_time_in_morning, monday_time_out_morning, monday_time_in_afternoon, monday_time_out_afternoon,
                                        tuesday_time_in_morning, tuesday_time_out_morning, tuesday_time_in_afternoon, tuesday_time_out_afternoon,
                                        wednesday_time_in_morning, wednesday_time_out_morning, wednesday_time_in_afternoon, wednesday_time_out_afternoon,
                                        thursday_time_in_morning, thursday_time_out_morning, thursday_time_in_afternoon, thursday_time_out_afternoon,
                                        friday_time_in_morning, friday_time_out_morning, friday_time_in_afternoon, friday_time_out_afternoon,
                                        saturday_time_in_morning, saturday_time_out_morning, saturday_time_in_afternoon, saturday_time_out_afternoon,
                                        sunday_time_in_morning, sunday_time_out_morning, sunday_time_in_afternoon, sunday_time_out_afternoon, 
                                        monday_time_in_morning_undergrad_overload, monday_time_out_morning_undergrad_overload, monday_time_in_afternoon_undergrad_overload, monday_time_out_afternoon_undergrad_overload,
                                        tuesday_time_in_morning_undergrad_overload, tuesday_time_out_morning_undergrad_overload, tuesday_time_in_afternoon_undergrad_overload, tuesday_time_out_afternoon_undergrad_overload,
                                        wednesday_time_in_morning_undergrad_overload, wednesday_time_out_morning_undergrad_overload, wednesday_time_in_afternoon_undergrad_overload, wednesday_time_out_afternoon_undergrad_overload,
                                        thursday_time_in_morning_undergrad_overload, thursday_time_out_morning_undergrad_overload, thursday_time_in_afternoon_undergrad_overload, thursday_time_out_afternoon_undergrad_overload,
                                        friday_time_in_morning_undergrad_overload, friday_time_out_morning_undergrad_overload, friday_time_in_afternoon_undergrad_overload, friday_time_out_afternoon_undergrad_overload,
                                        saturday_time_in_morning_undergrad_overload, saturday_time_out_morning_undergrad_overload, saturday_time_in_afternoon_undergrad_overload, saturday_time_out_afternoon_undergrad_overload,
                                        sunday_time_in_morning_undergrad_overload, sunday_time_out_morning_undergrad_overload, sunday_time_in_afternoon_undergrad_overload, sunday_time_out_afternoon_undergrad_overload,
                                        monday_time_in_morning_grad_overload, monday_time_out_morning_grad_overload, monday_time_in_afternoon_grad_overload, monday_time_out_afternoon_grad_overload,
                                        tuesday_time_in_morning_grad_overload, tuesday_time_out_morning_grad_overload, tuesday_time_in_afternoon_grad_overload, tuesday_time_out_afternoon_grad_overload,
                                        wednesday_time_in_morning_grad_overload, wednesday_time_out_morning_grad_overload, wednesday_time_in_afternoon_grad_overload, wednesday_time_out_afternoon_grad_overload,
                                        thursday_time_in_morning_grad_overload, thursday_time_out_morning_grad_overload, thursday_time_in_afternoon_grad_overload, thursday_time_out_afternoon_grad_overload,
                                        friday_time_in_morning_grad_overload, friday_time_out_morning_grad_overload, friday_time_in_afternoon_grad_overload, friday_time_out_afternoon_grad_overload,
                                        saturday_time_in_morning_grad_overload, saturday_time_out_morning_grad_overload, saturday_time_in_afternoon_grad_overload, saturday_time_out_afternoon_grad_overload,
                                        sunday_time_in_morning_grad_overload, sunday_time_out_morning_grad_overload, sunday_time_in_afternoon_grad_overload, sunday_time_out_afternoon_grad_overload)
        
        context = {
            'month_name':month_name,
            'middle_initial':middle_initial,
        }
        context["times"] = times

        return render(request, 'undergradPrev.html', context)
    #Add warning message if the inputted data is wrong.
    return render(request, 'undergradPrev.html', context)

def gradpreview(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    data = get_object_or_404(userTime, user=user)
    context ["data"] = data
    if request.method == 'POST':
        month = data.month
        month_name = calendar.month_name[month]
        middle_initial = data.middle_initial
        monday_time_in_morning = data.monday_morning_time_in
        monday_time_out_morning = data.monday_morning_time_out
        monday_time_in_afternoon = data.monday_afternoon_time_in
        monday_time_out_afternoon = data.monday_afternoon_time_out

        tuesday_time_in_morning = data.tuesday_morning_time_in
        tuesday_time_out_morning = data.tuesday_morning_time_out
        tuesday_time_in_afternoon = data.tuesday_afternoon_time_in
        tuesday_time_out_afternoon = data.tuesday_afternoon_time_out

        wednesday_time_in_morning = data.wednesday_morning_time_in
        wednesday_time_out_morning = data.wednesday_morning_time_out
        wednesday_time_in_afternoon = data.wednesday_afternoon_time_in
        wednesday_time_out_afternoon = data.wednesday_afternoon_time_out

        thursday_time_in_morning = data.thursday_morning_time_in
        thursday_time_out_morning = data.thursday_morning_time_out
        thursday_time_in_afternoon = data.thursday_afternoon_time_in
        thursday_time_out_afternoon = data.thursday_afternoon_time_out

        friday_time_in_morning = data.friday_morning_time_in
        friday_time_out_morning = data.friday_morning_time_out
        friday_time_in_afternoon = data.friday_afternoon_time_in
        friday_time_out_afternoon = data.friday_afternoon_time_out

        saturday_time_in_morning = data.saturday_morning_time_in
        saturday_time_out_morning = data.saturday_morning_time_out
        saturday_time_in_afternoon = data.saturday_afternoon_time_in
        saturday_time_out_afternoon = data.saturday_afternoon_time_out

        sunday_time_in_morning = data.sunday_morning_time_in
        sunday_time_out_morning = data.sunday_morning_time_out
        sunday_time_in_afternoon = data.sunday_afternoon_time_in
        sunday_time_out_afternoon = data.sunday_afternoon_time_out

        monday_time_in_morning_undergrad_overload = data.monday_time_in_morning_overload_undergrad
        monday_time_out_morning_undergrad_overload = data.monday_time_out_morning_overload_undergrad
        monday_time_in_afternoon_undergrad_overload = data.monday_time_in_afternoon_overload_undergrad
        monday_time_out_afternoon_undergrad_overload = data.monday_time_out_afternoon_overload_undergrad

        monday_time_in_morning_grad_overload = data.monday_time_in_morning_overload_grad
        monday_time_out_morning_grad_overload = data.monday_time_out_morning_overload_grad
        monday_time_in_afternoon_grad_overload = data.monday_time_in_afternoon_overload_grad
        monday_time_out_afternoon_grad_overload = data.monday_time_out_afternoon_overload_grad

        tuesday_time_in_morning_undergrad_overload = data.tuesday_time_in_morning_overload_undergrad
        tuesday_time_out_morning_undergrad_overload = data.tuesday_time_out_morning_overload_undergrad
        tuesday_time_in_afternoon_undergrad_overload = data.tuesday_time_in_afternoon_overload_undergrad
        tuesday_time_out_afternoon_undergrad_overload = data.tuesday_time_out_afternoon_overload_undergrad

        tuesday_time_in_morning_grad_overload = data.tuesday_time_in_morning_overload_grad
        tuesday_time_out_morning_grad_overload = data.tuesday_time_out_morning_overload_grad
        tuesday_time_in_afternoon_grad_overload = data.tuesday_time_in_afternoon_overload_grad
        tuesday_time_out_afternoon_grad_overload = data.tuesday_time_out_afternoon_overload_grad

        wednesday_time_in_morning_undergrad_overload = data.wednesday_time_in_morning_overload_undergrad
        wednesday_time_out_morning_undergrad_overload = data.wednesday_time_out_morning_overload_undergrad
        wednesday_time_in_afternoon_undergrad_overload = data.wednesday_time_in_afternoon_overload_undergrad
        wednesday_time_out_afternoon_undergrad_overload = data.wednesday_time_out_afternoon_overload_undergrad

        wednesday_time_in_morning_grad_overload = data.wednesday_time_in_morning_overload_grad
        wednesday_time_out_morning_grad_overload = data.wednesday_time_out_morning_overload_grad
        wednesday_time_in_afternoon_grad_overload = data.wednesday_time_in_afternoon_overload_grad
        wednesday_time_out_afternoon_grad_overload = data.wednesday_time_out_afternoon_overload_grad

        thursday_time_in_morning_undergrad_overload = data.thursday_time_in_morning_overload_undergrad
        thursday_time_out_morning_undergrad_overload = data.thursday_time_out_morning_overload_undergrad
        thursday_time_in_afternoon_undergrad_overload = data.thursday_time_in_afternoon_overload_undergrad
        thursday_time_out_afternoon_undergrad_overload = data.thursday_time_out_afternoon_overload_undergrad

        thursday_time_in_morning_grad_overload = data.thursday_time_in_morning_overload_grad
        thursday_time_out_morning_grad_overload = data.thursday_time_out_morning_overload_grad
        thursday_time_in_afternoon_grad_overload = data.thursday_time_in_afternoon_overload_grad
        thursday_time_out_afternoon_grad_overload = data.thursday_time_out_afternoon_overload_grad

        friday_time_in_morning_undergrad_overload = data.friday_time_in_morning_overload_undergrad
        friday_time_out_morning_undergrad_overload = data.friday_time_out_morning_overload_undergrad
        friday_time_in_afternoon_undergrad_overload = data.friday_time_in_afternoon_overload_undergrad
        friday_time_out_afternoon_undergrad_overload = data.friday_time_out_afternoon_overload_undergrad

        friday_time_in_morning_grad_overload = data.friday_time_in_morning_overload_grad
        friday_time_out_morning_grad_overload = data.friday_time_out_morning_overload_grad
        friday_time_in_afternoon_grad_overload = data.friday_time_in_afternoon_overload_grad
        friday_time_out_afternoon_grad_overload = data.friday_time_out_afternoon_overload_grad

        saturday_time_in_morning_undergrad_overload = data.saturday_time_in_morning_overload_undergrad
        saturday_time_out_morning_undergrad_overload = data.saturday_time_out_morning_overload_undergrad
        saturday_time_in_afternoon_undergrad_overload = data.saturday_time_in_afternoon_overload_undergrad
        saturday_time_out_afternoon_undergrad_overload = data.saturday_time_out_afternoon_overload_undergrad

        saturday_time_in_morning_grad_overload = data.saturday_time_in_morning_overload_grad
        saturday_time_out_morning_grad_overload = data.saturday_time_out_morning_overload_grad
        saturday_time_in_afternoon_grad_overload = data.saturday_time_in_afternoon_overload_grad
        saturday_time_out_afternoon_grad_overload = data.saturday_time_out_afternoon_overload_grad
        
        sunday_time_in_morning_undergrad_overload = data.sunday_time_in_morning_overload_undergrad
        sunday_time_out_morning_undergrad_overload = data.sunday_time_out_morning_overload_undergrad
        sunday_time_in_afternoon_undergrad_overload = data.sunday_time_in_afternoon_overload_undergrad
        sunday_time_out_afternoon_undergrad_overload = data.sunday_time_out_afternoon_overload_undergrad

        sunday_time_in_morning_grad_overload = data.sunday_time_in_morning_overload_grad
        sunday_time_out_morning_grad_overload = data.sunday_time_out_morning_overload_grad
        sunday_time_in_afternoon_grad_overload = data.sunday_time_in_afternoon_overload_grad
        sunday_time_out_afternoon_grad_overload = data.sunday_time_out_afternoon_overload_grad

        times = generate_random_times(month, monday_time_in_morning, monday_time_out_morning, monday_time_in_afternoon, monday_time_out_afternoon,
                                        tuesday_time_in_morning, tuesday_time_out_morning, tuesday_time_in_afternoon, tuesday_time_out_afternoon,
                                        wednesday_time_in_morning, wednesday_time_out_morning, wednesday_time_in_afternoon, wednesday_time_out_afternoon,
                                        thursday_time_in_morning, thursday_time_out_morning, thursday_time_in_afternoon, thursday_time_out_afternoon,
                                        friday_time_in_morning, friday_time_out_morning, friday_time_in_afternoon, friday_time_out_afternoon,
                                        saturday_time_in_morning, saturday_time_out_morning, saturday_time_in_afternoon, saturday_time_out_afternoon,
                                        sunday_time_in_morning, sunday_time_out_morning, sunday_time_in_afternoon, sunday_time_out_afternoon, 
                                        monday_time_in_morning_undergrad_overload, monday_time_out_morning_undergrad_overload, monday_time_in_afternoon_undergrad_overload, monday_time_out_afternoon_undergrad_overload,
                                        tuesday_time_in_morning_undergrad_overload, tuesday_time_out_morning_undergrad_overload, tuesday_time_in_afternoon_undergrad_overload, tuesday_time_out_afternoon_undergrad_overload,
                                        wednesday_time_in_morning_undergrad_overload, wednesday_time_out_morning_undergrad_overload, wednesday_time_in_afternoon_undergrad_overload, wednesday_time_out_afternoon_undergrad_overload,
                                        thursday_time_in_morning_undergrad_overload, thursday_time_out_morning_undergrad_overload, thursday_time_in_afternoon_undergrad_overload, thursday_time_out_afternoon_undergrad_overload,
                                        friday_time_in_morning_undergrad_overload, friday_time_out_morning_undergrad_overload, friday_time_in_afternoon_undergrad_overload, friday_time_out_afternoon_undergrad_overload,
                                        saturday_time_in_morning_undergrad_overload, saturday_time_out_morning_undergrad_overload, saturday_time_in_afternoon_undergrad_overload, saturday_time_out_afternoon_undergrad_overload,
                                        sunday_time_in_morning_undergrad_overload, sunday_time_out_morning_undergrad_overload, sunday_time_in_afternoon_undergrad_overload, sunday_time_out_afternoon_undergrad_overload,
                                        monday_time_in_morning_grad_overload, monday_time_out_morning_grad_overload, monday_time_in_afternoon_grad_overload, monday_time_out_afternoon_grad_overload,
                                        tuesday_time_in_morning_grad_overload, tuesday_time_out_morning_grad_overload, tuesday_time_in_afternoon_grad_overload, tuesday_time_out_afternoon_grad_overload,
                                        wednesday_time_in_morning_grad_overload, wednesday_time_out_morning_grad_overload, wednesday_time_in_afternoon_grad_overload, wednesday_time_out_afternoon_grad_overload,
                                        thursday_time_in_morning_grad_overload, thursday_time_out_morning_grad_overload, thursday_time_in_afternoon_grad_overload, thursday_time_out_afternoon_grad_overload,
                                        friday_time_in_morning_grad_overload, friday_time_out_morning_grad_overload, friday_time_in_afternoon_grad_overload, friday_time_out_afternoon_grad_overload,
                                        saturday_time_in_morning_grad_overload, saturday_time_out_morning_grad_overload, saturday_time_in_afternoon_grad_overload, saturday_time_out_afternoon_grad_overload,
                                        sunday_time_in_morning_grad_overload, sunday_time_out_morning_grad_overload, sunday_time_in_afternoon_grad_overload, sunday_time_out_afternoon_grad_overload)
        
        context = {
            'month_name':month_name,
            'middle_initial':middle_initial,
        }
        context["times"] = times

        return render(request, 'gradPrev.html', context)
    #Add warning message if the inputted data is wrong.
    return render(request, 'gradPrev.html', context)


@login_required
def saveTimes(request):
    context = {}
    user = get_object_or_404(User, id=request.user.id)
    data = get_object_or_404(userTime, user=user)
    context ["data"] = data
    if request.method == 'POST':
        
        firstName = request.POST.get('firstName')
        middle_initial = request.POST.get('middleInitial')
        lastName = request.POST.get('lastName')
        month = request.POST.get('month')

        monday_time_in_morning = request.POST.get('monday_time_in_morning')
        monday_time_out_morning = request.POST.get('monday_time_out_morning')
        monday_time_in_afternoon = request.POST.get('monday_time_in_afternoon')
        monday_time_out_afternoon = request.POST.get('monday_time_out_afternoon')

        tuesday_time_in_morning = request.POST.get('tuesday_time_in_morning')
        tuesday_time_out_morning = request.POST.get('tuesday_time_out_morning')
        tuesday_time_in_afternoon = request.POST.get('tuesday_time_in_afternoon')
        tuesday_time_out_afternoon = request.POST.get('tuesday_time_out_afternoon')

        wednesday_time_in_morning = request.POST.get('wednesday_time_in_morning')
        wednesday_time_out_morning = request.POST.get('wednesday_time_out_morning')
        wednesday_time_in_afternoon = request.POST.get('wednesday_time_in_afternoon')
        wednesday_time_out_afternoon = request.POST.get('wednesday_time_out_afternoon')

        thursday_time_in_morning = request.POST.get('thursday_time_in_morning')
        thursday_time_out_morning = request.POST.get('thursday_time_out_morning')
        thursday_time_in_afternoon = request.POST.get('thursday_time_in_afternoon')
        thursday_time_out_afternoon = request.POST.get('thursday_time_out_afternoon')

        friday_time_in_morning = request.POST.get('friday_time_in_morning')
        friday_time_out_morning = request.POST.get('friday_time_out_morning')
        friday_time_in_afternoon = request.POST.get('friday_time_in_afternoon')
        friday_time_out_afternoon = request.POST.get('friday_time_out_afternoon')

        saturday_time_in_morning = request.POST.get('saturday_time_in_morning')
        saturday_time_out_morning = request.POST.get('saturday_time_out_morning')
        saturday_time_in_afternoon = request.POST.get('saturday_time_in_afternoon')
        saturday_time_out_afternoon = request.POST.get('saturday_time_out_afternoon')

        sunday_time_in_morning = request.POST.get('sunday_time_in_morning')
        sunday_time_out_morning = request.POST.get('sunday_time_out_morning')
        sunday_time_in_afternoon = request.POST.get('sunday_time_in_afternoon')
        sunday_time_out_afternoon = request.POST.get('sunday_time_out_afternoon')

        
        monday_time_in_morning_overload_undergrad = request.POST.get('monday_time_in_morning_overload_undergrad')
        monday_time_out_morning_overload_undergrad = request.POST.get('monday_time_out_morning_overload_undergrad')
        monday_time_in_afternoon_overload_undergrad = request.POST.get('monday_time_in_afternoon_overload_undergrad')
        monday_time_out_afternoon_overload_undergrad = request.POST.get('monday_time_out_afternoon_overload_undergrad')

        tuesday_time_in_morning_overload_undergrad = request.POST.get('tuesday_time_in_morning_overload_undergrad')
        tuesday_time_out_morning_overload_undergrad = request.POST.get('tuesday_time_out_morning_overload_undergrad')
        tuesday_time_in_afternoon_overload_undergrad = request.POST.get('tuesday_time_in_afternoon_overload_undergrad')
        tuesday_time_out_afternoon_overload_undergrad = request.POST.get('tuesday_time_out_afternoon_overload_undergrad')
        
        wednesday_time_in_morning_overload_undergrad = request.POST.get('wednesday_time_in_morning_overload_undergrad')
        wednesday_time_out_morning_overload_undergrad = request.POST.get('wednesday_time_out_morning_overload_undergrad')
        wednesday_time_in_afternoon_overload_undergrad = request.POST.get('wednesday_time_in_afternoon_overload_undergrad')
        wednesday_time_out_afternoon_overload_undergrad = request.POST.get('wednesday_time_out_afternoon_overload_undergrad')

        thursday_time_in_morning_overload_undergrad = request.POST.get('thursday_time_in_morning_overload_undergrad')
        thursday_time_out_morning_overload_undergrad = request.POST.get('thursday_time_out_morning_overload_undergrad')
        thursday_time_in_afternoon_overload_undergrad = request.POST.get('thursday_time_in_afternoon_overload_undergrad')
        thursday_time_out_afternoon_overload_undergrad = request.POST.get('thursday_time_out_afternoon_overload_undergrad')

        friday_time_in_morning_overload_undergrad = request.POST.get('friday_time_in_morning_overload_undergrad')
        friday_time_out_morning_overload_undergrad = request.POST.get('friday_time_out_morning_overload_undergrad')
        friday_time_in_afternoon_overload_undergrad = request.POST.get('friday_time_in_afternoon_overload_undergrad')
        friday_time_out_afternoon_overload_undergrad = request.POST.get('friday_time_out_afternoon_overload_undergrad')

        saturday_time_in_morning_overload_undergrad = request.POST.get('saturday_time_in_morning_overload_undergrad')
        saturday_time_out_morning_overload_undergrad = request.POST.get('saturday_time_out_morning_overload_undergrad')
        saturday_time_in_afternoon_overload_undergrad = request.POST.get('saturday_time_in_afternoon_overload_undergrad')
        saturday_time_out_afternoon_overload_undergrad = request.POST.get('saturday_time_out_afternoon_overload_undergrad')

        sunday_time_in_morning_overload_undergrad = request.POST.get('sunday_time_in_morning_overload_undergrad')
        sunday_time_out_morning_overload_undergrad = request.POST.get('sunday_time_out_morning_overload_undergrad')
        sunday_time_in_afternoon_overload_undergrad = request.POST.get('sunday_time_in_afternoon_overload_undergrad')
        sunday_time_out_afternoon_overload_undergrad = request.POST.get('sunday_time_out_afternoon_overload_undergrad')

        monday_time_in_morning_overload_grad = request.POST.get('monday_time_in_morning_overload_grad')
        monday_time_out_morning_overload_grad = request.POST.get('monday_time_out_morning_overload_grad')
        monday_time_in_afternoon_overload_grad = request.POST.get('monday_time_in_afternoon_overload_grad')
        monday_time_out_afternoon_overload_grad = request.POST.get('monday_time_out_afternoon_overload_grad')

        tuesday_time_in_morning_overload_grad = request.POST.get('tuesday_time_in_morning_overload_grad')
        tuesday_time_out_morning_overload_grad = request.POST.get('tuesday_time_out_morning_overload_grad')
        tuesday_time_in_afternoon_overload_grad = request.POST.get('tuesday_time_in_afternoon_overload_grad')
        tuesday_time_out_afternoon_overload_grad = request.POST.get('tuesday_time_out_afternoon_overload_grad')
        
        wednesday_time_in_morning_overload_grad = request.POST.get('wednesday_time_in_morning_overload_grad')
        wednesday_time_out_morning_overload_grad = request.POST.get('wednesday_time_out_morning_overload_grad')
        wednesday_time_in_afternoon_overload_grad = request.POST.get('wednesday_time_in_afternoon_overload_grad')
        wednesday_time_out_afternoon_overload_grad = request.POST.get('wednesday_time_out_afternoon_overload_grad')

        thursday_time_in_morning_overload_grad = request.POST.get('thursday_time_in_morning_overload_grad')
        thursday_time_out_morning_overload_grad = request.POST.get('thursday_time_out_morning_overload_grad')
        thursday_time_in_afternoon_overload_grad = request.POST.get('thursday_time_in_afternoon_overload_grad')
        thursday_time_out_afternoon_overload_grad = request.POST.get('thursday_time_out_afternoon_overload_grad')

        friday_time_in_morning_overload_grad = request.POST.get('friday_time_in_morning_overload_grad')
        friday_time_out_morning_overload_grad = request.POST.get('friday_time_out_morning_overload_grad')
        friday_time_in_afternoon_overload_grad = request.POST.get('friday_time_in_afternoon_overload_grad')
        friday_time_out_afternoon_overload_grad = request.POST.get('friday_time_out_afternoon_overload_grad')

        saturday_time_in_morning_overload_grad = request.POST.get('saturday_time_in_morning_overload_grad')
        saturday_time_out_morning_overload_grad = request.POST.get('saturday_time_out_morning_overload_grad')
        saturday_time_in_afternoon_overload_grad = request.POST.get('saturday_time_in_afternoon_overload_grad')
        saturday_time_out_afternoon_overload_grad = request.POST.get('saturday_time_out_afternoon_overload_grad')

        sunday_time_in_morning_overload_grad = request.POST.get('sunday_time_in_morning_overload_grad')
        sunday_time_out_morning_overload_grad = request.POST.get('sunday_time_out_morning_overload_grad')
        sunday_time_in_afternoon_overload_grad = request.POST.get('sunday_time_in_afternoon_overload_grad')
        sunday_time_out_afternoon_overload_grad = request.POST.get('sunday_time_out_afternoon_overload_grad')

        user.first_name = firstName
        user.last_name = lastName
    
        data.first_name = firstName
        data.last_name = lastName
        data.middle_initial = middle_initial
        data.month = month
        data.monday_morning_time_in = monday_time_in_morning
        data.monday_morning_time_out = monday_time_out_morning
        data.monday_afternoon_time_in = monday_time_in_afternoon
        data.monday_afternoon_time_out = monday_time_out_afternoon
        data.tuesday_morning_time_in = tuesday_time_in_morning
        data.tuesday_morning_time_out = tuesday_time_out_morning
        data.tuesday_afternoon_time_in = tuesday_time_in_afternoon
        data.tuesday_afternoon_time_out = tuesday_time_out_afternoon
        data.wednesday_morning_time_in = wednesday_time_in_morning
        data.wednesday_morning_time_out = wednesday_time_out_morning
        data.wednesday_afternoon_time_in = wednesday_time_in_afternoon
        data.wednesday_afternoon_time_out = wednesday_time_out_afternoon
        data.thursday_morning_time_in = thursday_time_in_morning
        data.thursday_morning_time_out = thursday_time_out_morning
        data.thursday_afternoon_time_in = thursday_time_in_afternoon
        data.thursday_afternoon_time_out = thursday_time_out_afternoon
        data.friday_morning_time_in = friday_time_in_morning
        data.friday_morning_time_out = friday_time_out_morning
        data.friday_afternoon_time_in = friday_time_in_afternoon
        data.friday_afternoon_time_out = friday_time_out_afternoon
        data.saturday_morning_time_in = saturday_time_in_morning
        data.saturday_morning_time_out = saturday_time_out_morning
        data.saturday_afternoon_time_in = saturday_time_in_afternoon
        data.saturday_afternoon_time_out = saturday_time_out_afternoon
        data.sunday_morning_time_in = sunday_time_in_morning
        data.sunday_morning_time_out = sunday_time_out_morning
        data.sunday_afternoon_time_in = sunday_time_in_afternoon
        data.sunday_afternoon_time_out = sunday_time_out_afternoon
        data.monday_time_in_morning_overload_undergrad = monday_time_in_morning_overload_undergrad
        data.monday_time_out_morning_overload_undergrad = monday_time_out_morning_overload_undergrad
        data.monday_time_in_afternoon_overload_undergrad = monday_time_in_afternoon_overload_undergrad
        data.monday_time_out_afternoon_overload_undergrad = monday_time_out_afternoon_overload_undergrad
        data.tuesday_time_in_morning_overload_undergrad = tuesday_time_in_morning_overload_undergrad
        data.tuesday_time_out_morning_overload_undergrad = tuesday_time_out_morning_overload_undergrad
        data.tuesday_time_in_afternoon_overload_undergrad = tuesday_time_in_afternoon_overload_undergrad
        data.tuesday_time_out_afternoon_overload_undergrad = tuesday_time_out_afternoon_overload_undergrad
        data.wednesday_time_in_morning_overload_undergrad = wednesday_time_in_morning_overload_undergrad
        data.wednesday_time_out_morning_overload_undergrad = wednesday_time_out_morning_overload_undergrad
        data.wednesday_time_in_afternoon_overload_undergrad = wednesday_time_in_afternoon_overload_undergrad
        data.wednesday_time_out_afternoon_overload_undergrad = wednesday_time_out_afternoon_overload_undergrad
        data.thursday_time_in_morning_overload_undergrad = thursday_time_in_morning_overload_undergrad
        data.thursday_time_out_morning_overload_undergrad = thursday_time_out_morning_overload_undergrad
        data.thursday_time_in_afternoon_overload_undergrad = thursday_time_in_afternoon_overload_undergrad
        data.thursday_time_out_afternoon_overload_undergrad = thursday_time_out_afternoon_overload_undergrad
        data.friday_time_in_morning_overload_undergrad = friday_time_in_morning_overload_undergrad
        data.friday_time_out_morning_overload_undergrad = friday_time_out_morning_overload_undergrad
        data.friday_time_in_afternoon_overload_undergrad = friday_time_in_afternoon_overload_undergrad
        data.friday_time_out_afternoon_overload_undergrad = friday_time_out_afternoon_overload_undergrad
        data.saturday_time_in_morning_overload_undergrad = saturday_time_in_morning_overload_undergrad
        data.saturday_time_out_morning_overload_undergrad = saturday_time_out_morning_overload_undergrad
        data.saturday_time_in_afternoon_overload_undergrad = saturday_time_in_afternoon_overload_undergrad
        data.saturday_time_out_afternoon_overload_undergrad = saturday_time_out_afternoon_overload_undergrad
        data.sunday_time_in_morning_overload_undergrad = sunday_time_in_morning_overload_undergrad
        data.sunday_time_out_morning_overload_undergrad = sunday_time_out_morning_overload_undergrad
        data.sunday_time_in_afternoon_overload_undergrad = sunday_time_in_afternoon_overload_undergrad
        data.sunday_time_out_afternoon_overload_undergrad = sunday_time_out_afternoon_overload_undergrad
        data.monday_time_in_morning_overload_grad = monday_time_in_morning_overload_grad
        data.monday_time_out_morning_overload_grad = monday_time_out_morning_overload_grad
        data.monday_time_in_afternoon_overload_grad = monday_time_in_afternoon_overload_grad
        data.monday_time_out_afternoon_overload_grad = monday_time_out_afternoon_overload_grad
        data.tuesday_time_in_morning_overload_grad = tuesday_time_in_morning_overload_grad
        data.tuesday_time_out_morning_overload_grad = tuesday_time_out_morning_overload_grad
        data.tuesday_time_in_afternoon_overload_grad = tuesday_time_in_afternoon_overload_grad
        data.tuesday_time_out_afternoon_overload_grad = tuesday_time_out_afternoon_overload_grad
        data.wednesday_time_in_morning_overload_grad = wednesday_time_in_morning_overload_grad
        data.wednesday_time_out_morning_overload_grad = wednesday_time_out_morning_overload_grad
        data.wednesday_time_in_afternoon_overload_grad = wednesday_time_in_afternoon_overload_grad
        data.wednesday_time_out_afternoon_overload_grad = wednesday_time_out_afternoon_overload_grad
        data.thursday_time_in_morning_overload_grad = thursday_time_in_morning_overload_grad
        data.thursday_time_out_morning_overload_grad = thursday_time_out_morning_overload_grad
        data.thursday_time_in_afternoon_overload_grad = thursday_time_in_afternoon_overload_grad
        data.thursday_time_out_afternoon_overload_grad = thursday_time_out_afternoon_overload_grad
        data.friday_time_in_morning_overload_grad = friday_time_in_morning_overload_grad
        data.friday_time_out_morning_overload_grad = friday_time_out_morning_overload_grad
        data.friday_time_in_afternoon_overload_grad = friday_time_in_afternoon_overload_grad
        data.friday_time_out_afternoon_overload_grad = friday_time_out_afternoon_overload_grad
        data.saturday_time_in_morning_overload_grad = saturday_time_in_morning_overload_grad
        data.saturday_time_out_morning_overload_grad = saturday_time_out_morning_overload_grad
        data.saturday_time_in_afternoon_overload_grad = saturday_time_in_afternoon_overload_grad
        data.saturday_time_out_afternoon_overload_grad = saturday_time_out_afternoon_overload_grad
        data.sunday_time_in_morning_overload_grad = sunday_time_in_morning_overload_grad
        data.sunday_time_out_morning_overload_grad = sunday_time_out_morning_overload_grad
        data.sunday_time_in_afternoon_overload_grad = sunday_time_in_afternoon_overload_grad
        data.sunday_time_out_afternoon_overload_grad = sunday_time_out_afternoon_overload_grad

        data.save()
        user.save()
        
        return render(request, 'myprofile.html', context)
    return render(request, 'myprofile.html', context)



def generate_random_times(month, monday_morning_time_in, monday_morning_time_out, monday_afternoon_time_in, monday_afternoon_time_out,
                          tuesday_morning_time_in, tuesday_morning_time_out, tuesday_afternoon_time_in, tuesday_afternoon_time_out,
                          wednesday_morning_time_in, wednesday_morning_time_out, wednesday_afternoon_time_in, wednesday_afternoon_time_out,
                          thursday_morning_time_in, thursday_morning_time_out, thursday_afternoon_time_in, thursday_afternoon_time_out,
                          friday_morning_time_in, friday_morning_time_out, friday_afternoon_time_in, friday_afternoon_time_out,
                          saturday_morning_time_in, saturday_morning_time_out, saturday_afternoon_time_in, saturday_afternoon_time_out,
                          sunday_morning_time_in, sunday_morning_time_out, sunday_afternoon_time_in, sunday_afternoon_time_out, 
                                monday_time_in_morning_overload_undergrad, monday_time_out_morning_overload_undergrad, monday_time_in_afternoon_overload_undergrad, monday_time_out_afternoon_overload_undergrad,
                                    tuesday_time_in_morning_overload_undergrad, tuesday_time_out_morning_overload_undergrad, tuesday_time_in_afternoon_overload_undergrad, tuesday_time_out_afternoon_overload_undergrad,
                                    wednesday_time_in_morning_overload_undergrad, wednesday_time_out_morning_overload_undergrad, wednesday_time_in_afternoon_overload_undergrad, wednesday_time_out_afternoon_overload_undergrad,
                                    thursday_time_in_morning_overload_undergrad, thursday_time_out_morning_overload_undergrad, thursday_time_in_afternoon_overload_undergrad, thursday_time_out_afternoon_overload_undergrad,
                                    friday_time_in_morning_overload_undergrad, friday_time_out_morning_overload_undergrad, friday_time_in_afternoon_overload_undergrad, friday_time_out_afternoon_overload_undergrad,
                                    saturday_time_in_morning_overload_undergrad, saturday_time_out_morning_overload_undergrad, saturday_time_in_afternoon_overload_undergrad, saturday_time_out_afternoon_overload_undergrad,
                                    sunday_time_in_morning_overload_undergrad, sunday_time_out_morning_overload_undergrad, sunday_time_in_afternoon_overload_undergrad, sunday_time_out_afternoon_overload_undergrad,
                                    monday_time_in_morning_overload_grad, monday_time_out_morning_overload_grad, monday_time_in_afternoon_overload_grad, monday_time_out_afternoon_overload_grad,
                                    tuesday_time_in_morning_overload_grad, tuesday_time_out_morning_overload_grad, tuesday_time_in_afternoon_overload_grad, tuesday_time_out_afternoon_overload_grad,
                                    wednesday_time_in_morning_overload_grad, wednesday_time_out_morning_overload_grad, wednesday_time_in_afternoon_overload_grad, wednesday_time_out_afternoon_overload_grad,
                                    thursday_time_in_morning_overload_grad, thursday_time_out_morning_overload_grad, thursday_time_in_afternoon_overload_grad, thursday_time_out_afternoon_overload_grad,
                                    friday_time_in_morning_overload_grad, friday_time_out_morning_overload_grad, friday_time_in_afternoon_overload_grad, friday_time_out_afternoon_overload_grad,
                                    saturday_time_in_morning_overload_grad, saturday_time_out_morning_overload_grad, saturday_time_in_afternoon_overload_grad, saturday_time_out_afternoon_overload_grad,
                                    sunday_time_in_morning_overload_grad, sunday_time_out_morning_overload_grad, sunday_time_in_afternoon_overload_grad, sunday_time_out_afternoon_overload_grad):
    month_int = int(month)
    

    if monday_morning_time_in:
        monday_morning_time_in_dt = datetime.strptime(monday_morning_time_in, '%H:%M').time()
    else:
        monday_morning_time_in_dt = None
    if monday_morning_time_out:
        monday_morning_time_out_dt = datetime.strptime(monday_morning_time_out, '%H:%M').time()
    else:
        monday_morning_time_out_dt = None
    if monday_afternoon_time_in:
        monday_afternoon_time_in_dt = datetime.strptime(monday_afternoon_time_in, '%H:%M').time()
    else:
        monday_afternoon_time_in_dt = None
    if monday_afternoon_time_out:
        monday_afternoon_time_out_dt = datetime.strptime(monday_afternoon_time_out, '%H:%M').time()
    else:
        monday_afternoon_time_out_dt = None

    if tuesday_morning_time_in:
        tuesday_morning_time_in_dt = datetime.strptime(tuesday_morning_time_in, '%H:%M').time()
    else:
        tuesday_morning_time_in_dt = None
    if tuesday_morning_time_out:
        tuesday_morning_time_out_dt = datetime.strptime(tuesday_morning_time_out, '%H:%M').time()
    else:
        tuesday_morning_time_out_dt = None
    if tuesday_afternoon_time_in:
        tuesday_afternoon_time_in_dt = datetime.strptime(tuesday_afternoon_time_in, '%H:%M').time()
    else:
        tuesday_afternoon_time_in_dt = None
    if tuesday_afternoon_time_out:
        tuesday_afternoon_time_out_dt = datetime.strptime(tuesday_afternoon_time_out, '%H:%M').time()
    else:
        tuesday_afternoon_time_out_dt = None

    if wednesday_morning_time_in:
        wednesday_morning_time_in_dt = datetime.strptime(wednesday_morning_time_in, '%H:%M').time()
    else:
        wednesday_morning_time_in_dt = None
    if wednesday_morning_time_out:
        wednesday_morning_time_out_dt = datetime.strptime(wednesday_morning_time_out, '%H:%M').time()
    else:
        wednesday_morning_time_out_dt = None
    if wednesday_afternoon_time_in:
        wednesday_afternoon_time_in_dt = datetime.strptime(wednesday_afternoon_time_in, '%H:%M').time()
    else:
        wednesday_afternoon_time_in_dt = None
    if wednesday_afternoon_time_out:
        wednesday_afternoon_time_out_dt = datetime.strptime(wednesday_afternoon_time_out, '%H:%M').time()
    else:
        wednesday_afternoon_time_out_dt = None

    if thursday_morning_time_in:
        thursday_morning_time_in_dt = datetime.strptime(thursday_morning_time_in, '%H:%M').time()
    else:
        thursday_morning_time_in_dt = None
    if thursday_morning_time_out:
        thursday_morning_time_out_dt = datetime.strptime(thursday_morning_time_out, '%H:%M').time()
    else:
        thursday_morning_time_out_dt = None
    if thursday_afternoon_time_in:
        thursday_afternoon_time_in_dt = datetime.strptime(thursday_afternoon_time_in, '%H:%M').time()
    else:
        thursday_afternoon_time_in_dt = None
    if thursday_afternoon_time_out:
        thursday_afternoon_time_out_dt = datetime.strptime(thursday_afternoon_time_out, '%H:%M').time()
    else:
        thursday_afternoon_time_out_dt = None

    if friday_morning_time_in:
        friday_morning_time_in_dt = datetime.strptime(friday_morning_time_in, '%H:%M').time()
    else:
        friday_morning_time_in_dt = None
    if friday_morning_time_out:
        friday_morning_time_out_dt = datetime.strptime(friday_morning_time_out, '%H:%M').time()
    else:
        friday_morning_time_out_dt = None
    if friday_afternoon_time_in:
        friday_afternoon_time_in_dt = datetime.strptime(friday_afternoon_time_in, '%H:%M').time()
    else:
        friday_afternoon_time_in_dt = None
    if friday_afternoon_time_out:
        friday_afternoon_time_out_dt = datetime.strptime(friday_afternoon_time_out, '%H:%M').time()
    else:
        friday_afternoon_time_out_dt = None

    if saturday_morning_time_in:
        saturday_morning_time_in_dt = datetime.strptime(saturday_morning_time_in, '%H:%M').time()
    else:
        saturday_morning_time_in_dt = None
    if saturday_morning_time_out:
        saturday_morning_time_out_dt = datetime.strptime(saturday_morning_time_out, '%H:%M').time()
    else:
        saturday_morning_time_out_dt = None
    if saturday_afternoon_time_in:
        saturday_afternoon_time_in_dt = datetime.strptime(saturday_afternoon_time_in, '%H:%M').time()
    else:
        saturday_afternoon_time_in_dt = None
    if saturday_afternoon_time_out:
        saturday_afternoon_time_out_dt = datetime.strptime(saturday_afternoon_time_out, '%H:%M').time()
    else:
        saturday_afternoon_time_out_dt = None

    if sunday_morning_time_in:
        sunday_morning_time_in_dt = datetime.strptime(sunday_morning_time_in, '%H:%M').time()
    else:
        sunday_morning_time_in_dt = None
    if sunday_morning_time_out:
        sunday_morning_time_out_dt = datetime.strptime(sunday_morning_time_out, '%H:%M').time()
    else:
        sunday_morning_time_out_dt = None
    if sunday_afternoon_time_in:
        sunday_afternoon_time_in_dt = datetime.strptime(sunday_afternoon_time_in, '%H:%M').time()
    else:
        sunday_afternoon_time_in_dt = None
    if sunday_afternoon_time_out:
        sunday_afternoon_time_out_dt = datetime.strptime(sunday_afternoon_time_out, '%H:%M').time()
    else:
        sunday_afternoon_time_out_dt = None

    if monday_time_in_morning_overload_undergrad:
        monday_morning_time_in_overload_undergrad_dt = datetime.strptime(monday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        monday_morning_time_in_overload_undergrad_dt = None
    if monday_time_out_morning_overload_undergrad:
        monday_morning_time_out_overload_undergrad_dt = datetime.strptime(monday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        monday_morning_time_out_overload_undergrad_dt = None
    if monday_time_in_afternoon_overload_undergrad:
        monday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(monday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        monday_afternoon_time_in_overload_undergrad_dt = None
    if monday_time_out_afternoon_overload_undergrad:
        monday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(monday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        monday_afternoon_time_out_overload_undergrad_dt = None

    if tuesday_time_in_morning_overload_undergrad:
        tuesday_morning_time_in_overload_undergrad_dt = datetime.strptime(tuesday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        tuesday_morning_time_in_overload_undergrad_dt = None
    if tuesday_time_out_morning_overload_undergrad:
        tuesday_morning_time_out_overload_undergrad_dt = datetime.strptime(tuesday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        tuesday_morning_time_out_overload_undergrad_dt = None
    if tuesday_time_in_afternoon_overload_undergrad:
        tuesday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(tuesday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        tuesday_afternoon_time_in_overload_undergrad_dt = None
    if tuesday_time_out_afternoon_overload_undergrad:
        tuesday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(tuesday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        tuesday_afternoon_time_out_overload_undergrad_dt = None

    if wednesday_time_in_morning_overload_undergrad:
        wednesday_morning_time_in_overload_undergrad_dt = datetime.strptime(wednesday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        wednesday_morning_time_in_overload_undergrad_dt = None
    if wednesday_time_out_morning_overload_undergrad:
        wednesday_morning_time_out_overload_undergrad_dt = datetime.strptime(wednesday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        wednesday_morning_time_out_overload_undergrad_dt = None
    if wednesday_time_in_afternoon_overload_undergrad:
        wednesday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(wednesday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        wednesday_afternoon_time_in_overload_undergrad_dt = None
    if wednesday_time_out_afternoon_overload_undergrad:
        wednesday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(wednesday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        wednesday_afternoon_time_out_overload_undergrad_dt = None

    if thursday_time_in_morning_overload_undergrad:
        thursday_morning_time_in_overload_undergrad_dt = datetime.strptime(thursday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        thursday_morning_time_in_overload_undergrad_dt = None
    if thursday_time_out_morning_overload_undergrad:
        thursday_morning_time_out_overload_undergrad_dt = datetime.strptime(thursday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        thursday_morning_time_out_overload_undergrad_dt = None
    if thursday_time_in_afternoon_overload_undergrad:
        thursday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(thursday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        thursday_afternoon_time_in_overload_undergrad_dt = None
    if thursday_time_out_afternoon_overload_undergrad:
        thursday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(thursday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        thursday_afternoon_time_out_overload_undergrad_dt = None

    if friday_time_in_morning_overload_undergrad:
        friday_morning_time_in_overload_undergrad_dt = datetime.strptime(friday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        friday_morning_time_in_overload_undergrad_dt = None
    if friday_time_out_morning_overload_undergrad:
        friday_morning_time_out_overload_undergrad_dt = datetime.strptime(friday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        friday_morning_time_out_overload_undergrad_dt = None
    if friday_time_in_afternoon_overload_undergrad:
        friday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(friday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        friday_afternoon_time_in_overload_undergrad_dt = None
    if friday_time_out_afternoon_overload_undergrad:
        friday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(friday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        friday_afternoon_time_out_overload_undergrad_dt = None

    if saturday_time_in_morning_overload_undergrad:
        saturday_morning_time_in_overload_undergrad_dt = datetime.strptime(saturday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        saturday_morning_time_in_overload_undergrad_dt = None
    if saturday_time_out_morning_overload_undergrad:
        saturday_morning_time_out_overload_undergrad_dt = datetime.strptime(saturday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        saturday_morning_time_out_overload_undergrad_dt = None
    if saturday_time_in_afternoon_overload_undergrad:
        saturday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(saturday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        saturday_afternoon_time_in_overload_undergrad_dt = None
    if saturday_time_out_afternoon_overload_undergrad:
        saturday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(saturday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        saturday_afternoon_time_out_overload_undergrad_dt = None

    if sunday_time_in_morning_overload_undergrad:
        sunday_morning_time_in_overload_undergrad_dt = datetime.strptime(sunday_time_in_morning_overload_undergrad, '%H:%M').time()
    else:
        sunday_morning_time_in_overload_undergrad_dt = None
    if sunday_time_out_morning_overload_undergrad:
        sunday_morning_time_out_overload_undergrad_dt = datetime.strptime(sunday_time_out_morning_overload_undergrad, '%H:%M').time()
    else:
        sunday_morning_time_out_overload_undergrad_dt = None
    if sunday_time_in_afternoon_overload_undergrad:
        sunday_afternoon_time_in_overload_undergrad_dt = datetime.strptime(sunday_time_in_afternoon_overload_undergrad, '%H:%M').time()
    else:
        sunday_afternoon_time_in_overload_undergrad_dt = None
    if sunday_time_out_afternoon_overload_undergrad:
        sunday_afternoon_time_out_overload_undergrad_dt = datetime.strptime(sunday_time_out_afternoon_overload_undergrad, '%H:%M').time()
    else:
        sunday_afternoon_time_out_overload_undergrad_dt = None

    if monday_time_in_morning_overload_grad:
        monday_morning_time_in_overload_grad_dt = datetime.strptime(monday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        monday_morning_time_in_overload_grad_dt = None
    if monday_time_out_morning_overload_grad:
        monday_morning_time_out_overload_grad_dt = datetime.strptime(monday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        monday_morning_time_out_overload_grad_dt = None
    if monday_time_in_afternoon_overload_grad:
        monday_afternoon_time_in_overload_grad_dt = datetime.strptime(monday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        monday_afternoon_time_in_overload_grad_dt = None
    if monday_time_out_afternoon_overload_grad:
        monday_afternoon_time_out_overload_grad_dt = datetime.strptime(monday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        monday_afternoon_time_out_overload_grad_dt = None

    if tuesday_time_in_morning_overload_grad:
        tuesday_morning_time_in_overload_grad_dt = datetime.strptime(tuesday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        tuesday_morning_time_in_overload_grad_dt = None
    if tuesday_time_out_morning_overload_grad:
        tuesday_morning_time_out_overload_grad_dt = datetime.strptime(tuesday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        tuesday_morning_time_out_overload_grad_dt = None
    if tuesday_time_in_afternoon_overload_grad:
        tuesday_afternoon_time_in_overload_grad_dt = datetime.strptime(tuesday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        tuesday_afternoon_time_in_overload_grad_dt = None
    if tuesday_time_out_afternoon_overload_grad:
        tuesday_afternoon_time_out_overload_grad_dt = datetime.strptime(tuesday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        tuesday_afternoon_time_out_overload_grad_dt = None

    if wednesday_time_in_morning_overload_grad:
        wednesday_morning_time_in_overload_grad_dt = datetime.strptime(wednesday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        wednesday_morning_time_in_overload_grad_dt = None
    if wednesday_time_out_morning_overload_grad:
        wednesday_morning_time_out_overload_grad_dt = datetime.strptime(wednesday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        wednesday_morning_time_out_overload_grad_dt = None
    if wednesday_time_in_afternoon_overload_grad:
        wednesday_afternoon_time_in_overload_grad_dt = datetime.strptime(wednesday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        wednesday_afternoon_time_in_overload_grad_dt = None
    if wednesday_time_out_afternoon_overload_grad:
        wednesday_afternoon_time_out_overload_grad_dt = datetime.strptime(wednesday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        wednesday_afternoon_time_out_overload_grad_dt = None

    if thursday_time_in_morning_overload_grad:
        thursday_morning_time_in_overload_grad_dt = datetime.strptime(thursday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        thursday_morning_time_in_overload_grad_dt = None
    if thursday_time_out_morning_overload_grad:
        thursday_morning_time_out_overload_grad_dt = datetime.strptime(thursday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        thursday_morning_time_out_overload_grad_dt = None
    if thursday_time_in_afternoon_overload_grad:
        thursday_afternoon_time_in_overload_grad_dt = datetime.strptime(thursday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        thursday_afternoon_time_in_overload_grad_dt = None
    if thursday_time_out_afternoon_overload_grad:
        thursday_afternoon_time_out_overload_grad_dt = datetime.strptime(thursday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        thursday_afternoon_time_out_overload_grad_dt = None

    if friday_time_in_morning_overload_grad:
        friday_morning_time_in_overload_grad_dt = datetime.strptime(friday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        friday_morning_time_in_overload_grad_dt = None
    if friday_time_out_morning_overload_grad:
        friday_morning_time_out_overload_grad_dt = datetime.strptime(friday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        friday_morning_time_out_overload_grad_dt = None
    if friday_time_in_afternoon_overload_grad:
        friday_afternoon_time_in_overload_grad_dt = datetime.strptime(friday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        friday_afternoon_time_in_overload_grad_dt = None
    if friday_time_out_afternoon_overload_grad:
        friday_afternoon_time_out_overload_grad_dt = datetime.strptime(friday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        friday_afternoon_time_out_overload_grad_dt = None

    if saturday_time_in_morning_overload_grad:
        saturday_morning_time_in_overload_grad_dt = datetime.strptime(saturday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        saturday_morning_time_in_overload_grad_dt = None
    if saturday_time_out_morning_overload_grad:
        saturday_morning_time_out_overload_grad_dt = datetime.strptime(saturday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        saturday_morning_time_out_overload_grad_dt = None
    if saturday_time_in_afternoon_overload_grad:
        saturday_afternoon_time_in_overload_grad_dt = datetime.strptime(saturday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        saturday_afternoon_time_in_overload_grad_dt = None
    if saturday_time_out_afternoon_overload_grad:
        saturday_afternoon_time_out_overload_grad_dt = datetime.strptime(saturday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        saturday_afternoon_time_out_overload_grad_dt = None

    if sunday_time_in_morning_overload_grad:
        sunday_morning_time_in_overload_grad_dt = datetime.strptime(sunday_time_in_morning_overload_grad, '%H:%M').time()
    else:
        sunday_morning_time_in_overload_grad_dt = None
    if sunday_time_out_morning_overload_grad:
        sunday_morning_time_out_overload_grad_dt = datetime.strptime(sunday_time_out_morning_overload_grad, '%H:%M').time()
    else:
        sunday_morning_time_out_overload_grad_dt = None
    if sunday_time_in_afternoon_overload_grad:
        sunday_afternoon_time_in_overload_grad_dt = datetime.strptime(sunday_time_in_afternoon_overload_grad, '%H:%M').time()
    else:
        sunday_afternoon_time_in_overload_grad_dt = None
    if sunday_time_out_afternoon_overload_grad:
        sunday_afternoon_time_out_overload_grad_dt = datetime.strptime(sunday_time_out_afternoon_overload_grad, '%H:%M').time()
    else:
        sunday_afternoon_time_out_overload_grad_dt = None

    num_days = monthrange(datetime.now().year, month_int)[1]
    times = []
    for day in range(1, num_days+1):
        while True:

            if datetime(datetime.now().year, month_int, day).strftime('%A') == "Monday":
                
                if monday_morning_time_in_overload_undergrad_dt == None:
                    monday_morning_in_time_overload_undergrad = ""
                    monday_morning_in_time_overload_undergrad_show = ""
                else:
                    monday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_in_overload_undergrad_dt.hour, monday_morning_time_in_overload_undergrad_dt.minute)
                    monday_morning_in_time_overload_undergrad_hour = monday_morning_time_in_overload_undergrad_dt.hour
                    monday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    monday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, monday_morning_in_time_overload_undergrad_hour, monday_morning_in_time_overload_undergrad_minute)
                    monday_morning_in_time_overload_undergrad_show = monday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if monday_morning_time_out_overload_undergrad_dt == None:
                    monday_morning_out_time_overload_undergrad = ""
                    monday_morning_out_time_overload_undergrad_show = ""
                else:
                    monday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_out_overload_undergrad_dt.hour, monday_morning_time_out_overload_undergrad_dt.minute)
                    monday_morning_out_time_overload_undergrad_hour = monday_morning_time_out_overload_undergrad_dt.hour
                    monday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    monday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, monday_morning_out_time_overload_undergrad_hour, monday_morning_out_time_overload_undergrad_minute)
                    monday_morning_out_time_overload_undergrad_show = monday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if monday_afternoon_time_in_overload_undergrad_dt == None:
                    monday_afternoon_in_time_overload_undergrad = ""
                    monday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    monday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_in_overload_undergrad_dt.hour, monday_afternoon_time_in_overload_undergrad_dt.minute)
                    monday_afternoon_in_time_overload_undergrad_hour = monday_afternoon_time_in_overload_undergrad_dt.hour
                    monday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    monday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, monday_afternoon_in_time_overload_undergrad_hour, monday_afternoon_in_time_overload_undergrad_minute)
                    monday_afternoon_in_time_overload_undergrad_show = monday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if monday_afternoon_time_out_overload_undergrad_dt == None:
                    monday_afternoon_out_time_overload_undergrad = ""
                    monday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    monday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_out_overload_undergrad_dt.hour, monday_afternoon_time_out_overload_undergrad_dt.minute)
                    monday_afternoon_out_time_overload_undergrad_hour = monday_afternoon_time_out_overload_undergrad_dt.hour
                    monday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    monday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, monday_afternoon_out_time_overload_undergrad_hour, monday_afternoon_out_time_overload_undergrad_minute)
                    monday_afternoon_out_time_overload_undergrad_show = monday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if monday_morning_time_in_overload_grad_dt == None:
                    monday_morning_in_time_overload_grad = ""
                    monday_morning_in_time_overload_grad_show = ""
                else:
                    monday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_in_overload_grad_dt.hour, monday_morning_time_in_overload_grad_dt.minute)
                    monday_morning_in_time_overload_grad_hour = monday_morning_time_in_overload_grad_dt.hour
                    monday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    monday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, monday_morning_in_time_overload_grad_hour, monday_morning_in_time_overload_grad_minute)
                    monday_morning_in_time_overload_grad_show = monday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if monday_morning_time_out_overload_grad_dt == None:
                    monday_morning_out_time_overload_grad = ""
                    monday_morning_out_time_overload_grad_show = ""
                else:
                    monday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_out_overload_grad_dt.hour, monday_morning_time_out_overload_grad_dt.minute)
                    monday_morning_out_time_overload_grad_hour = monday_morning_time_out_overload_grad_dt.hour
                    monday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    monday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, monday_morning_out_time_overload_grad_hour, monday_morning_out_time_overload_grad_minute)
                    monday_morning_out_time_overload_grad_show = monday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if monday_afternoon_time_in_overload_grad_dt == None:
                    monday_afternoon_in_time_overload_grad = ""
                    monday_afternoon_in_time_overload_grad_show = ""
                else:
                    monday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_in_overload_grad_dt.hour, monday_afternoon_time_in_overload_grad_dt.minute)
                    monday_afternoon_in_time_overload_grad_hour = monday_afternoon_time_in_overload_grad_dt.hour
                    monday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    monday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, monday_afternoon_in_time_overload_grad_hour, monday_afternoon_in_time_overload_grad_minute)
                    monday_afternoon_in_time_overload_grad_show = monday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if monday_afternoon_time_out_overload_grad_dt == None:
                    monday_afternoon_out_time_overload_grad = ""
                    monday_afternoon_out_time_overload_grad_show = ""
                else:
                    monday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_out_overload_grad_dt.hour, monday_afternoon_time_out_overload_grad_dt.minute)
                    monday_afternoon_out_time_overload_grad_hour = monday_afternoon_time_out_overload_grad_dt.hour
                    monday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    monday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, monday_afternoon_out_time_overload_grad_hour, monday_afternoon_out_time_overload_grad_minute)
                    monday_afternoon_out_time_overload_grad_show = monday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if monday_morning_time_in_dt == None and monday_morning_time_in_overload_undergrad_dt != None:
                    monday_morning_in_time = ""
                    monday_morning_in_time_show = monday_morning_in_time_overload_undergrad_show
                elif monday_morning_time_in_dt == None and monday_morning_time_in_overload_grad_dt != None:
                    monday_morning_in_time = ""
                    monday_morning_in_time_show = monday_morning_in_time_overload_grad_show
                elif monday_morning_time_in_dt != None and monday_morning_time_in_overload_undergrad_dt != None:
                    monday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_in_dt.hour, monday_morning_time_in_dt.minute)
                    monday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_out_dt.hour, monday_morning_time_out_dt.minute)
                    monday_morning_in_hour = random.randint(monday_morning_time_in_dt.hour, monday_morning_time_in_dt.hour)
                    monday_morning_in_minute = random.randint(0, 59)
                    monday_morning_in_time = datetime(datetime.now().year, month_int, day, monday_morning_in_hour, monday_morning_in_minute)
                    if monday_morning_in_time_overload_undergrad_condition < monday_morning_in_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time_overload_undergrad_show
                    elif monday_morning_in_time_overload_undergrad_condition > monday_morning_in_time_condition and monday_morning_in_time_overload_undergrad_condition < monday_morning_out_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time.strftime('%I:%M %p')
                    elif monday_morning_in_time_overload_undergrad_condition > monday_morning_out_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time_overload_undergrad_show
                elif monday_morning_time_in_dt != None and monday_morning_time_in_overload_grad_dt != None:
                    monday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_in_dt.hour, monday_morning_time_in_dt.minute)
                    monday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, monday_morning_time_out_dt.hour, monday_morning_time_out_dt.minute)
                    monday_morning_in_hour = random.randint(monday_morning_time_in_dt.hour, monday_morning_time_in_dt.hour)
                    monday_morning_in_minute = random.randint(0, 59)
                    monday_morning_in_time = datetime(datetime.now().year, month_int, day, monday_morning_in_hour, monday_morning_in_minute)
                    if monday_morning_in_time_overload_grad_condition < monday_morning_in_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time_overload_grad_show
                    elif monday_morning_in_time_overload_grad_condition > monday_morning_in_time_condition and monday_morning_in_time_overload_grad_condition < monday_morning_out_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time.strftime('%I:%M %p')
                    elif monday_morning_in_time_overload_grad_condition > monday_morning_out_time_condition:
                        monday_morning_in_time_show = monday_morning_in_time_overload_grad_show
                elif monday_morning_time_in_dt == None and monday_morning_time_in_overload_undergrad_dt == None:
                    monday_morning_in_time = ""
                    monday_morning_in_time_show = ""
                elif monday_morning_time_in_dt == None and monday_morning_time_in_overload_grad_dt == None:
                    monday_morning_in_time = ""
                    monday_morning_in_time_show = ""
                else:
                    monday_morning_in_hour = random.randint(monday_morning_time_in_dt.hour, monday_morning_time_in_dt.hour)
                    monday_morning_in_minute = random.randint(0, 59)
                    monday_morning_in_time = datetime(datetime.now().year, month_int, day, monday_morning_in_hour, monday_morning_in_minute)
                    monday_morning_in_time_show = monday_morning_in_time.strftime('%I:%M %p')
                

                if monday_morning_time_out_dt != None and monday_morning_time_out_overload_undergrad_dt != None:
                    monday_morning_out_hour = random.randint(monday_morning_time_out_dt.hour, monday_morning_time_out_dt.hour)
                    monday_morning_out_minute = random.randint(0, 59)
                    monday_morning_out_time = datetime(datetime.now().year, month_int, day, monday_morning_out_hour, monday_morning_out_minute)
                    if monday_morning_out_time_overload_undergrad_condition > monday_morning_out_time_condition:
                        monday_morning_out_time_show = monday_morning_out_time_overload_undergrad_show
                    else:
                        monday_morning_out_time_show = monday_morning_out_time.strftime('%I:%M %p')
                elif monday_morning_time_out_dt != None and monday_morning_time_out_overload_grad_dt != None:
                    monday_morning_out_hour = random.randint(monday_morning_time_out_dt.hour, monday_morning_time_out_dt.hour)
                    monday_morning_out_minute = random.randint(0, 59)
                    monday_morning_out_time = datetime(datetime.now().year, month_int, day, monday_morning_out_hour, monday_morning_out_minute)
                    if monday_morning_out_time_overload_grad_condition > monday_morning_out_time_condition:
                        monday_morning_out_time_show = monday_morning_out_time_overload_grad_show
                    else:
                        monday_morning_out_time_show = monday_morning_out_time.strftime('%I:%M %p')

                elif monday_morning_time_out_dt == None and monday_morning_time_out_overload_undergrad_dt == None:
                    monday_morning_out_time = ""
                    monday_morning_out_time_show = ""
                elif monday_morning_time_out_dt == None and monday_morning_time_out_overload_grad_dt == None:
                    monday_morning_out_time = ""
                    monday_morning_out_time_show = ""
      
                else:
                    monday_morning_out_hour = random.randint(monday_morning_time_out_dt.hour, monday_morning_time_out_dt.hour)
                    monday_morning_out_minute = random.randint(0, 59)
                    monday_morning_out_time = datetime(datetime.now().year, month_int, day, monday_morning_out_hour, monday_morning_out_minute)
                    monday_morning_out_time_show = monday_morning_out_time.strftime('%I:%M %p')

                if monday_morning_time_out_dt == None and monday_morning_time_out_overload_undergrad_dt != None:
                    monday_morning_out_time = ""
                    monday_morning_out_time_show = monday_morning_out_time_overload_undergrad_show
                elif monday_morning_time_out_dt == None and monday_morning_time_out_overload_grad_dt != None:
                    monday_morning_out_time = ""
                    monday_morning_out_time_show = monday_morning_out_time_overload_grad_show
                
                if monday_afternoon_time_in_dt == None and monday_afternoon_time_in_overload_undergrad_dt != None:
                    monday_afternoon_in_time = ""
                    monday_afternoon_in_time_show = monday_afternoon_in_time_overload_undergrad_show
                elif monday_afternoon_time_in_dt == None and monday_afternoon_time_in_overload_grad_dt != None:
                    monday_afternoon_in_time = ""
                    monday_afternoon_in_time_show = monday_afternoon_in_time_overload_grad_show
                    
                elif monday_afternoon_time_in_dt != None and monday_afternoon_time_in_overload_undergrad_dt != None:
                    monday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_in_dt.hour, monday_afternoon_time_in_dt.minute)
                    monday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_out_dt.hour, monday_afternoon_time_out_dt.minute)
                    monday_afternoon_in_hour = random.randint(monday_afternoon_time_in_dt.hour, monday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    monday_afternoon_in_minute = random.randint(0, 59)
                    monday_afternoon_in_time = datetime(datetime.now().year, month_int, day, monday_afternoon_in_hour, monday_afternoon_in_minute)                    
                    if monday_afternoon_in_time_overload_undergrad_condition < monday_afternoon_in_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time_overload_undergrad_show
                    elif monday_afternoon_in_time_overload_undergrad_condition > monday_afternoon_in_time_condition and monday_afternoon_in_time_overload_undergrad_condition < monday_afternoon_out_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time.strftime('%I:%M %p')
                    elif monday_afternoon_in_time_overload_undergrad_condition > monday_afternoon_out_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif monday_afternoon_time_in_dt != None and monday_afternoon_time_in_overload_grad_dt != None:
                    monday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_in_dt.hour, monday_afternoon_time_in_dt.minute)
                    monday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, monday_afternoon_time_out_dt.hour, monday_afternoon_time_out_dt.minute)
                    monday_afternoon_in_hour = random.randint(monday_afternoon_time_in_dt.hour, monday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    monday_afternoon_in_minute = random.randint(0, 59)
                    monday_afternoon_in_time = datetime(datetime.now().year, month_int, day, monday_afternoon_in_hour, monday_afternoon_in_minute)                    
                    if monday_afternoon_in_time_overload_grad_condition < monday_afternoon_in_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time_overload_grad_show
                    elif monday_afternoon_in_time_overload_grad_condition > monday_afternoon_in_time_condition and monday_afternoon_in_time_overload_grad_condition < monday_afternoon_out_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time.strftime('%I:%M %p')
                    elif monday_afternoon_in_time_overload_grad_condition > monday_afternoon_out_time_condition:
                        monday_afternoon_in_time_show = monday_afternoon_in_time.strftime('%I:%M %p')
                
                elif monday_afternoon_time_in_dt == None and monday_afternoon_time_in_overload_undergrad_dt == None:
                    monday_afternoon_in_time = ""
                    monday_afternoon_in_time_show = ""
                elif monday_afternoon_time_in_dt == None and monday_afternoon_time_in_overload_grad_dt == None:
                    monday_afternoon_in_time = ""
                    monday_afternoon_in_time_show = ""

                else:
                    monday_afternoon_in_hour = random.randint(monday_afternoon_time_in_dt.hour, monday_afternoon_time_in_dt.hour)
                    monday_afternoon_in_minute = random.randint(0, 59)
                    monday_afternoon_in_time = datetime(datetime.now().year, month_int, day, monday_afternoon_in_hour, monday_afternoon_in_minute)
                    monday_afternoon_in_time_show = monday_afternoon_in_time.strftime('%I:%M %p')
                

                if monday_afternoon_time_out_dt != None and monday_afternoon_time_out_overload_undergrad_dt != None:
                    monday_afternoon_out_hour = random.randint(monday_afternoon_time_out_dt.hour, monday_afternoon_time_out_dt.hour)
                    monday_afternoon_out_minute = random.randint(0, 59)
                    monday_afternoon_out_time = datetime(datetime.now().year, month_int, day, monday_afternoon_out_hour, monday_afternoon_out_minute)
                    if monday_afternoon_out_time_overload_undergrad_condition > monday_afternoon_out_time_condition:
                        monday_afternoon_out_time_show = monday_afternoon_out_time_overload_undergrad_show
                    else:
                        monday_afternoon_out_time_show = monday_afternoon_out_time.strftime('%I:%M %p')

                elif monday_afternoon_time_out_dt != None and monday_afternoon_time_out_overload_grad_dt != None:
                    monday_afternoon_out_hour = random.randint(monday_afternoon_time_out_dt.hour, monday_afternoon_time_out_dt.hour)
                    monday_afternoon_out_minute = random.randint(0, 59)
                    monday_afternoon_out_time = datetime(datetime.now().year, month_int, day, monday_afternoon_out_hour, monday_afternoon_out_minute)
                    if monday_afternoon_out_time_overload_grad_condition > monday_afternoon_out_time_condition:
                        monday_afternoon_out_time_show = monday_afternoon_out_time_overload_grad_show
                    else:
                        monday_afternoon_out_time_show = monday_afternoon_out_time.strftime('%I:%M %p')


                elif monday_afternoon_time_out_dt == None and monday_afternoon_time_out_overload_undergrad_dt == None:
                    monday_afternoon_out_time = ""
                    monday_afternoon_out_time_show = ""
                elif monday_afternoon_time_out_dt == None and monday_afternoon_time_out_overload_grad_dt == None:
                    monday_afternoon_out_time = ""
                    monday_afternoon_out_time_show = ""
                else:
                    monday_afternoon_out_hour = random.randint(monday_afternoon_time_out_dt.hour, monday_afternoon_time_out_dt.hour)
                    monday_afternoon_out_minute = random.randint(0, 59)
                    monday_afternoon_out_time = datetime(datetime.now().year, month_int, day, monday_afternoon_out_hour, monday_afternoon_out_minute)
                    monday_afternoon_out_time_show = monday_afternoon_out_time.strftime('%I:%M %p')

                if monday_afternoon_time_out_dt == None and monday_afternoon_time_out_overload_undergrad_dt != None:
                    monday_afternoon_out_time = ""
                    monday_afternoon_out_time_show = monday_afternoon_out_time_overload_undergrad_show
                elif monday_afternoon_time_out_dt == None and monday_afternoon_time_out_overload_grad_dt != None:
                    monday_afternoon_out_time = ""
                    monday_afternoon_out_time_show = monday_afternoon_out_time_overload_grad_show


                if monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    monday_morning_in_time_show,
                    monday_morning_out_time_show,
                    monday_afternoon_in_time_show,
                    monday_afternoon_out_time_show,
                    monday_morning_in_time_overload_undergrad_show,
                    monday_morning_out_time_overload_undergrad_show,
                    monday_afternoon_in_time_overload_undergrad_show,
                    monday_afternoon_out_time_overload_undergrad_show,
                    monday_morning_in_time_overload_grad_show,
                    monday_morning_out_time_overload_grad_show,
                    monday_afternoon_in_time_overload_grad_show,
                    monday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time != "" and monday_morning_out_time != "" and monday_afternoon_in_time != "" and monday_afternoon_out_time != "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad != "" and monday_morning_out_time_overload_undergrad != "" and monday_afternoon_in_time_overload_undergrad != "" and monday_afternoon_out_time_overload_undergrad != "" \
                    and monday_morning_in_time_overload_grad == "" and monday_morning_out_time_overload_grad == "" and monday_afternoon_in_time_overload_grad == "" and monday_afternoon_out_time_overload_grad == "":
                    if abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif monday_morning_in_time == "" and monday_morning_out_time == "" and monday_afternoon_in_time == "" and monday_afternoon_out_time == "" \
                    and monday_morning_in_time_overload_undergrad == "" and monday_morning_out_time_overload_undergrad == "" and monday_afternoon_in_time_overload_undergrad == "" and monday_afternoon_out_time_overload_undergrad == "" \
                    and monday_morning_in_time_overload_grad != "" and monday_morning_out_time_overload_grad != "" and monday_afternoon_in_time_overload_grad != "" and monday_afternoon_out_time_overload_grad != "":
                    if abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            monday_morning_in_time_show,
                            monday_morning_out_time_show,
                            monday_afternoon_in_time_show,
                            monday_afternoon_out_time_show,
                            monday_morning_in_time_overload_undergrad_show,
                            monday_morning_out_time_overload_undergrad_show,
                            monday_afternoon_in_time_overload_undergrad_show,
                            monday_afternoon_out_time_overload_undergrad_show,
                            monday_morning_in_time_overload_grad_show,
                            monday_morning_out_time_overload_grad_show,
                            monday_afternoon_in_time_overload_grad_show,
                            monday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((monday_morning_in_time - datetime.combine(monday_morning_in_time.date(), monday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((monday_morning_out_time - datetime.combine(monday_morning_out_time.date(), monday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((monday_morning_in_time_overload_grad - datetime.combine(monday_morning_in_time_overload_grad.date(), monday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((monday_morning_out_time_overload_grad - datetime.combine(monday_morning_out_time_overload_grad.date(), monday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((monday_morning_in_time_overload_undergrad - datetime.combine(monday_morning_in_time_overload_undergrad.date(), monday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((monday_morning_out_time_overload_undergrad - datetime.combine(monday_morning_out_time_overload_undergrad.date(), monday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_in_time - datetime.combine(monday_afternoon_in_time.date(), monday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_out_time - datetime.combine(monday_afternoon_out_time.date(), monday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_in_time_overload_grad - datetime.combine(monday_afternoon_in_time_overload_grad.date(), monday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_out_time_overload_grad - datetime.combine(monday_afternoon_out_time_overload_grad.date(), monday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_in_time_overload_undergrad - datetime.combine(monday_afternoon_in_time_overload_undergrad.date(), monday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((monday_afternoon_out_time_overload_undergrad - datetime.combine(monday_afternoon_out_time_overload_undergrad.date(), monday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                monday_morning_in_time_show,
                                monday_morning_out_time_show,
                                monday_afternoon_in_time_show,
                                monday_afternoon_out_time_show,
                                monday_morning_in_time_overload_undergrad_show,
                                monday_morning_out_time_overload_undergrad_show,
                                monday_afternoon_in_time_overload_undergrad_show,
                                monday_afternoon_out_time_overload_undergrad_show,
                                monday_morning_in_time_overload_grad_show,
                                monday_morning_out_time_overload_grad_show,
                                monday_afternoon_in_time_overload_grad_show,
                                monday_afternoon_out_time_overload_grad_show
                            ))
                            break

            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Tuesday":
                
                if tuesday_morning_time_in_overload_undergrad_dt == None:
                    tuesday_morning_in_time_overload_undergrad = ""
                    tuesday_morning_in_time_overload_undergrad_show = ""
                else:
                    tuesday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_in_overload_undergrad_dt.hour, tuesday_morning_time_in_overload_undergrad_dt.minute)
                    tuesday_morning_in_time_overload_undergrad_hour = tuesday_morning_time_in_overload_undergrad_dt.hour
                    tuesday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    tuesday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, tuesday_morning_in_time_overload_undergrad_hour, tuesday_morning_in_time_overload_undergrad_minute)
                    tuesday_morning_in_time_overload_undergrad_show = tuesday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if tuesday_morning_time_out_overload_undergrad_dt == None:
                    tuesday_morning_out_time_overload_undergrad = ""
                    tuesday_morning_out_time_overload_undergrad_show = ""
                else:
                    tuesday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_out_overload_undergrad_dt.hour, tuesday_morning_time_out_overload_undergrad_dt.minute)
                    tuesday_morning_out_time_overload_undergrad_hour = tuesday_morning_time_out_overload_undergrad_dt.hour
                    tuesday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    tuesday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, tuesday_morning_out_time_overload_undergrad_hour, tuesday_morning_out_time_overload_undergrad_minute)
                    tuesday_morning_out_time_overload_undergrad_show = tuesday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if tuesday_afternoon_time_in_overload_undergrad_dt == None:
                    tuesday_afternoon_in_time_overload_undergrad = ""
                    tuesday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    tuesday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_in_overload_undergrad_dt.hour, tuesday_afternoon_time_in_overload_undergrad_dt.minute)
                    tuesday_afternoon_in_time_overload_undergrad_hour = tuesday_afternoon_time_in_overload_undergrad_dt.hour
                    tuesday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    tuesday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, tuesday_afternoon_in_time_overload_undergrad_hour, tuesday_afternoon_in_time_overload_undergrad_minute)
                    tuesday_afternoon_in_time_overload_undergrad_show = tuesday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if tuesday_afternoon_time_out_overload_undergrad_dt == None:
                    tuesday_afternoon_out_time_overload_undergrad = ""
                    tuesday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    tuesday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_out_overload_undergrad_dt.hour, tuesday_afternoon_time_out_overload_undergrad_dt.minute)
                    tuesday_afternoon_out_time_overload_undergrad_hour = tuesday_afternoon_time_out_overload_undergrad_dt.hour
                    tuesday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    tuesday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, tuesday_afternoon_out_time_overload_undergrad_hour, tuesday_afternoon_out_time_overload_undergrad_minute)
                    tuesday_afternoon_out_time_overload_undergrad_show = tuesday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if tuesday_morning_time_in_overload_grad_dt == None:
                    tuesday_morning_in_time_overload_grad = ""
                    tuesday_morning_in_time_overload_grad_show = ""
                else:
                    tuesday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_in_overload_grad_dt.hour, tuesday_morning_time_in_overload_grad_dt.minute)
                    tuesday_morning_in_time_overload_grad_hour = tuesday_morning_time_in_overload_grad_dt.hour
                    tuesday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    tuesday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, tuesday_morning_in_time_overload_grad_hour, tuesday_morning_in_time_overload_grad_minute)
                    tuesday_morning_in_time_overload_grad_show = tuesday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if tuesday_morning_time_out_overload_grad_dt == None:
                    tuesday_morning_out_time_overload_grad = ""
                    tuesday_morning_out_time_overload_grad_show = ""
                else:
                    tuesday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_out_overload_grad_dt.hour, tuesday_morning_time_out_overload_grad_dt.minute)
                    tuesday_morning_out_time_overload_grad_hour = tuesday_morning_time_out_overload_grad_dt.hour
                    tuesday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    tuesday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, tuesday_morning_out_time_overload_grad_hour, tuesday_morning_out_time_overload_grad_minute)
                    tuesday_morning_out_time_overload_grad_show = tuesday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if tuesday_afternoon_time_in_overload_grad_dt == None:
                    tuesday_afternoon_in_time_overload_grad = ""
                    tuesday_afternoon_in_time_overload_grad_show = ""
                else:
                    tuesday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_in_overload_grad_dt.hour, tuesday_afternoon_time_in_overload_grad_dt.minute)
                    tuesday_afternoon_in_time_overload_grad_hour = tuesday_afternoon_time_in_overload_grad_dt.hour
                    tuesday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    tuesday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, tuesday_afternoon_in_time_overload_grad_hour, tuesday_afternoon_in_time_overload_grad_minute)
                    tuesday_afternoon_in_time_overload_grad_show = tuesday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if tuesday_afternoon_time_out_overload_grad_dt == None:
                    tuesday_afternoon_out_time_overload_grad = ""
                    tuesday_afternoon_out_time_overload_grad_show = ""
                else:
                    tuesday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_out_overload_grad_dt.hour, tuesday_afternoon_time_out_overload_grad_dt.minute)
                    tuesday_afternoon_out_time_overload_grad_hour = tuesday_afternoon_time_out_overload_grad_dt.hour
                    tuesday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    tuesday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, tuesday_afternoon_out_time_overload_grad_hour, tuesday_afternoon_out_time_overload_grad_minute)
                    tuesday_afternoon_out_time_overload_grad_show = tuesday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if tuesday_morning_time_in_dt == None and tuesday_morning_time_in_overload_undergrad_dt != None:
                    tuesday_morning_in_time = ""
                    tuesday_morning_in_time_show = tuesday_morning_in_time_overload_undergrad_show
                elif tuesday_morning_time_in_dt == None and tuesday_morning_time_in_overload_grad_dt != None:
                    tuesday_morning_in_time = ""
                    tuesday_morning_in_time_show = tuesday_morning_in_time_overload_grad_show
                elif tuesday_morning_time_in_dt != None and tuesday_morning_time_in_overload_undergrad_dt != None:
                    tuesday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_in_dt.hour, tuesday_morning_time_in_dt.minute)
                    tuesday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_out_dt.hour, tuesday_morning_time_out_dt.minute)
                    tuesday_morning_in_hour = random.randint(tuesday_morning_time_in_dt.hour, tuesday_morning_time_in_dt.hour)
                    tuesday_morning_in_minute = random.randint(0, 59)
                    tuesday_morning_in_time = datetime(datetime.now().year, month_int, day, tuesday_morning_in_hour, tuesday_morning_in_minute)
                    if tuesday_morning_in_time_overload_undergrad_condition < tuesday_morning_in_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time_overload_undergrad_show
                    elif tuesday_morning_in_time_overload_undergrad_condition > tuesday_morning_in_time_condition and tuesday_morning_in_time_overload_undergrad_condition < tuesday_morning_out_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time.strftime('%I:%M %p')
                    elif tuesday_morning_in_time_overload_undergrad_condition > tuesday_morning_out_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time_overload_undergrad_show
                elif tuesday_morning_time_in_dt != None and tuesday_morning_time_in_overload_grad_dt != None:
                    tuesday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_in_dt.hour, tuesday_morning_time_in_dt.minute)
                    tuesday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, tuesday_morning_time_out_dt.hour, tuesday_morning_time_out_dt.minute)
                    tuesday_morning_in_hour = random.randint(tuesday_morning_time_in_dt.hour, tuesday_morning_time_in_dt.hour)
                    tuesday_morning_in_minute = random.randint(0, 59)
                    tuesday_morning_in_time = datetime(datetime.now().year, month_int, day, tuesday_morning_in_hour, tuesday_morning_in_minute)
                    if tuesday_morning_in_time_overload_grad_condition < tuesday_morning_in_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time_overload_grad_show
                    elif tuesday_morning_in_time_overload_grad_condition > tuesday_morning_in_time_condition and tuesday_morning_in_time_overload_grad_condition < tuesday_morning_out_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time.strftime('%I:%M %p')
                    elif tuesday_morning_in_time_overload_grad_condition > tuesday_morning_out_time_condition:
                        tuesday_morning_in_time_show = tuesday_morning_in_time_overload_grad_show
                elif tuesday_morning_time_in_dt == None and tuesday_morning_time_in_overload_undergrad_dt == None:
                    tuesday_morning_in_time = ""
                    tuesday_morning_in_time_show = ""
                elif tuesday_morning_time_in_dt == None and tuesday_morning_time_in_overload_grad_dt == None:
                    tuesday_morning_in_time = ""
                    tuesday_morning_in_time_show = ""
                else:
                    tuesday_morning_in_hour = random.randint(tuesday_morning_time_in_dt.hour, tuesday_morning_time_in_dt.hour)
                    tuesday_morning_in_minute = random.randint(0, 59)
                    tuesday_morning_in_time = datetime(datetime.now().year, month_int, day, tuesday_morning_in_hour, tuesday_morning_in_minute)
                    tuesday_morning_in_time_show = tuesday_morning_in_time.strftime('%I:%M %p')
                

                if tuesday_morning_time_out_dt != None and tuesday_morning_time_out_overload_undergrad_dt != None:
                    tuesday_morning_out_hour = random.randint(tuesday_morning_time_out_dt.hour, tuesday_morning_time_out_dt.hour)
                    tuesday_morning_out_minute = random.randint(0, 59)
                    tuesday_morning_out_time = datetime(datetime.now().year, month_int, day, tuesday_morning_out_hour, tuesday_morning_out_minute)
                    if tuesday_morning_out_time_overload_undergrad_condition > tuesday_morning_out_time_condition:
                        tuesday_morning_out_time_show = tuesday_morning_out_time_overload_undergrad_show
                    else:
                        tuesday_morning_out_time_show = tuesday_morning_out_time.strftime('%I:%M %p')
                elif tuesday_morning_time_out_dt != None and tuesday_morning_time_out_overload_grad_dt != None:
                    tuesday_morning_out_hour = random.randint(tuesday_morning_time_out_dt.hour, tuesday_morning_time_out_dt.hour)
                    tuesday_morning_out_minute = random.randint(0, 59)
                    tuesday_morning_out_time = datetime(datetime.now().year, month_int, day, tuesday_morning_out_hour, tuesday_morning_out_minute)
                    if tuesday_morning_out_time_overload_grad_condition > tuesday_morning_out_time_condition:
                        tuesday_morning_out_time_show = tuesday_morning_out_time_overload_grad_show
                    else:
                        tuesday_morning_out_time_show = tuesday_morning_out_time.strftime('%I:%M %p')

                elif tuesday_morning_time_out_dt == None and tuesday_morning_time_out_overload_undergrad_dt == None:
                    tuesday_morning_out_time = ""
                    tuesday_morning_out_time_show = ""
                elif tuesday_morning_time_out_dt == None and tuesday_morning_time_out_overload_grad_dt == None:
                    tuesday_morning_out_time = ""
                    tuesday_morning_out_time_show = ""
      
                else:
                    tuesday_morning_out_hour = random.randint(tuesday_morning_time_out_dt.hour, tuesday_morning_time_out_dt.hour)
                    tuesday_morning_out_minute = random.randint(0, 59)
                    tuesday_morning_out_time = datetime(datetime.now().year, month_int, day, tuesday_morning_out_hour, tuesday_morning_out_minute)
                    tuesday_morning_out_time_show = tuesday_morning_out_time.strftime('%I:%M %p')

                if tuesday_morning_time_out_dt == None and tuesday_morning_time_out_overload_undergrad_dt != None:
                    tuesday_morning_out_time = ""
                    tuesday_morning_out_time_show = tuesday_morning_out_time_overload_undergrad_show
                elif tuesday_morning_time_out_dt == None and tuesday_morning_time_out_overload_grad_dt != None:
                    tuesday_morning_out_time = ""
                    tuesday_morning_out_time_show = tuesday_morning_out_time_overload_grad_show
                
                if tuesday_afternoon_time_in_dt == None and tuesday_afternoon_time_in_overload_undergrad_dt != None:
                    tuesday_afternoon_in_time = ""
                    tuesday_afternoon_in_time_show = tuesday_afternoon_in_time_overload_undergrad_show
                elif tuesday_afternoon_time_in_dt == None and tuesday_afternoon_time_in_overload_grad_dt != None:
                    tuesday_afternoon_in_time = ""
                    tuesday_afternoon_in_time_show = tuesday_afternoon_in_time_overload_grad_show
                    
                elif tuesday_afternoon_time_in_dt != None and tuesday_afternoon_time_in_overload_undergrad_dt != None:
                    tuesday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_in_dt.hour, tuesday_afternoon_time_in_dt.minute)
                    tuesday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_out_dt.hour, tuesday_afternoon_time_out_dt.minute)
                    tuesday_afternoon_in_hour = random.randint(tuesday_afternoon_time_in_dt.hour, tuesday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    tuesday_afternoon_in_minute = random.randint(0, 59)
                    tuesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_in_hour, tuesday_afternoon_in_minute)                    
                    if tuesday_afternoon_in_time_overload_undergrad_condition < tuesday_afternoon_in_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time_overload_undergrad_show
                    elif tuesday_afternoon_in_time_overload_undergrad_condition > tuesday_afternoon_in_time_condition and tuesday_afternoon_in_time_overload_undergrad_condition < tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time.strftime('%I:%M %p')
                    elif tuesday_afternoon_in_time_overload_undergrad_condition > tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif tuesday_afternoon_time_in_dt != None and tuesday_afternoon_time_in_overload_grad_dt != None:
                    tuesday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_in_dt.hour, tuesday_afternoon_time_in_dt.minute)
                    tuesday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, tuesday_afternoon_time_out_dt.hour, tuesday_afternoon_time_out_dt.minute)
                    tuesday_afternoon_in_hour = random.randint(tuesday_afternoon_time_in_dt.hour, tuesday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    tuesday_afternoon_in_minute = random.randint(0, 59)
                    tuesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_in_hour, tuesday_afternoon_in_minute)                    
                    if tuesday_afternoon_in_time_overload_grad_condition < tuesday_afternoon_in_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time_overload_grad_show
                    elif tuesday_afternoon_in_time_overload_grad_condition > tuesday_afternoon_in_time_condition and tuesday_afternoon_in_time_overload_grad_condition < tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time.strftime('%I:%M %p')
                    elif tuesday_afternoon_in_time_overload_grad_condition > tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_in_time_show = tuesday_afternoon_in_time.strftime('%I:%M %p')
                
                elif tuesday_afternoon_time_in_dt == None and tuesday_afternoon_time_in_overload_undergrad_dt == None:
                    tuesday_afternoon_in_time = ""
                    tuesday_afternoon_in_time_show = ""
                elif tuesday_afternoon_time_in_dt == None and tuesday_afternoon_time_in_overload_grad_dt == None:
                    tuesday_afternoon_in_time = ""
                    tuesday_afternoon_in_time_show = ""

                else:
                    tuesday_afternoon_in_hour = random.randint(tuesday_afternoon_time_in_dt.hour, tuesday_afternoon_time_in_dt.hour)
                    tuesday_afternoon_in_minute = random.randint(0, 59)
                    tuesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_in_hour, tuesday_afternoon_in_minute)
                    tuesday_afternoon_in_time_show = tuesday_afternoon_in_time.strftime('%I:%M %p')
                

                if tuesday_afternoon_time_out_dt != None and tuesday_afternoon_time_out_overload_undergrad_dt != None:
                    tuesday_afternoon_out_hour = random.randint(tuesday_afternoon_time_out_dt.hour, tuesday_afternoon_time_out_dt.hour)
                    tuesday_afternoon_out_minute = random.randint(0, 59)
                    tuesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_out_hour, tuesday_afternoon_out_minute)
                    if tuesday_afternoon_out_time_overload_undergrad_condition > tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_out_time_show = tuesday_afternoon_out_time_overload_undergrad_show
                    else:
                        tuesday_afternoon_out_time_show = tuesday_afternoon_out_time.strftime('%I:%M %p')

                elif tuesday_afternoon_time_out_dt != None and tuesday_afternoon_time_out_overload_grad_dt != None:
                    tuesday_afternoon_out_hour = random.randint(tuesday_afternoon_time_out_dt.hour, tuesday_afternoon_time_out_dt.hour)
                    tuesday_afternoon_out_minute = random.randint(0, 59)
                    tuesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_out_hour, tuesday_afternoon_out_minute)
                    if tuesday_afternoon_out_time_overload_grad_condition > tuesday_afternoon_out_time_condition:
                        tuesday_afternoon_out_time_show = tuesday_afternoon_out_time_overload_grad_show
                    else:
                        tuesday_afternoon_out_time_show = tuesday_afternoon_out_time.strftime('%I:%M %p')


                elif tuesday_afternoon_time_out_dt == None and tuesday_afternoon_time_out_overload_undergrad_dt == None:
                    tuesday_afternoon_out_time = ""
                    tuesday_afternoon_out_time_show = ""
                elif tuesday_afternoon_time_out_dt == None and tuesday_afternoon_time_out_overload_grad_dt == None:
                    tuesday_afternoon_out_time = ""
                    tuesday_afternoon_out_time_show = ""
                else:
                    tuesday_afternoon_out_hour = random.randint(tuesday_afternoon_time_out_dt.hour, tuesday_afternoon_time_out_dt.hour)
                    tuesday_afternoon_out_minute = random.randint(0, 59)
                    tuesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, tuesday_afternoon_out_hour, tuesday_afternoon_out_minute)
                    tuesday_afternoon_out_time_show = tuesday_afternoon_out_time.strftime('%I:%M %p')

                if tuesday_afternoon_time_out_dt == None and tuesday_afternoon_time_out_overload_undergrad_dt != None:
                    tuesday_afternoon_out_time = ""
                    tuesday_afternoon_out_time_show = tuesday_afternoon_out_time_overload_undergrad_show
                elif tuesday_afternoon_time_out_dt == None and tuesday_afternoon_time_out_overload_grad_dt != None:
                    tuesday_afternoon_out_time = ""
                    tuesday_afternoon_out_time_show = tuesday_afternoon_out_time_overload_grad_show


                if tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    tuesday_morning_in_time_show,
                    tuesday_morning_out_time_show,
                    tuesday_afternoon_in_time_show,
                    tuesday_afternoon_out_time_show,
                    tuesday_morning_in_time_overload_undergrad_show,
                    tuesday_morning_out_time_overload_undergrad_show,
                    tuesday_afternoon_in_time_overload_undergrad_show,
                    tuesday_afternoon_out_time_overload_undergrad_show,
                    tuesday_morning_in_time_overload_grad_show,
                    tuesday_morning_out_time_overload_grad_show,
                    tuesday_afternoon_in_time_overload_grad_show,
                    tuesday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time != "" and tuesday_morning_out_time != "" and tuesday_afternoon_in_time != "" and tuesday_afternoon_out_time != "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad != "" and tuesday_morning_out_time_overload_undergrad != "" and tuesday_afternoon_in_time_overload_undergrad != "" and tuesday_afternoon_out_time_overload_undergrad != "" \
                    and tuesday_morning_in_time_overload_grad == "" and tuesday_morning_out_time_overload_grad == "" and tuesday_afternoon_in_time_overload_grad == "" and tuesday_afternoon_out_time_overload_grad == "":
                    if abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif tuesday_morning_in_time == "" and tuesday_morning_out_time == "" and tuesday_afternoon_in_time == "" and tuesday_afternoon_out_time == "" \
                    and tuesday_morning_in_time_overload_undergrad == "" and tuesday_morning_out_time_overload_undergrad == "" and tuesday_afternoon_in_time_overload_undergrad == "" and tuesday_afternoon_out_time_overload_undergrad == "" \
                    and tuesday_morning_in_time_overload_grad != "" and tuesday_morning_out_time_overload_grad != "" and tuesday_afternoon_in_time_overload_grad != "" and tuesday_afternoon_out_time_overload_grad != "":
                    if abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            tuesday_morning_in_time_show,
                            tuesday_morning_out_time_show,
                            tuesday_afternoon_in_time_show,
                            tuesday_afternoon_out_time_show,
                            tuesday_morning_in_time_overload_undergrad_show,
                            tuesday_morning_out_time_overload_undergrad_show,
                            tuesday_afternoon_in_time_overload_undergrad_show,
                            tuesday_afternoon_out_time_overload_undergrad_show,
                            tuesday_morning_in_time_overload_grad_show,
                            tuesday_morning_out_time_overload_grad_show,
                            tuesday_afternoon_in_time_overload_grad_show,
                            tuesday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((tuesday_morning_in_time - datetime.combine(tuesday_morning_in_time.date(), tuesday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_morning_out_time - datetime.combine(tuesday_morning_out_time.date(), tuesday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_morning_in_time_overload_grad - datetime.combine(tuesday_morning_in_time_overload_grad.date(), tuesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_morning_out_time_overload_grad - datetime.combine(tuesday_morning_out_time_overload_grad.date(), tuesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_morning_in_time_overload_undergrad - datetime.combine(tuesday_morning_in_time_overload_undergrad.date(), tuesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_morning_out_time_overload_undergrad - datetime.combine(tuesday_morning_out_time_overload_undergrad.date(), tuesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_in_time - datetime.combine(tuesday_afternoon_in_time.date(), tuesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_out_time - datetime.combine(tuesday_afternoon_out_time.date(), tuesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_in_time_overload_grad - datetime.combine(tuesday_afternoon_in_time_overload_grad.date(), tuesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_out_time_overload_grad - datetime.combine(tuesday_afternoon_out_time_overload_grad.date(), tuesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_in_time_overload_undergrad - datetime.combine(tuesday_afternoon_in_time_overload_undergrad.date(), tuesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((tuesday_afternoon_out_time_overload_undergrad - datetime.combine(tuesday_afternoon_out_time_overload_undergrad.date(), tuesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                tuesday_morning_in_time_show,
                                tuesday_morning_out_time_show,
                                tuesday_afternoon_in_time_show,
                                tuesday_afternoon_out_time_show,
                                tuesday_morning_in_time_overload_undergrad_show,
                                tuesday_morning_out_time_overload_undergrad_show,
                                tuesday_afternoon_in_time_overload_undergrad_show,
                                tuesday_afternoon_out_time_overload_undergrad_show,
                                tuesday_morning_in_time_overload_grad_show,
                                tuesday_morning_out_time_overload_grad_show,
                                tuesday_afternoon_in_time_overload_grad_show,
                                tuesday_afternoon_out_time_overload_grad_show
                            ))
                            break
                
            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Wednesday":
                
                if wednesday_morning_time_in_overload_undergrad_dt == None:
                    wednesday_morning_in_time_overload_undergrad = ""
                    wednesday_morning_in_time_overload_undergrad_show = ""
                else:
                    wednesday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_in_overload_undergrad_dt.hour, wednesday_morning_time_in_overload_undergrad_dt.minute)
                    wednesday_morning_in_time_overload_undergrad_hour = wednesday_morning_time_in_overload_undergrad_dt.hour
                    wednesday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    wednesday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, wednesday_morning_in_time_overload_undergrad_hour, wednesday_morning_in_time_overload_undergrad_minute)
                    wednesday_morning_in_time_overload_undergrad_show = wednesday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if wednesday_morning_time_out_overload_undergrad_dt == None:
                    wednesday_morning_out_time_overload_undergrad = ""
                    wednesday_morning_out_time_overload_undergrad_show = ""
                else:
                    wednesday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_out_overload_undergrad_dt.hour, wednesday_morning_time_out_overload_undergrad_dt.minute)
                    wednesday_morning_out_time_overload_undergrad_hour = wednesday_morning_time_out_overload_undergrad_dt.hour
                    wednesday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    wednesday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, wednesday_morning_out_time_overload_undergrad_hour, wednesday_morning_out_time_overload_undergrad_minute)
                    wednesday_morning_out_time_overload_undergrad_show = wednesday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if wednesday_afternoon_time_in_overload_undergrad_dt == None:
                    wednesday_afternoon_in_time_overload_undergrad = ""
                    wednesday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    wednesday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_in_overload_undergrad_dt.hour, wednesday_afternoon_time_in_overload_undergrad_dt.minute)
                    wednesday_afternoon_in_time_overload_undergrad_hour = wednesday_afternoon_time_in_overload_undergrad_dt.hour
                    wednesday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    wednesday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, wednesday_afternoon_in_time_overload_undergrad_hour, wednesday_afternoon_in_time_overload_undergrad_minute)
                    wednesday_afternoon_in_time_overload_undergrad_show = wednesday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if wednesday_afternoon_time_out_overload_undergrad_dt == None:
                    wednesday_afternoon_out_time_overload_undergrad = ""
                    wednesday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    wednesday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_out_overload_undergrad_dt.hour, wednesday_afternoon_time_out_overload_undergrad_dt.minute)
                    wednesday_afternoon_out_time_overload_undergrad_hour = wednesday_afternoon_time_out_overload_undergrad_dt.hour
                    wednesday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    wednesday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, wednesday_afternoon_out_time_overload_undergrad_hour, wednesday_afternoon_out_time_overload_undergrad_minute)
                    wednesday_afternoon_out_time_overload_undergrad_show = wednesday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if wednesday_morning_time_in_overload_grad_dt == None:
                    wednesday_morning_in_time_overload_grad = ""
                    wednesday_morning_in_time_overload_grad_show = ""
                else:
                    wednesday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_in_overload_grad_dt.hour, wednesday_morning_time_in_overload_grad_dt.minute)
                    wednesday_morning_in_time_overload_grad_hour = wednesday_morning_time_in_overload_grad_dt.hour
                    wednesday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    wednesday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, wednesday_morning_in_time_overload_grad_hour, wednesday_morning_in_time_overload_grad_minute)
                    wednesday_morning_in_time_overload_grad_show = wednesday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if wednesday_morning_time_out_overload_grad_dt == None:
                    wednesday_morning_out_time_overload_grad = ""
                    wednesday_morning_out_time_overload_grad_show = ""
                else:
                    wednesday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_out_overload_grad_dt.hour, wednesday_morning_time_out_overload_grad_dt.minute)
                    wednesday_morning_out_time_overload_grad_hour = wednesday_morning_time_out_overload_grad_dt.hour
                    wednesday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    wednesday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, wednesday_morning_out_time_overload_grad_hour, wednesday_morning_out_time_overload_grad_minute)
                    wednesday_morning_out_time_overload_grad_show = wednesday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if wednesday_afternoon_time_in_overload_grad_dt == None:
                    wednesday_afternoon_in_time_overload_grad = ""
                    wednesday_afternoon_in_time_overload_grad_show = ""
                else:
                    wednesday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_in_overload_grad_dt.hour, wednesday_afternoon_time_in_overload_grad_dt.minute)
                    wednesday_afternoon_in_time_overload_grad_hour = wednesday_afternoon_time_in_overload_grad_dt.hour
                    wednesday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    wednesday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, wednesday_afternoon_in_time_overload_grad_hour, wednesday_afternoon_in_time_overload_grad_minute)
                    wednesday_afternoon_in_time_overload_grad_show = wednesday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if wednesday_afternoon_time_out_overload_grad_dt == None:
                    wednesday_afternoon_out_time_overload_grad = ""
                    wednesday_afternoon_out_time_overload_grad_show = ""
                else:
                    wednesday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_out_overload_grad_dt.hour, wednesday_afternoon_time_out_overload_grad_dt.minute)
                    wednesday_afternoon_out_time_overload_grad_hour = wednesday_afternoon_time_out_overload_grad_dt.hour
                    wednesday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    wednesday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, wednesday_afternoon_out_time_overload_grad_hour, wednesday_afternoon_out_time_overload_grad_minute)
                    wednesday_afternoon_out_time_overload_grad_show = wednesday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if wednesday_morning_time_in_dt == None and wednesday_morning_time_in_overload_undergrad_dt != None:
                    wednesday_morning_in_time = ""
                    wednesday_morning_in_time_show = wednesday_morning_in_time_overload_undergrad_show
                elif wednesday_morning_time_in_dt == None and wednesday_morning_time_in_overload_grad_dt != None:
                    wednesday_morning_in_time = ""
                    wednesday_morning_in_time_show = wednesday_morning_in_time_overload_grad_show
                elif wednesday_morning_time_in_dt != None and wednesday_morning_time_in_overload_undergrad_dt != None:
                    wednesday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_in_dt.hour, wednesday_morning_time_in_dt.minute)
                    wednesday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_out_dt.hour, wednesday_morning_time_out_dt.minute)
                    wednesday_morning_in_hour = random.randint(wednesday_morning_time_in_dt.hour, wednesday_morning_time_in_dt.hour)
                    wednesday_morning_in_minute = random.randint(0, 59)
                    wednesday_morning_in_time = datetime(datetime.now().year, month_int, day, wednesday_morning_in_hour, wednesday_morning_in_minute)
                    if wednesday_morning_in_time_overload_undergrad_condition < wednesday_morning_in_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time_overload_undergrad_show
                    elif wednesday_morning_in_time_overload_undergrad_condition > wednesday_morning_in_time_condition and wednesday_morning_in_time_overload_undergrad_condition < wednesday_morning_out_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time.strftime('%I:%M %p')
                    elif wednesday_morning_in_time_overload_undergrad_condition > wednesday_morning_out_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time_overload_undergrad_show
                elif wednesday_morning_time_in_dt != None and wednesday_morning_time_in_overload_grad_dt != None:
                    wednesday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_in_dt.hour, wednesday_morning_time_in_dt.minute)
                    wednesday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, wednesday_morning_time_out_dt.hour, wednesday_morning_time_out_dt.minute)
                    wednesday_morning_in_hour = random.randint(wednesday_morning_time_in_dt.hour, wednesday_morning_time_in_dt.hour)
                    wednesday_morning_in_minute = random.randint(0, 59)
                    wednesday_morning_in_time = datetime(datetime.now().year, month_int, day, wednesday_morning_in_hour, wednesday_morning_in_minute)
                    if wednesday_morning_in_time_overload_grad_condition < wednesday_morning_in_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time_overload_grad_show
                    elif wednesday_morning_in_time_overload_grad_condition > wednesday_morning_in_time_condition and wednesday_morning_in_time_overload_grad_condition < wednesday_morning_out_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time.strftime('%I:%M %p')
                    elif wednesday_morning_in_time_overload_grad_condition > wednesday_morning_out_time_condition:
                        wednesday_morning_in_time_show = wednesday_morning_in_time_overload_grad_show
                elif wednesday_morning_time_in_dt == None and wednesday_morning_time_in_overload_undergrad_dt == None:
                    wednesday_morning_in_time = ""
                    wednesday_morning_in_time_show = ""
                elif wednesday_morning_time_in_dt == None and wednesday_morning_time_in_overload_grad_dt == None:
                    wednesday_morning_in_time = ""
                    wednesday_morning_in_time_show = ""
                else:
                    wednesday_morning_in_hour = random.randint(wednesday_morning_time_in_dt.hour, wednesday_morning_time_in_dt.hour)
                    wednesday_morning_in_minute = random.randint(0, 59)
                    wednesday_morning_in_time = datetime(datetime.now().year, month_int, day, wednesday_morning_in_hour, wednesday_morning_in_minute)
                    wednesday_morning_in_time_show = wednesday_morning_in_time.strftime('%I:%M %p')
                

                if wednesday_morning_time_out_dt != None and wednesday_morning_time_out_overload_undergrad_dt != None:
                    wednesday_morning_out_hour = random.randint(wednesday_morning_time_out_dt.hour, wednesday_morning_time_out_dt.hour)
                    wednesday_morning_out_minute = random.randint(0, 59)
                    wednesday_morning_out_time = datetime(datetime.now().year, month_int, day, wednesday_morning_out_hour, wednesday_morning_out_minute)
                    if wednesday_morning_out_time_overload_undergrad_condition > wednesday_morning_out_time_condition:
                        wednesday_morning_out_time_show = wednesday_morning_out_time_overload_undergrad_show
                    else:
                        wednesday_morning_out_time_show = wednesday_morning_out_time.strftime('%I:%M %p')
                elif wednesday_morning_time_out_dt != None and wednesday_morning_time_out_overload_grad_dt != None:
                    wednesday_morning_out_hour = random.randint(wednesday_morning_time_out_dt.hour, wednesday_morning_time_out_dt.hour)
                    wednesday_morning_out_minute = random.randint(0, 59)
                    wednesday_morning_out_time = datetime(datetime.now().year, month_int, day, wednesday_morning_out_hour, wednesday_morning_out_minute)
                    if wednesday_morning_out_time_overload_grad_condition > wednesday_morning_out_time_condition:
                        wednesday_morning_out_time_show = wednesday_morning_out_time_overload_grad_show
                    else:
                        wednesday_morning_out_time_show = wednesday_morning_out_time.strftime('%I:%M %p')

                elif wednesday_morning_time_out_dt == None and wednesday_morning_time_out_overload_undergrad_dt == None:
                    wednesday_morning_out_time = ""
                    wednesday_morning_out_time_show = ""
                elif wednesday_morning_time_out_dt == None and wednesday_morning_time_out_overload_grad_dt == None:
                    wednesday_morning_out_time = ""
                    wednesday_morning_out_time_show = ""
      
                else:
                    wednesday_morning_out_hour = random.randint(wednesday_morning_time_out_dt.hour, wednesday_morning_time_out_dt.hour)
                    wednesday_morning_out_minute = random.randint(0, 59)
                    wednesday_morning_out_time = datetime(datetime.now().year, month_int, day, wednesday_morning_out_hour, wednesday_morning_out_minute)
                    wednesday_morning_out_time_show = wednesday_morning_out_time.strftime('%I:%M %p')

                if wednesday_morning_time_out_dt == None and wednesday_morning_time_out_overload_undergrad_dt != None:
                    wednesday_morning_out_time = ""
                    wednesday_morning_out_time_show = wednesday_morning_out_time_overload_undergrad_show
                elif wednesday_morning_time_out_dt == None and wednesday_morning_time_out_overload_grad_dt != None:
                    wednesday_morning_out_time = ""
                    wednesday_morning_out_time_show = wednesday_morning_out_time_overload_grad_show
                
                if wednesday_afternoon_time_in_dt == None and wednesday_afternoon_time_in_overload_undergrad_dt != None:
                    wednesday_afternoon_in_time = ""
                    wednesday_afternoon_in_time_show = wednesday_afternoon_in_time_overload_undergrad_show
                elif wednesday_afternoon_time_in_dt == None and wednesday_afternoon_time_in_overload_grad_dt != None:
                    wednesday_afternoon_in_time = ""
                    wednesday_afternoon_in_time_show = wednesday_afternoon_in_time_overload_grad_show
                    
                elif wednesday_afternoon_time_in_dt != None and wednesday_afternoon_time_in_overload_undergrad_dt != None:
                    wednesday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_in_dt.hour, wednesday_afternoon_time_in_dt.minute)
                    wednesday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_out_dt.hour, wednesday_afternoon_time_out_dt.minute)
                    wednesday_afternoon_in_hour = random.randint(wednesday_afternoon_time_in_dt.hour, wednesday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    wednesday_afternoon_in_minute = random.randint(0, 59)
                    wednesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_in_hour, wednesday_afternoon_in_minute)                    
                    if wednesday_afternoon_in_time_overload_undergrad_condition < wednesday_afternoon_in_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time_overload_undergrad_show
                    elif wednesday_afternoon_in_time_overload_undergrad_condition > wednesday_afternoon_in_time_condition and wednesday_afternoon_in_time_overload_undergrad_condition < wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time.strftime('%I:%M %p')
                    elif wednesday_afternoon_in_time_overload_undergrad_condition > wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif wednesday_afternoon_time_in_dt != None and wednesday_afternoon_time_in_overload_grad_dt != None:
                    wednesday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_in_dt.hour, wednesday_afternoon_time_in_dt.minute)
                    wednesday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, wednesday_afternoon_time_out_dt.hour, wednesday_afternoon_time_out_dt.minute)
                    wednesday_afternoon_in_hour = random.randint(wednesday_afternoon_time_in_dt.hour, wednesday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    wednesday_afternoon_in_minute = random.randint(0, 59)
                    wednesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_in_hour, wednesday_afternoon_in_minute)                    
                    if wednesday_afternoon_in_time_overload_grad_condition < wednesday_afternoon_in_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time_overload_grad_show
                    elif wednesday_afternoon_in_time_overload_grad_condition > wednesday_afternoon_in_time_condition and wednesday_afternoon_in_time_overload_grad_condition < wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time.strftime('%I:%M %p')
                    elif wednesday_afternoon_in_time_overload_grad_condition > wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_in_time_show = wednesday_afternoon_in_time.strftime('%I:%M %p')
                
                elif wednesday_afternoon_time_in_dt == None and wednesday_afternoon_time_in_overload_undergrad_dt == None:
                    wednesday_afternoon_in_time = ""
                    wednesday_afternoon_in_time_show = ""
                elif wednesday_afternoon_time_in_dt == None and wednesday_afternoon_time_in_overload_grad_dt == None:
                    wednesday_afternoon_in_time = ""
                    wednesday_afternoon_in_time_show = ""

                else:
                    wednesday_afternoon_in_hour = random.randint(wednesday_afternoon_time_in_dt.hour, wednesday_afternoon_time_in_dt.hour)
                    wednesday_afternoon_in_minute = random.randint(0, 59)
                    wednesday_afternoon_in_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_in_hour, wednesday_afternoon_in_minute)
                    wednesday_afternoon_in_time_show = wednesday_afternoon_in_time.strftime('%I:%M %p')
                

                if wednesday_afternoon_time_out_dt != None and wednesday_afternoon_time_out_overload_undergrad_dt != None:
                    wednesday_afternoon_out_hour = random.randint(wednesday_afternoon_time_out_dt.hour, wednesday_afternoon_time_out_dt.hour)
                    wednesday_afternoon_out_minute = random.randint(0, 59)
                    wednesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_out_hour, wednesday_afternoon_out_minute)
                    if wednesday_afternoon_out_time_overload_undergrad_condition > wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_out_time_show = wednesday_afternoon_out_time_overload_undergrad_show
                    else:
                        wednesday_afternoon_out_time_show = wednesday_afternoon_out_time.strftime('%I:%M %p')

                elif wednesday_afternoon_time_out_dt != None and wednesday_afternoon_time_out_overload_grad_dt != None:
                    wednesday_afternoon_out_hour = random.randint(wednesday_afternoon_time_out_dt.hour, wednesday_afternoon_time_out_dt.hour)
                    wednesday_afternoon_out_minute = random.randint(0, 59)
                    wednesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_out_hour, wednesday_afternoon_out_minute)
                    if wednesday_afternoon_out_time_overload_grad_condition > wednesday_afternoon_out_time_condition:
                        wednesday_afternoon_out_time_show = wednesday_afternoon_out_time_overload_grad_show
                    else:
                        wednesday_afternoon_out_time_show = wednesday_afternoon_out_time.strftime('%I:%M %p')


                elif wednesday_afternoon_time_out_dt == None and wednesday_afternoon_time_out_overload_undergrad_dt == None:
                    wednesday_afternoon_out_time = ""
                    wednesday_afternoon_out_time_show = ""
                elif wednesday_afternoon_time_out_dt == None and wednesday_afternoon_time_out_overload_grad_dt == None:
                    wednesday_afternoon_out_time = ""
                    wednesday_afternoon_out_time_show = ""
                else:
                    wednesday_afternoon_out_hour = random.randint(wednesday_afternoon_time_out_dt.hour, wednesday_afternoon_time_out_dt.hour)
                    wednesday_afternoon_out_minute = random.randint(0, 59)
                    wednesday_afternoon_out_time = datetime(datetime.now().year, month_int, day, wednesday_afternoon_out_hour, wednesday_afternoon_out_minute)
                    wednesday_afternoon_out_time_show = wednesday_afternoon_out_time.strftime('%I:%M %p')

                if wednesday_afternoon_time_out_dt == None and wednesday_afternoon_time_out_overload_undergrad_dt != None:
                    wednesday_afternoon_out_time = ""
                    wednesday_afternoon_out_time_show = wednesday_afternoon_out_time_overload_undergrad_show
                elif wednesday_afternoon_time_out_dt == None and wednesday_afternoon_time_out_overload_grad_dt != None:
                    wednesday_afternoon_out_time = ""
                    wednesday_afternoon_out_time_show = wednesday_afternoon_out_time_overload_grad_show


                if wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    wednesday_morning_in_time_show,
                    wednesday_morning_out_time_show,
                    wednesday_afternoon_in_time_show,
                    wednesday_afternoon_out_time_show,
                    wednesday_morning_in_time_overload_undergrad_show,
                    wednesday_morning_out_time_overload_undergrad_show,
                    wednesday_afternoon_in_time_overload_undergrad_show,
                    wednesday_afternoon_out_time_overload_undergrad_show,
                    wednesday_morning_in_time_overload_grad_show,
                    wednesday_morning_out_time_overload_grad_show,
                    wednesday_afternoon_in_time_overload_grad_show,
                    wednesday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time != "" and wednesday_morning_out_time != "" and wednesday_afternoon_in_time != "" and wednesday_afternoon_out_time != "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad != "" and wednesday_morning_out_time_overload_undergrad != "" and wednesday_afternoon_in_time_overload_undergrad != "" and wednesday_afternoon_out_time_overload_undergrad != "" \
                    and wednesday_morning_in_time_overload_grad == "" and wednesday_morning_out_time_overload_grad == "" and wednesday_afternoon_in_time_overload_grad == "" and wednesday_afternoon_out_time_overload_grad == "":
                    if abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif wednesday_morning_in_time == "" and wednesday_morning_out_time == "" and wednesday_afternoon_in_time == "" and wednesday_afternoon_out_time == "" \
                    and wednesday_morning_in_time_overload_undergrad == "" and wednesday_morning_out_time_overload_undergrad == "" and wednesday_afternoon_in_time_overload_undergrad == "" and wednesday_afternoon_out_time_overload_undergrad == "" \
                    and wednesday_morning_in_time_overload_grad != "" and wednesday_morning_out_time_overload_grad != "" and wednesday_afternoon_in_time_overload_grad != "" and wednesday_afternoon_out_time_overload_grad != "":
                    if abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            wednesday_morning_in_time_show,
                            wednesday_morning_out_time_show,
                            wednesday_afternoon_in_time_show,
                            wednesday_afternoon_out_time_show,
                            wednesday_morning_in_time_overload_undergrad_show,
                            wednesday_morning_out_time_overload_undergrad_show,
                            wednesday_afternoon_in_time_overload_undergrad_show,
                            wednesday_afternoon_out_time_overload_undergrad_show,
                            wednesday_morning_in_time_overload_grad_show,
                            wednesday_morning_out_time_overload_grad_show,
                            wednesday_afternoon_in_time_overload_grad_show,
                            wednesday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((wednesday_morning_in_time - datetime.combine(wednesday_morning_in_time.date(), wednesday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_morning_out_time - datetime.combine(wednesday_morning_out_time.date(), wednesday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_morning_in_time_overload_grad - datetime.combine(wednesday_morning_in_time_overload_grad.date(), wednesday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_morning_out_time_overload_grad - datetime.combine(wednesday_morning_out_time_overload_grad.date(), wednesday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_morning_in_time_overload_undergrad - datetime.combine(wednesday_morning_in_time_overload_undergrad.date(), wednesday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_morning_out_time_overload_undergrad - datetime.combine(wednesday_morning_out_time_overload_undergrad.date(), wednesday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_in_time - datetime.combine(wednesday_afternoon_in_time.date(), wednesday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_out_time - datetime.combine(wednesday_afternoon_out_time.date(), wednesday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_in_time_overload_grad - datetime.combine(wednesday_afternoon_in_time_overload_grad.date(), wednesday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_out_time_overload_grad - datetime.combine(wednesday_afternoon_out_time_overload_grad.date(), wednesday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_in_time_overload_undergrad - datetime.combine(wednesday_afternoon_in_time_overload_undergrad.date(), wednesday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((wednesday_afternoon_out_time_overload_undergrad - datetime.combine(wednesday_afternoon_out_time_overload_undergrad.date(), wednesday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                wednesday_morning_in_time_show,
                                wednesday_morning_out_time_show,
                                wednesday_afternoon_in_time_show,
                                wednesday_afternoon_out_time_show,
                                wednesday_morning_in_time_overload_undergrad_show,
                                wednesday_morning_out_time_overload_undergrad_show,
                                wednesday_afternoon_in_time_overload_undergrad_show,
                                wednesday_afternoon_out_time_overload_undergrad_show,
                                wednesday_morning_in_time_overload_grad_show,
                                wednesday_morning_out_time_overload_grad_show,
                                wednesday_afternoon_in_time_overload_grad_show,
                                wednesday_afternoon_out_time_overload_grad_show
                            ))
                            break
                
            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Thursday":
                
                if thursday_morning_time_in_overload_undergrad_dt == None:
                    thursday_morning_in_time_overload_undergrad = ""
                    thursday_morning_in_time_overload_undergrad_show = ""
                else:
                    thursday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_in_overload_undergrad_dt.hour, thursday_morning_time_in_overload_undergrad_dt.minute)
                    thursday_morning_in_time_overload_undergrad_hour = thursday_morning_time_in_overload_undergrad_dt.hour
                    thursday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    thursday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, thursday_morning_in_time_overload_undergrad_hour, thursday_morning_in_time_overload_undergrad_minute)
                    thursday_morning_in_time_overload_undergrad_show = thursday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if thursday_morning_time_out_overload_undergrad_dt == None:
                    thursday_morning_out_time_overload_undergrad = ""
                    thursday_morning_out_time_overload_undergrad_show = ""
                else:
                    thursday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_out_overload_undergrad_dt.hour, thursday_morning_time_out_overload_undergrad_dt.minute)
                    thursday_morning_out_time_overload_undergrad_hour = thursday_morning_time_out_overload_undergrad_dt.hour
                    thursday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    thursday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, thursday_morning_out_time_overload_undergrad_hour, thursday_morning_out_time_overload_undergrad_minute)
                    thursday_morning_out_time_overload_undergrad_show = thursday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if thursday_afternoon_time_in_overload_undergrad_dt == None:
                    thursday_afternoon_in_time_overload_undergrad = ""
                    thursday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    thursday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_in_overload_undergrad_dt.hour, thursday_afternoon_time_in_overload_undergrad_dt.minute)
                    thursday_afternoon_in_time_overload_undergrad_hour = thursday_afternoon_time_in_overload_undergrad_dt.hour
                    thursday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    thursday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, thursday_afternoon_in_time_overload_undergrad_hour, thursday_afternoon_in_time_overload_undergrad_minute)
                    thursday_afternoon_in_time_overload_undergrad_show = thursday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if thursday_afternoon_time_out_overload_undergrad_dt == None:
                    thursday_afternoon_out_time_overload_undergrad = ""
                    thursday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    thursday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_out_overload_undergrad_dt.hour, thursday_afternoon_time_out_overload_undergrad_dt.minute)
                    thursday_afternoon_out_time_overload_undergrad_hour = thursday_afternoon_time_out_overload_undergrad_dt.hour
                    thursday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    thursday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, thursday_afternoon_out_time_overload_undergrad_hour, thursday_afternoon_out_time_overload_undergrad_minute)
                    thursday_afternoon_out_time_overload_undergrad_show = thursday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if thursday_morning_time_in_overload_grad_dt == None:
                    thursday_morning_in_time_overload_grad = ""
                    thursday_morning_in_time_overload_grad_show = ""
                else:
                    thursday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_in_overload_grad_dt.hour, thursday_morning_time_in_overload_grad_dt.minute)
                    thursday_morning_in_time_overload_grad_hour = thursday_morning_time_in_overload_grad_dt.hour
                    thursday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    thursday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, thursday_morning_in_time_overload_grad_hour, thursday_morning_in_time_overload_grad_minute)
                    thursday_morning_in_time_overload_grad_show = thursday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if thursday_morning_time_out_overload_grad_dt == None:
                    thursday_morning_out_time_overload_grad = ""
                    thursday_morning_out_time_overload_grad_show = ""
                else:
                    thursday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_out_overload_grad_dt.hour, thursday_morning_time_out_overload_grad_dt.minute)
                    thursday_morning_out_time_overload_grad_hour = thursday_morning_time_out_overload_grad_dt.hour
                    thursday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    thursday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, thursday_morning_out_time_overload_grad_hour, thursday_morning_out_time_overload_grad_minute)
                    thursday_morning_out_time_overload_grad_show = thursday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if thursday_afternoon_time_in_overload_grad_dt == None:
                    thursday_afternoon_in_time_overload_grad = ""
                    thursday_afternoon_in_time_overload_grad_show = ""
                else:
                    thursday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_in_overload_grad_dt.hour, thursday_afternoon_time_in_overload_grad_dt.minute)
                    thursday_afternoon_in_time_overload_grad_hour = thursday_afternoon_time_in_overload_grad_dt.hour
                    thursday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    thursday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, thursday_afternoon_in_time_overload_grad_hour, thursday_afternoon_in_time_overload_grad_minute)
                    thursday_afternoon_in_time_overload_grad_show = thursday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if thursday_afternoon_time_out_overload_grad_dt == None:
                    thursday_afternoon_out_time_overload_grad = ""
                    thursday_afternoon_out_time_overload_grad_show = ""
                else:
                    thursday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_out_overload_grad_dt.hour, thursday_afternoon_time_out_overload_grad_dt.minute)
                    thursday_afternoon_out_time_overload_grad_hour = thursday_afternoon_time_out_overload_grad_dt.hour
                    thursday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    thursday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, thursday_afternoon_out_time_overload_grad_hour, thursday_afternoon_out_time_overload_grad_minute)
                    thursday_afternoon_out_time_overload_grad_show = thursday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if thursday_morning_time_in_dt == None and thursday_morning_time_in_overload_undergrad_dt != None:
                    thursday_morning_in_time = ""
                    thursday_morning_in_time_show = thursday_morning_in_time_overload_undergrad_show
                elif thursday_morning_time_in_dt == None and thursday_morning_time_in_overload_grad_dt != None:
                    thursday_morning_in_time = ""
                    thursday_morning_in_time_show = thursday_morning_in_time_overload_grad_show
                elif thursday_morning_time_in_dt != None and thursday_morning_time_in_overload_undergrad_dt != None:
                    thursday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_in_dt.hour, thursday_morning_time_in_dt.minute)
                    thursday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_out_dt.hour, thursday_morning_time_out_dt.minute)
                    thursday_morning_in_hour = random.randint(thursday_morning_time_in_dt.hour, thursday_morning_time_in_dt.hour)
                    thursday_morning_in_minute = random.randint(0, 59)
                    thursday_morning_in_time = datetime(datetime.now().year, month_int, day, thursday_morning_in_hour, thursday_morning_in_minute)
                    if thursday_morning_in_time_overload_undergrad_condition < thursday_morning_in_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time_overload_undergrad_show
                    elif thursday_morning_in_time_overload_undergrad_condition > thursday_morning_in_time_condition and thursday_morning_in_time_overload_undergrad_condition < thursday_morning_out_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time.strftime('%I:%M %p')
                    elif thursday_morning_in_time_overload_undergrad_condition > thursday_morning_out_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time_overload_undergrad_show
                elif thursday_morning_time_in_dt != None and thursday_morning_time_in_overload_grad_dt != None:
                    thursday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_in_dt.hour, thursday_morning_time_in_dt.minute)
                    thursday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, thursday_morning_time_out_dt.hour, thursday_morning_time_out_dt.minute)
                    thursday_morning_in_hour = random.randint(thursday_morning_time_in_dt.hour, thursday_morning_time_in_dt.hour)
                    thursday_morning_in_minute = random.randint(0, 59)
                    thursday_morning_in_time = datetime(datetime.now().year, month_int, day, thursday_morning_in_hour, thursday_morning_in_minute)
                    if thursday_morning_in_time_overload_grad_condition < thursday_morning_in_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time_overload_grad_show
                    elif thursday_morning_in_time_overload_grad_condition > thursday_morning_in_time_condition and thursday_morning_in_time_overload_grad_condition < thursday_morning_out_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time.strftime('%I:%M %p')
                    elif thursday_morning_in_time_overload_grad_condition > thursday_morning_out_time_condition:
                        thursday_morning_in_time_show = thursday_morning_in_time_overload_grad_show
                elif thursday_morning_time_in_dt == None and thursday_morning_time_in_overload_undergrad_dt == None:
                    thursday_morning_in_time = ""
                    thursday_morning_in_time_show = ""
                elif thursday_morning_time_in_dt == None and thursday_morning_time_in_overload_grad_dt == None:
                    thursday_morning_in_time = ""
                    thursday_morning_in_time_show = ""
                else:
                    thursday_morning_in_hour = random.randint(thursday_morning_time_in_dt.hour, thursday_morning_time_in_dt.hour)
                    thursday_morning_in_minute = random.randint(0, 59)
                    thursday_morning_in_time = datetime(datetime.now().year, month_int, day, thursday_morning_in_hour, thursday_morning_in_minute)
                    thursday_morning_in_time_show = thursday_morning_in_time.strftime('%I:%M %p')
                

                if thursday_morning_time_out_dt != None and thursday_morning_time_out_overload_undergrad_dt != None:
                    thursday_morning_out_hour = random.randint(thursday_morning_time_out_dt.hour, thursday_morning_time_out_dt.hour)
                    thursday_morning_out_minute = random.randint(0, 59)
                    thursday_morning_out_time = datetime(datetime.now().year, month_int, day, thursday_morning_out_hour, thursday_morning_out_minute)
                    if thursday_morning_out_time_overload_undergrad_condition > thursday_morning_out_time_condition:
                        thursday_morning_out_time_show = thursday_morning_out_time_overload_undergrad_show
                    else:
                        thursday_morning_out_time_show = thursday_morning_out_time.strftime('%I:%M %p')
                elif thursday_morning_time_out_dt != None and thursday_morning_time_out_overload_grad_dt != None:
                    thursday_morning_out_hour = random.randint(thursday_morning_time_out_dt.hour, thursday_morning_time_out_dt.hour)
                    thursday_morning_out_minute = random.randint(0, 59)
                    thursday_morning_out_time = datetime(datetime.now().year, month_int, day, thursday_morning_out_hour, thursday_morning_out_minute)
                    if thursday_morning_out_time_overload_grad_condition > thursday_morning_out_time_condition:
                        thursday_morning_out_time_show = thursday_morning_out_time_overload_grad_show
                    else:
                        thursday_morning_out_time_show = thursday_morning_out_time.strftime('%I:%M %p')

                elif thursday_morning_time_out_dt == None and thursday_morning_time_out_overload_undergrad_dt == None:
                    thursday_morning_out_time = ""
                    thursday_morning_out_time_show = ""
                elif thursday_morning_time_out_dt == None and thursday_morning_time_out_overload_grad_dt == None:
                    thursday_morning_out_time = ""
                    thursday_morning_out_time_show = ""
      
                else:
                    thursday_morning_out_hour = random.randint(thursday_morning_time_out_dt.hour, thursday_morning_time_out_dt.hour)
                    thursday_morning_out_minute = random.randint(0, 59)
                    thursday_morning_out_time = datetime(datetime.now().year, month_int, day, thursday_morning_out_hour, thursday_morning_out_minute)
                    thursday_morning_out_time_show = thursday_morning_out_time.strftime('%I:%M %p')

                if thursday_morning_time_out_dt == None and thursday_morning_time_out_overload_undergrad_dt != None:
                    thursday_morning_out_time = ""
                    thursday_morning_out_time_show = thursday_morning_out_time_overload_undergrad_show
                elif thursday_morning_time_out_dt == None and thursday_morning_time_out_overload_grad_dt != None:
                    thursday_morning_out_time = ""
                    thursday_morning_out_time_show = thursday_morning_out_time_overload_grad_show
                
                if thursday_afternoon_time_in_dt == None and thursday_afternoon_time_in_overload_undergrad_dt != None:
                    thursday_afternoon_in_time = ""
                    thursday_afternoon_in_time_show = thursday_afternoon_in_time_overload_undergrad_show
                elif thursday_afternoon_time_in_dt == None and thursday_afternoon_time_in_overload_grad_dt != None:
                    thursday_afternoon_in_time = ""
                    thursday_afternoon_in_time_show = thursday_afternoon_in_time_overload_grad_show
                    
                elif thursday_afternoon_time_in_dt != None and thursday_afternoon_time_in_overload_undergrad_dt != None:
                    thursday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_in_dt.hour, thursday_afternoon_time_in_dt.minute)
                    thursday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_out_dt.hour, thursday_afternoon_time_out_dt.minute)
                    thursday_afternoon_in_hour = random.randint(thursday_afternoon_time_in_dt.hour, thursday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    thursday_afternoon_in_minute = random.randint(0, 59)
                    thursday_afternoon_in_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_in_hour, thursday_afternoon_in_minute)                    
                    if thursday_afternoon_in_time_overload_undergrad_condition < thursday_afternoon_in_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time_overload_undergrad_show
                    elif thursday_afternoon_in_time_overload_undergrad_condition > thursday_afternoon_in_time_condition and thursday_afternoon_in_time_overload_undergrad_condition < thursday_afternoon_out_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time.strftime('%I:%M %p')
                    elif thursday_afternoon_in_time_overload_undergrad_condition > thursday_afternoon_out_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif thursday_afternoon_time_in_dt != None and thursday_afternoon_time_in_overload_grad_dt != None:
                    thursday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_in_dt.hour, thursday_afternoon_time_in_dt.minute)
                    thursday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, thursday_afternoon_time_out_dt.hour, thursday_afternoon_time_out_dt.minute)
                    thursday_afternoon_in_hour = random.randint(thursday_afternoon_time_in_dt.hour, thursday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    thursday_afternoon_in_minute = random.randint(0, 59)
                    thursday_afternoon_in_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_in_hour, thursday_afternoon_in_minute)                    
                    if thursday_afternoon_in_time_overload_grad_condition < thursday_afternoon_in_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time_overload_grad_show
                    elif thursday_afternoon_in_time_overload_grad_condition > thursday_afternoon_in_time_condition and thursday_afternoon_in_time_overload_grad_condition < thursday_afternoon_out_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time.strftime('%I:%M %p')
                    elif thursday_afternoon_in_time_overload_grad_condition > thursday_afternoon_out_time_condition:
                        thursday_afternoon_in_time_show = thursday_afternoon_in_time.strftime('%I:%M %p')
                
                elif thursday_afternoon_time_in_dt == None and thursday_afternoon_time_in_overload_undergrad_dt == None:
                    thursday_afternoon_in_time = ""
                    thursday_afternoon_in_time_show = ""
                elif thursday_afternoon_time_in_dt == None and thursday_afternoon_time_in_overload_grad_dt == None:
                    thursday_afternoon_in_time = ""
                    thursday_afternoon_in_time_show = ""

                else:
                    thursday_afternoon_in_hour = random.randint(thursday_afternoon_time_in_dt.hour, thursday_afternoon_time_in_dt.hour)
                    thursday_afternoon_in_minute = random.randint(0, 59)
                    thursday_afternoon_in_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_in_hour, thursday_afternoon_in_minute)
                    thursday_afternoon_in_time_show = thursday_afternoon_in_time.strftime('%I:%M %p')
                

                if thursday_afternoon_time_out_dt != None and thursday_afternoon_time_out_overload_undergrad_dt != None:
                    thursday_afternoon_out_hour = random.randint(thursday_afternoon_time_out_dt.hour, thursday_afternoon_time_out_dt.hour)
                    thursday_afternoon_out_minute = random.randint(0, 59)
                    thursday_afternoon_out_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_out_hour, thursday_afternoon_out_minute)
                    if thursday_afternoon_out_time_overload_undergrad_condition > thursday_afternoon_out_time_condition:
                        thursday_afternoon_out_time_show = thursday_afternoon_out_time_overload_undergrad_show
                    else:
                        thursday_afternoon_out_time_show = thursday_afternoon_out_time.strftime('%I:%M %p')

                elif thursday_afternoon_time_out_dt != None and thursday_afternoon_time_out_overload_grad_dt != None:
                    thursday_afternoon_out_hour = random.randint(thursday_afternoon_time_out_dt.hour, thursday_afternoon_time_out_dt.hour)
                    thursday_afternoon_out_minute = random.randint(0, 59)
                    thursday_afternoon_out_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_out_hour, thursday_afternoon_out_minute)
                    if thursday_afternoon_out_time_overload_grad_condition > thursday_afternoon_out_time_condition:
                        thursday_afternoon_out_time_show = thursday_afternoon_out_time_overload_grad_show
                    else:
                        thursday_afternoon_out_time_show = thursday_afternoon_out_time.strftime('%I:%M %p')


                elif thursday_afternoon_time_out_dt == None and thursday_afternoon_time_out_overload_undergrad_dt == None:
                    thursday_afternoon_out_time = ""
                    thursday_afternoon_out_time_show = ""
                elif thursday_afternoon_time_out_dt == None and thursday_afternoon_time_out_overload_grad_dt == None:
                    thursday_afternoon_out_time = ""
                    thursday_afternoon_out_time_show = ""
                else:
                    thursday_afternoon_out_hour = random.randint(thursday_afternoon_time_out_dt.hour, thursday_afternoon_time_out_dt.hour)
                    thursday_afternoon_out_minute = random.randint(0, 59)
                    thursday_afternoon_out_time = datetime(datetime.now().year, month_int, day, thursday_afternoon_out_hour, thursday_afternoon_out_minute)
                    thursday_afternoon_out_time_show = thursday_afternoon_out_time.strftime('%I:%M %p')

                if thursday_afternoon_time_out_dt == None and thursday_afternoon_time_out_overload_undergrad_dt != None:
                    thursday_afternoon_out_time = ""
                    thursday_afternoon_out_time_show = thursday_afternoon_out_time_overload_undergrad_show
                elif thursday_afternoon_time_out_dt == None and thursday_afternoon_time_out_overload_grad_dt != None:
                    thursday_afternoon_out_time = ""
                    thursday_afternoon_out_time_show = thursday_afternoon_out_time_overload_grad_show


                if thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    thursday_morning_in_time_show,
                    thursday_morning_out_time_show,
                    thursday_afternoon_in_time_show,
                    thursday_afternoon_out_time_show,
                    thursday_morning_in_time_overload_undergrad_show,
                    thursday_morning_out_time_overload_undergrad_show,
                    thursday_afternoon_in_time_overload_undergrad_show,
                    thursday_afternoon_out_time_overload_undergrad_show,
                    thursday_morning_in_time_overload_grad_show,
                    thursday_morning_out_time_overload_grad_show,
                    thursday_afternoon_in_time_overload_grad_show,
                    thursday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time != "" and thursday_morning_out_time != "" and thursday_afternoon_in_time != "" and thursday_afternoon_out_time != "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad != "" and thursday_morning_out_time_overload_undergrad != "" and thursday_afternoon_in_time_overload_undergrad != "" and thursday_afternoon_out_time_overload_undergrad != "" \
                    and thursday_morning_in_time_overload_grad == "" and thursday_morning_out_time_overload_grad == "" and thursday_afternoon_in_time_overload_grad == "" and thursday_afternoon_out_time_overload_grad == "":
                    if abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif thursday_morning_in_time == "" and thursday_morning_out_time == "" and thursday_afternoon_in_time == "" and thursday_afternoon_out_time == "" \
                    and thursday_morning_in_time_overload_undergrad == "" and thursday_morning_out_time_overload_undergrad == "" and thursday_afternoon_in_time_overload_undergrad == "" and thursday_afternoon_out_time_overload_undergrad == "" \
                    and thursday_morning_in_time_overload_grad != "" and thursday_morning_out_time_overload_grad != "" and thursday_afternoon_in_time_overload_grad != "" and thursday_afternoon_out_time_overload_grad != "":
                    if abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            thursday_morning_in_time_show,
                            thursday_morning_out_time_show,
                            thursday_afternoon_in_time_show,
                            thursday_afternoon_out_time_show,
                            thursday_morning_in_time_overload_undergrad_show,
                            thursday_morning_out_time_overload_undergrad_show,
                            thursday_afternoon_in_time_overload_undergrad_show,
                            thursday_afternoon_out_time_overload_undergrad_show,
                            thursday_morning_in_time_overload_grad_show,
                            thursday_morning_out_time_overload_grad_show,
                            thursday_afternoon_in_time_overload_grad_show,
                            thursday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((thursday_morning_in_time - datetime.combine(thursday_morning_in_time.date(), thursday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((thursday_morning_out_time - datetime.combine(thursday_morning_out_time.date(), thursday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((thursday_morning_in_time_overload_grad - datetime.combine(thursday_morning_in_time_overload_grad.date(), thursday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_morning_out_time_overload_grad - datetime.combine(thursday_morning_out_time_overload_grad.date(), thursday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_morning_in_time_overload_undergrad - datetime.combine(thursday_morning_in_time_overload_undergrad.date(), thursday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_morning_out_time_overload_undergrad - datetime.combine(thursday_morning_out_time_overload_undergrad.date(), thursday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_in_time - datetime.combine(thursday_afternoon_in_time.date(), thursday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_out_time - datetime.combine(thursday_afternoon_out_time.date(), thursday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_in_time_overload_grad - datetime.combine(thursday_afternoon_in_time_overload_grad.date(), thursday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_out_time_overload_grad - datetime.combine(thursday_afternoon_out_time_overload_grad.date(), thursday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_in_time_overload_undergrad - datetime.combine(thursday_afternoon_in_time_overload_undergrad.date(), thursday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((thursday_afternoon_out_time_overload_undergrad - datetime.combine(thursday_afternoon_out_time_overload_undergrad.date(), thursday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                thursday_morning_in_time_show,
                                thursday_morning_out_time_show,
                                thursday_afternoon_in_time_show,
                                thursday_afternoon_out_time_show,
                                thursday_morning_in_time_overload_undergrad_show,
                                thursday_morning_out_time_overload_undergrad_show,
                                thursday_afternoon_in_time_overload_undergrad_show,
                                thursday_afternoon_out_time_overload_undergrad_show,
                                thursday_morning_in_time_overload_grad_show,
                                thursday_morning_out_time_overload_grad_show,
                                thursday_afternoon_in_time_overload_grad_show,
                                thursday_afternoon_out_time_overload_grad_show
                            ))
                            break
                
            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Friday":
                
                if friday_morning_time_in_overload_undergrad_dt == None:
                    friday_morning_in_time_overload_undergrad = ""
                    friday_morning_in_time_overload_undergrad_show = ""
                else:
                    friday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_in_overload_undergrad_dt.hour, friday_morning_time_in_overload_undergrad_dt.minute)
                    friday_morning_in_time_overload_undergrad_hour = friday_morning_time_in_overload_undergrad_dt.hour
                    friday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    friday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, friday_morning_in_time_overload_undergrad_hour, friday_morning_in_time_overload_undergrad_minute)
                    friday_morning_in_time_overload_undergrad_show = friday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if friday_morning_time_out_overload_undergrad_dt == None:
                    friday_morning_out_time_overload_undergrad = ""
                    friday_morning_out_time_overload_undergrad_show = ""
                else:
                    friday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_out_overload_undergrad_dt.hour, friday_morning_time_out_overload_undergrad_dt.minute)
                    friday_morning_out_time_overload_undergrad_hour = friday_morning_time_out_overload_undergrad_dt.hour
                    friday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    friday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, friday_morning_out_time_overload_undergrad_hour, friday_morning_out_time_overload_undergrad_minute)
                    friday_morning_out_time_overload_undergrad_show = friday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if friday_afternoon_time_in_overload_undergrad_dt == None:
                    friday_afternoon_in_time_overload_undergrad = ""
                    friday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    friday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_in_overload_undergrad_dt.hour, friday_afternoon_time_in_overload_undergrad_dt.minute)
                    friday_afternoon_in_time_overload_undergrad_hour = friday_afternoon_time_in_overload_undergrad_dt.hour
                    friday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    friday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, friday_afternoon_in_time_overload_undergrad_hour, friday_afternoon_in_time_overload_undergrad_minute)
                    friday_afternoon_in_time_overload_undergrad_show = friday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if friday_afternoon_time_out_overload_undergrad_dt == None:
                    friday_afternoon_out_time_overload_undergrad = ""
                    friday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    friday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_out_overload_undergrad_dt.hour, friday_afternoon_time_out_overload_undergrad_dt.minute)
                    friday_afternoon_out_time_overload_undergrad_hour = friday_afternoon_time_out_overload_undergrad_dt.hour
                    friday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    friday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, friday_afternoon_out_time_overload_undergrad_hour, friday_afternoon_out_time_overload_undergrad_minute)
                    friday_afternoon_out_time_overload_undergrad_show = friday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if friday_morning_time_in_overload_grad_dt == None:
                    friday_morning_in_time_overload_grad = ""
                    friday_morning_in_time_overload_grad_show = ""
                else:
                    friday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_in_overload_grad_dt.hour, friday_morning_time_in_overload_grad_dt.minute)
                    friday_morning_in_time_overload_grad_hour = friday_morning_time_in_overload_grad_dt.hour
                    friday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    friday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, friday_morning_in_time_overload_grad_hour, friday_morning_in_time_overload_grad_minute)
                    friday_morning_in_time_overload_grad_show = friday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if friday_morning_time_out_overload_grad_dt == None:
                    friday_morning_out_time_overload_grad = ""
                    friday_morning_out_time_overload_grad_show = ""
                else:
                    friday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_out_overload_grad_dt.hour, friday_morning_time_out_overload_grad_dt.minute)
                    friday_morning_out_time_overload_grad_hour = friday_morning_time_out_overload_grad_dt.hour
                    friday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    friday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, friday_morning_out_time_overload_grad_hour, friday_morning_out_time_overload_grad_minute)
                    friday_morning_out_time_overload_grad_show = friday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if friday_afternoon_time_in_overload_grad_dt == None:
                    friday_afternoon_in_time_overload_grad = ""
                    friday_afternoon_in_time_overload_grad_show = ""
                else:
                    friday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_in_overload_grad_dt.hour, friday_afternoon_time_in_overload_grad_dt.minute)
                    friday_afternoon_in_time_overload_grad_hour = friday_afternoon_time_in_overload_grad_dt.hour
                    friday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    friday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, friday_afternoon_in_time_overload_grad_hour, friday_afternoon_in_time_overload_grad_minute)
                    friday_afternoon_in_time_overload_grad_show = friday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if friday_afternoon_time_out_overload_grad_dt == None:
                    friday_afternoon_out_time_overload_grad = ""
                    friday_afternoon_out_time_overload_grad_show = ""
                else:
                    friday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_out_overload_grad_dt.hour, friday_afternoon_time_out_overload_grad_dt.minute)
                    friday_afternoon_out_time_overload_grad_hour = friday_afternoon_time_out_overload_grad_dt.hour
                    friday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    friday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, friday_afternoon_out_time_overload_grad_hour, friday_afternoon_out_time_overload_grad_minute)
                    friday_afternoon_out_time_overload_grad_show = friday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if friday_morning_time_in_dt == None and friday_morning_time_in_overload_undergrad_dt != None:
                    friday_morning_in_time = ""
                    friday_morning_in_time_show = friday_morning_in_time_overload_undergrad_show
                elif friday_morning_time_in_dt == None and friday_morning_time_in_overload_grad_dt != None:
                    friday_morning_in_time = ""
                    friday_morning_in_time_show = friday_morning_in_time_overload_grad_show
                elif friday_morning_time_in_dt != None and friday_morning_time_in_overload_undergrad_dt != None:
                    friday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_in_dt.hour, friday_morning_time_in_dt.minute)
                    friday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_out_dt.hour, friday_morning_time_out_dt.minute)
                    friday_morning_in_hour = random.randint(friday_morning_time_in_dt.hour, friday_morning_time_in_dt.hour)
                    friday_morning_in_minute = random.randint(0, 59)
                    friday_morning_in_time = datetime(datetime.now().year, month_int, day, friday_morning_in_hour, friday_morning_in_minute)
                    if friday_morning_in_time_overload_undergrad_condition < friday_morning_in_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time_overload_undergrad_show
                    elif friday_morning_in_time_overload_undergrad_condition > friday_morning_in_time_condition and friday_morning_in_time_overload_undergrad_condition < friday_morning_out_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time.strftime('%I:%M %p')
                    elif friday_morning_in_time_overload_undergrad_condition > friday_morning_out_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time_overload_undergrad_show
                elif friday_morning_time_in_dt != None and friday_morning_time_in_overload_grad_dt != None:
                    friday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_in_dt.hour, friday_morning_time_in_dt.minute)
                    friday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, friday_morning_time_out_dt.hour, friday_morning_time_out_dt.minute)
                    friday_morning_in_hour = random.randint(friday_morning_time_in_dt.hour, friday_morning_time_in_dt.hour)
                    friday_morning_in_minute = random.randint(0, 59)
                    friday_morning_in_time = datetime(datetime.now().year, month_int, day, friday_morning_in_hour, friday_morning_in_minute)
                    if friday_morning_in_time_overload_grad_condition < friday_morning_in_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time_overload_grad_show
                    elif friday_morning_in_time_overload_grad_condition > friday_morning_in_time_condition and friday_morning_in_time_overload_grad_condition < friday_morning_out_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time.strftime('%I:%M %p')
                    elif friday_morning_in_time_overload_grad_condition > friday_morning_out_time_condition:
                        friday_morning_in_time_show = friday_morning_in_time_overload_grad_show
                elif friday_morning_time_in_dt == None and friday_morning_time_in_overload_undergrad_dt == None:
                    friday_morning_in_time = ""
                    friday_morning_in_time_show = ""
                elif friday_morning_time_in_dt == None and friday_morning_time_in_overload_grad_dt == None:
                    friday_morning_in_time = ""
                    friday_morning_in_time_show = ""
                else:
                    friday_morning_in_hour = random.randint(friday_morning_time_in_dt.hour, friday_morning_time_in_dt.hour)
                    friday_morning_in_minute = random.randint(0, 59)
                    friday_morning_in_time = datetime(datetime.now().year, month_int, day, friday_morning_in_hour, friday_morning_in_minute)
                    friday_morning_in_time_show = friday_morning_in_time.strftime('%I:%M %p')
                

                if friday_morning_time_out_dt != None and friday_morning_time_out_overload_undergrad_dt != None:
                    friday_morning_out_hour = random.randint(friday_morning_time_out_dt.hour, friday_morning_time_out_dt.hour)
                    friday_morning_out_minute = random.randint(0, 59)
                    friday_morning_out_time = datetime(datetime.now().year, month_int, day, friday_morning_out_hour, friday_morning_out_minute)
                    if friday_morning_out_time_overload_undergrad_condition > friday_morning_out_time_condition:
                        friday_morning_out_time_show = friday_morning_out_time_overload_undergrad_show
                    else:
                        friday_morning_out_time_show = friday_morning_out_time.strftime('%I:%M %p')
                elif friday_morning_time_out_dt != None and friday_morning_time_out_overload_grad_dt != None:
                    friday_morning_out_hour = random.randint(friday_morning_time_out_dt.hour, friday_morning_time_out_dt.hour)
                    friday_morning_out_minute = random.randint(0, 59)
                    friday_morning_out_time = datetime(datetime.now().year, month_int, day, friday_morning_out_hour, friday_morning_out_minute)
                    if friday_morning_out_time_overload_grad_condition > friday_morning_out_time_condition:
                        friday_morning_out_time_show = friday_morning_out_time_overload_grad_show
                    else:
                        friday_morning_out_time_show = friday_morning_out_time.strftime('%I:%M %p')

                elif friday_morning_time_out_dt == None and friday_morning_time_out_overload_undergrad_dt == None:
                    friday_morning_out_time = ""
                    friday_morning_out_time_show = ""
                elif friday_morning_time_out_dt == None and friday_morning_time_out_overload_grad_dt == None:
                    friday_morning_out_time = ""
                    friday_morning_out_time_show = ""
      
                else:
                    friday_morning_out_hour = random.randint(friday_morning_time_out_dt.hour, friday_morning_time_out_dt.hour)
                    friday_morning_out_minute = random.randint(0, 59)
                    friday_morning_out_time = datetime(datetime.now().year, month_int, day, friday_morning_out_hour, friday_morning_out_minute)
                    friday_morning_out_time_show = friday_morning_out_time.strftime('%I:%M %p')

                if friday_morning_time_out_dt == None and friday_morning_time_out_overload_undergrad_dt != None:
                    friday_morning_out_time = ""
                    friday_morning_out_time_show = friday_morning_out_time_overload_undergrad_show
                elif friday_morning_time_out_dt == None and friday_morning_time_out_overload_grad_dt != None:
                    friday_morning_out_time = ""
                    friday_morning_out_time_show = friday_morning_out_time_overload_grad_show
                
                if friday_afternoon_time_in_dt == None and friday_afternoon_time_in_overload_undergrad_dt != None:
                    friday_afternoon_in_time = ""
                    friday_afternoon_in_time_show = friday_afternoon_in_time_overload_undergrad_show
                elif friday_afternoon_time_in_dt == None and friday_afternoon_time_in_overload_grad_dt != None:
                    friday_afternoon_in_time = ""
                    friday_afternoon_in_time_show = friday_afternoon_in_time_overload_grad_show
                    
                elif friday_afternoon_time_in_dt != None and friday_afternoon_time_in_overload_undergrad_dt != None:
                    friday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_in_dt.hour, friday_afternoon_time_in_dt.minute)
                    friday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_out_dt.hour, friday_afternoon_time_out_dt.minute)
                    friday_afternoon_in_hour = random.randint(friday_afternoon_time_in_dt.hour, friday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    friday_afternoon_in_minute = random.randint(0, 59)
                    friday_afternoon_in_time = datetime(datetime.now().year, month_int, day, friday_afternoon_in_hour, friday_afternoon_in_minute)                    
                    if friday_afternoon_in_time_overload_undergrad_condition < friday_afternoon_in_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time_overload_undergrad_show
                    elif friday_afternoon_in_time_overload_undergrad_condition > friday_afternoon_in_time_condition and friday_afternoon_in_time_overload_undergrad_condition < friday_afternoon_out_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time.strftime('%I:%M %p')
                    elif friday_afternoon_in_time_overload_undergrad_condition > friday_afternoon_out_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif friday_afternoon_time_in_dt != None and friday_afternoon_time_in_overload_grad_dt != None:
                    friday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_in_dt.hour, friday_afternoon_time_in_dt.minute)
                    friday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, friday_afternoon_time_out_dt.hour, friday_afternoon_time_out_dt.minute)
                    friday_afternoon_in_hour = random.randint(friday_afternoon_time_in_dt.hour, friday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    friday_afternoon_in_minute = random.randint(0, 59)
                    friday_afternoon_in_time = datetime(datetime.now().year, month_int, day, friday_afternoon_in_hour, friday_afternoon_in_minute)                    
                    if friday_afternoon_in_time_overload_grad_condition < friday_afternoon_in_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time_overload_grad_show
                    elif friday_afternoon_in_time_overload_grad_condition > friday_afternoon_in_time_condition and friday_afternoon_in_time_overload_grad_condition < friday_afternoon_out_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time.strftime('%I:%M %p')
                    elif friday_afternoon_in_time_overload_grad_condition > friday_afternoon_out_time_condition:
                        friday_afternoon_in_time_show = friday_afternoon_in_time.strftime('%I:%M %p')
                
                elif friday_afternoon_time_in_dt == None and friday_afternoon_time_in_overload_undergrad_dt == None:
                    friday_afternoon_in_time = ""
                    friday_afternoon_in_time_show = ""
                elif friday_afternoon_time_in_dt == None and friday_afternoon_time_in_overload_grad_dt == None:
                    friday_afternoon_in_time = ""
                    friday_afternoon_in_time_show = ""

                else:
                    friday_afternoon_in_hour = random.randint(friday_afternoon_time_in_dt.hour, friday_afternoon_time_in_dt.hour)
                    friday_afternoon_in_minute = random.randint(0, 59)
                    friday_afternoon_in_time = datetime(datetime.now().year, month_int, day, friday_afternoon_in_hour, friday_afternoon_in_minute)
                    friday_afternoon_in_time_show = friday_afternoon_in_time.strftime('%I:%M %p')
                

                if friday_afternoon_time_out_dt != None and friday_afternoon_time_out_overload_undergrad_dt != None:
                    friday_afternoon_out_hour = random.randint(friday_afternoon_time_out_dt.hour, friday_afternoon_time_out_dt.hour)
                    friday_afternoon_out_minute = random.randint(0, 59)
                    friday_afternoon_out_time = datetime(datetime.now().year, month_int, day, friday_afternoon_out_hour, friday_afternoon_out_minute)
                    if friday_afternoon_out_time_overload_undergrad_condition > friday_afternoon_out_time_condition:
                        friday_afternoon_out_time_show = friday_afternoon_out_time_overload_undergrad_show
                    else:
                        friday_afternoon_out_time_show = friday_afternoon_out_time.strftime('%I:%M %p')

                elif friday_afternoon_time_out_dt != None and friday_afternoon_time_out_overload_grad_dt != None:
                    friday_afternoon_out_hour = random.randint(friday_afternoon_time_out_dt.hour, friday_afternoon_time_out_dt.hour)
                    friday_afternoon_out_minute = random.randint(0, 59)
                    friday_afternoon_out_time = datetime(datetime.now().year, month_int, day, friday_afternoon_out_hour, friday_afternoon_out_minute)
                    if friday_afternoon_out_time_overload_grad_condition > friday_afternoon_out_time_condition:
                        friday_afternoon_out_time_show = friday_afternoon_out_time_overload_grad_show
                    else:
                        friday_afternoon_out_time_show = friday_afternoon_out_time.strftime('%I:%M %p')


                elif friday_afternoon_time_out_dt == None and friday_afternoon_time_out_overload_undergrad_dt == None:
                    friday_afternoon_out_time = ""
                    friday_afternoon_out_time_show = ""
                elif friday_afternoon_time_out_dt == None and friday_afternoon_time_out_overload_grad_dt == None:
                    friday_afternoon_out_time = ""
                    friday_afternoon_out_time_show = ""
                else:
                    friday_afternoon_out_hour = random.randint(friday_afternoon_time_out_dt.hour, friday_afternoon_time_out_dt.hour)
                    friday_afternoon_out_minute = random.randint(0, 59)
                    friday_afternoon_out_time = datetime(datetime.now().year, month_int, day, friday_afternoon_out_hour, friday_afternoon_out_minute)
                    friday_afternoon_out_time_show = friday_afternoon_out_time.strftime('%I:%M %p')

                if friday_afternoon_time_out_dt == None and friday_afternoon_time_out_overload_undergrad_dt != None:
                    friday_afternoon_out_time = ""
                    friday_afternoon_out_time_show = friday_afternoon_out_time_overload_undergrad_show
                elif friday_afternoon_time_out_dt == None and friday_afternoon_time_out_overload_grad_dt != None:
                    friday_afternoon_out_time = ""
                    friday_afternoon_out_time_show = friday_afternoon_out_time_overload_grad_show


                if friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    friday_morning_in_time_show,
                    friday_morning_out_time_show,
                    friday_afternoon_in_time_show,
                    friday_afternoon_out_time_show,
                    friday_morning_in_time_overload_undergrad_show,
                    friday_morning_out_time_overload_undergrad_show,
                    friday_afternoon_in_time_overload_undergrad_show,
                    friday_afternoon_out_time_overload_undergrad_show,
                    friday_morning_in_time_overload_grad_show,
                    friday_morning_out_time_overload_grad_show,
                    friday_afternoon_in_time_overload_grad_show,
                    friday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time != "" and friday_morning_out_time != "" and friday_afternoon_in_time != "" and friday_afternoon_out_time != "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad != "" and friday_morning_out_time_overload_undergrad != "" and friday_afternoon_in_time_overload_undergrad != "" and friday_afternoon_out_time_overload_undergrad != "" \
                    and friday_morning_in_time_overload_grad == "" and friday_morning_out_time_overload_grad == "" and friday_afternoon_in_time_overload_grad == "" and friday_afternoon_out_time_overload_grad == "":
                    if abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif friday_morning_in_time == "" and friday_morning_out_time == "" and friday_afternoon_in_time == "" and friday_afternoon_out_time == "" \
                    and friday_morning_in_time_overload_undergrad == "" and friday_morning_out_time_overload_undergrad == "" and friday_afternoon_in_time_overload_undergrad == "" and friday_afternoon_out_time_overload_undergrad == "" \
                    and friday_morning_in_time_overload_grad != "" and friday_morning_out_time_overload_grad != "" and friday_afternoon_in_time_overload_grad != "" and friday_afternoon_out_time_overload_grad != "":
                    if abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            friday_morning_in_time_show,
                            friday_morning_out_time_show,
                            friday_afternoon_in_time_show,
                            friday_afternoon_out_time_show,
                            friday_morning_in_time_overload_undergrad_show,
                            friday_morning_out_time_overload_undergrad_show,
                            friday_afternoon_in_time_overload_undergrad_show,
                            friday_afternoon_out_time_overload_undergrad_show,
                            friday_morning_in_time_overload_grad_show,
                            friday_morning_out_time_overload_grad_show,
                            friday_afternoon_in_time_overload_grad_show,
                            friday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((friday_morning_in_time - datetime.combine(friday_morning_in_time.date(), friday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((friday_morning_out_time - datetime.combine(friday_morning_out_time.date(), friday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((friday_morning_in_time_overload_grad - datetime.combine(friday_morning_in_time_overload_grad.date(), friday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((friday_morning_out_time_overload_grad - datetime.combine(friday_morning_out_time_overload_grad.date(), friday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((friday_morning_in_time_overload_undergrad - datetime.combine(friday_morning_in_time_overload_undergrad.date(), friday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((friday_morning_out_time_overload_undergrad - datetime.combine(friday_morning_out_time_overload_undergrad.date(), friday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_in_time - datetime.combine(friday_afternoon_in_time.date(), friday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_out_time - datetime.combine(friday_afternoon_out_time.date(), friday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_in_time_overload_grad - datetime.combine(friday_afternoon_in_time_overload_grad.date(), friday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_out_time_overload_grad - datetime.combine(friday_afternoon_out_time_overload_grad.date(), friday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_in_time_overload_undergrad - datetime.combine(friday_afternoon_in_time_overload_undergrad.date(), friday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((friday_afternoon_out_time_overload_undergrad - datetime.combine(friday_afternoon_out_time_overload_undergrad.date(), friday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                friday_morning_in_time_show,
                                friday_morning_out_time_show,
                                friday_afternoon_in_time_show,
                                friday_afternoon_out_time_show,
                                friday_morning_in_time_overload_undergrad_show,
                                friday_morning_out_time_overload_undergrad_show,
                                friday_afternoon_in_time_overload_undergrad_show,
                                friday_afternoon_out_time_overload_undergrad_show,
                                friday_morning_in_time_overload_grad_show,
                                friday_morning_out_time_overload_grad_show,
                                friday_afternoon_in_time_overload_grad_show,
                                friday_afternoon_out_time_overload_grad_show
                            ))
                            break
                
            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Saturday":
                
                if saturday_morning_time_in_overload_undergrad_dt == None:
                    saturday_morning_in_time_overload_undergrad = ""
                    saturday_morning_in_time_overload_undergrad_show = ""
                else:
                    saturday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_in_overload_undergrad_dt.hour, saturday_morning_time_in_overload_undergrad_dt.minute)
                    saturday_morning_in_time_overload_undergrad_hour = saturday_morning_time_in_overload_undergrad_dt.hour
                    saturday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    saturday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, saturday_morning_in_time_overload_undergrad_hour, saturday_morning_in_time_overload_undergrad_minute)
                    saturday_morning_in_time_overload_undergrad_show = saturday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if saturday_morning_time_out_overload_undergrad_dt == None:
                    saturday_morning_out_time_overload_undergrad = ""
                    saturday_morning_out_time_overload_undergrad_show = ""
                else:
                    saturday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_out_overload_undergrad_dt.hour, saturday_morning_time_out_overload_undergrad_dt.minute)
                    saturday_morning_out_time_overload_undergrad_hour = saturday_morning_time_out_overload_undergrad_dt.hour
                    saturday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    saturday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, saturday_morning_out_time_overload_undergrad_hour, saturday_morning_out_time_overload_undergrad_minute)
                    saturday_morning_out_time_overload_undergrad_show = saturday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if saturday_afternoon_time_in_overload_undergrad_dt == None:
                    saturday_afternoon_in_time_overload_undergrad = ""
                    saturday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    saturday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_in_overload_undergrad_dt.hour, saturday_afternoon_time_in_overload_undergrad_dt.minute)
                    saturday_afternoon_in_time_overload_undergrad_hour = saturday_afternoon_time_in_overload_undergrad_dt.hour
                    saturday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    saturday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, saturday_afternoon_in_time_overload_undergrad_hour, saturday_afternoon_in_time_overload_undergrad_minute)
                    saturday_afternoon_in_time_overload_undergrad_show = saturday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if saturday_afternoon_time_out_overload_undergrad_dt == None:
                    saturday_afternoon_out_time_overload_undergrad = ""
                    saturday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    saturday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_out_overload_undergrad_dt.hour, saturday_afternoon_time_out_overload_undergrad_dt.minute)
                    saturday_afternoon_out_time_overload_undergrad_hour = saturday_afternoon_time_out_overload_undergrad_dt.hour
                    saturday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    saturday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, saturday_afternoon_out_time_overload_undergrad_hour, saturday_afternoon_out_time_overload_undergrad_minute)
                    saturday_afternoon_out_time_overload_undergrad_show = saturday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if saturday_morning_time_in_overload_grad_dt == None:
                    saturday_morning_in_time_overload_grad = ""
                    saturday_morning_in_time_overload_grad_show = ""
                else:
                    saturday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_in_overload_grad_dt.hour, saturday_morning_time_in_overload_grad_dt.minute)
                    saturday_morning_in_time_overload_grad_hour = saturday_morning_time_in_overload_grad_dt.hour
                    saturday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    saturday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, saturday_morning_in_time_overload_grad_hour, saturday_morning_in_time_overload_grad_minute)
                    saturday_morning_in_time_overload_grad_show = saturday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if saturday_morning_time_out_overload_grad_dt == None:
                    saturday_morning_out_time_overload_grad = ""
                    saturday_morning_out_time_overload_grad_show = ""
                else:
                    saturday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_out_overload_grad_dt.hour, saturday_morning_time_out_overload_grad_dt.minute)
                    saturday_morning_out_time_overload_grad_hour = saturday_morning_time_out_overload_grad_dt.hour
                    saturday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    saturday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, saturday_morning_out_time_overload_grad_hour, saturday_morning_out_time_overload_grad_minute)
                    saturday_morning_out_time_overload_grad_show = saturday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if saturday_afternoon_time_in_overload_grad_dt == None:
                    saturday_afternoon_in_time_overload_grad = ""
                    saturday_afternoon_in_time_overload_grad_show = ""
                else:
                    saturday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_in_overload_grad_dt.hour, saturday_afternoon_time_in_overload_grad_dt.minute)
                    saturday_afternoon_in_time_overload_grad_hour = saturday_afternoon_time_in_overload_grad_dt.hour
                    saturday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    saturday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, saturday_afternoon_in_time_overload_grad_hour, saturday_afternoon_in_time_overload_grad_minute)
                    saturday_afternoon_in_time_overload_grad_show = saturday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if saturday_afternoon_time_out_overload_grad_dt == None:
                    saturday_afternoon_out_time_overload_grad = ""
                    saturday_afternoon_out_time_overload_grad_show = ""
                else:
                    saturday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_out_overload_grad_dt.hour, saturday_afternoon_time_out_overload_grad_dt.minute)
                    saturday_afternoon_out_time_overload_grad_hour = saturday_afternoon_time_out_overload_grad_dt.hour
                    saturday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    saturday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, saturday_afternoon_out_time_overload_grad_hour, saturday_afternoon_out_time_overload_grad_minute)
                    saturday_afternoon_out_time_overload_grad_show = saturday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if saturday_morning_time_in_dt == None and saturday_morning_time_in_overload_undergrad_dt != None:
                    saturday_morning_in_time = ""
                    saturday_morning_in_time_show = saturday_morning_in_time_overload_undergrad_show
                elif saturday_morning_time_in_dt == None and saturday_morning_time_in_overload_grad_dt != None:
                    saturday_morning_in_time = ""
                    saturday_morning_in_time_show = saturday_morning_in_time_overload_grad_show
                elif saturday_morning_time_in_dt != None and saturday_morning_time_in_overload_undergrad_dt != None:
                    saturday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_in_dt.hour, saturday_morning_time_in_dt.minute)
                    saturday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_out_dt.hour, saturday_morning_time_out_dt.minute)
                    saturday_morning_in_hour = random.randint(saturday_morning_time_in_dt.hour, saturday_morning_time_in_dt.hour)
                    saturday_morning_in_minute = random.randint(0, 59)
                    saturday_morning_in_time = datetime(datetime.now().year, month_int, day, saturday_morning_in_hour, saturday_morning_in_minute)
                    if saturday_morning_in_time_overload_undergrad_condition < saturday_morning_in_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time_overload_undergrad_show
                    elif saturday_morning_in_time_overload_undergrad_condition > saturday_morning_in_time_condition and saturday_morning_in_time_overload_undergrad_condition < saturday_morning_out_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time.strftime('%I:%M %p')
                    elif saturday_morning_in_time_overload_undergrad_condition > saturday_morning_out_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time_overload_undergrad_show
                elif saturday_morning_time_in_dt != None and saturday_morning_time_in_overload_grad_dt != None:
                    saturday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_in_dt.hour, saturday_morning_time_in_dt.minute)
                    saturday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, saturday_morning_time_out_dt.hour, saturday_morning_time_out_dt.minute)
                    saturday_morning_in_hour = random.randint(saturday_morning_time_in_dt.hour, saturday_morning_time_in_dt.hour)
                    saturday_morning_in_minute = random.randint(0, 59)
                    saturday_morning_in_time = datetime(datetime.now().year, month_int, day, saturday_morning_in_hour, saturday_morning_in_minute)
                    if saturday_morning_in_time_overload_grad_condition < saturday_morning_in_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time_overload_grad_show
                    elif saturday_morning_in_time_overload_grad_condition > saturday_morning_in_time_condition and saturday_morning_in_time_overload_grad_condition < saturday_morning_out_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time.strftime('%I:%M %p')
                    elif saturday_morning_in_time_overload_grad_condition > saturday_morning_out_time_condition:
                        saturday_morning_in_time_show = saturday_morning_in_time_overload_grad_show
                elif saturday_morning_time_in_dt == None and saturday_morning_time_in_overload_undergrad_dt == None:
                    saturday_morning_in_time = ""
                    saturday_morning_in_time_show = ""
                elif saturday_morning_time_in_dt == None and saturday_morning_time_in_overload_grad_dt == None:
                    saturday_morning_in_time = ""
                    saturday_morning_in_time_show = ""
                else:
                    saturday_morning_in_hour = random.randint(saturday_morning_time_in_dt.hour, saturday_morning_time_in_dt.hour)
                    saturday_morning_in_minute = random.randint(0, 59)
                    saturday_morning_in_time = datetime(datetime.now().year, month_int, day, saturday_morning_in_hour, saturday_morning_in_minute)
                    saturday_morning_in_time_show = saturday_morning_in_time.strftime('%I:%M %p')
                

                if saturday_morning_time_out_dt != None and saturday_morning_time_out_overload_undergrad_dt != None:
                    saturday_morning_out_hour = random.randint(saturday_morning_time_out_dt.hour, saturday_morning_time_out_dt.hour)
                    saturday_morning_out_minute = random.randint(0, 59)
                    saturday_morning_out_time = datetime(datetime.now().year, month_int, day, saturday_morning_out_hour, saturday_morning_out_minute)
                    if saturday_morning_out_time_overload_undergrad_condition > saturday_morning_out_time_condition:
                        saturday_morning_out_time_show = saturday_morning_out_time_overload_undergrad_show
                    else:
                        saturday_morning_out_time_show = saturday_morning_out_time.strftime('%I:%M %p')
                elif saturday_morning_time_out_dt != None and saturday_morning_time_out_overload_grad_dt != None:
                    saturday_morning_out_hour = random.randint(saturday_morning_time_out_dt.hour, saturday_morning_time_out_dt.hour)
                    saturday_morning_out_minute = random.randint(0, 59)
                    saturday_morning_out_time = datetime(datetime.now().year, month_int, day, saturday_morning_out_hour, saturday_morning_out_minute)
                    if saturday_morning_out_time_overload_grad_condition > saturday_morning_out_time_condition:
                        saturday_morning_out_time_show = saturday_morning_out_time_overload_grad_show
                    else:
                        saturday_morning_out_time_show = saturday_morning_out_time.strftime('%I:%M %p')

                elif saturday_morning_time_out_dt == None and saturday_morning_time_out_overload_undergrad_dt == None:
                    saturday_morning_out_time = ""
                    saturday_morning_out_time_show = ""
                elif saturday_morning_time_out_dt == None and saturday_morning_time_out_overload_grad_dt == None:
                    saturday_morning_out_time = ""
                    saturday_morning_out_time_show = ""
      
                else:
                    saturday_morning_out_hour = random.randint(saturday_morning_time_out_dt.hour, saturday_morning_time_out_dt.hour)
                    saturday_morning_out_minute = random.randint(0, 59)
                    saturday_morning_out_time = datetime(datetime.now().year, month_int, day, saturday_morning_out_hour, saturday_morning_out_minute)
                    saturday_morning_out_time_show = saturday_morning_out_time.strftime('%I:%M %p')

                if saturday_morning_time_out_dt == None and saturday_morning_time_out_overload_undergrad_dt != None:
                    saturday_morning_out_time = ""
                    saturday_morning_out_time_show = saturday_morning_out_time_overload_undergrad_show
                elif saturday_morning_time_out_dt == None and saturday_morning_time_out_overload_grad_dt != None:
                    saturday_morning_out_time = ""
                    saturday_morning_out_time_show = saturday_morning_out_time_overload_grad_show
                
                if saturday_afternoon_time_in_dt == None and saturday_afternoon_time_in_overload_undergrad_dt != None:
                    saturday_afternoon_in_time = ""
                    saturday_afternoon_in_time_show = saturday_afternoon_in_time_overload_undergrad_show
                elif saturday_afternoon_time_in_dt == None and saturday_afternoon_time_in_overload_grad_dt != None:
                    saturday_afternoon_in_time = ""
                    saturday_afternoon_in_time_show = saturday_afternoon_in_time_overload_grad_show
                    
                elif saturday_afternoon_time_in_dt != None and saturday_afternoon_time_in_overload_undergrad_dt != None:
                    saturday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_in_dt.hour, saturday_afternoon_time_in_dt.minute)
                    saturday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_out_dt.hour, saturday_afternoon_time_out_dt.minute)
                    saturday_afternoon_in_hour = random.randint(saturday_afternoon_time_in_dt.hour, saturday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    saturday_afternoon_in_minute = random.randint(0, 59)
                    saturday_afternoon_in_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_in_hour, saturday_afternoon_in_minute)                    
                    if saturday_afternoon_in_time_overload_undergrad_condition < saturday_afternoon_in_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time_overload_undergrad_show
                    elif saturday_afternoon_in_time_overload_undergrad_condition > saturday_afternoon_in_time_condition and saturday_afternoon_in_time_overload_undergrad_condition < saturday_afternoon_out_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time.strftime('%I:%M %p')
                    elif saturday_afternoon_in_time_overload_undergrad_condition > saturday_afternoon_out_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif saturday_afternoon_time_in_dt != None and saturday_afternoon_time_in_overload_grad_dt != None:
                    saturday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_in_dt.hour, saturday_afternoon_time_in_dt.minute)
                    saturday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, saturday_afternoon_time_out_dt.hour, saturday_afternoon_time_out_dt.minute)
                    saturday_afternoon_in_hour = random.randint(saturday_afternoon_time_in_dt.hour, saturday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    saturday_afternoon_in_minute = random.randint(0, 59)
                    saturday_afternoon_in_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_in_hour, saturday_afternoon_in_minute)                    
                    if saturday_afternoon_in_time_overload_grad_condition < saturday_afternoon_in_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time_overload_grad_show
                    elif saturday_afternoon_in_time_overload_grad_condition > saturday_afternoon_in_time_condition and saturday_afternoon_in_time_overload_grad_condition < saturday_afternoon_out_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time.strftime('%I:%M %p')
                    elif saturday_afternoon_in_time_overload_grad_condition > saturday_afternoon_out_time_condition:
                        saturday_afternoon_in_time_show = saturday_afternoon_in_time.strftime('%I:%M %p')
                
                elif saturday_afternoon_time_in_dt == None and saturday_afternoon_time_in_overload_undergrad_dt == None:
                    saturday_afternoon_in_time = ""
                    saturday_afternoon_in_time_show = ""
                elif saturday_afternoon_time_in_dt == None and saturday_afternoon_time_in_overload_grad_dt == None:
                    saturday_afternoon_in_time = ""
                    saturday_afternoon_in_time_show = ""

                else:
                    saturday_afternoon_in_hour = random.randint(saturday_afternoon_time_in_dt.hour, saturday_afternoon_time_in_dt.hour)
                    saturday_afternoon_in_minute = random.randint(0, 59)
                    saturday_afternoon_in_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_in_hour, saturday_afternoon_in_minute)
                    saturday_afternoon_in_time_show = saturday_afternoon_in_time.strftime('%I:%M %p')
                

                if saturday_afternoon_time_out_dt != None and saturday_afternoon_time_out_overload_undergrad_dt != None:
                    saturday_afternoon_out_hour = random.randint(saturday_afternoon_time_out_dt.hour, saturday_afternoon_time_out_dt.hour)
                    saturday_afternoon_out_minute = random.randint(0, 59)
                    saturday_afternoon_out_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_out_hour, saturday_afternoon_out_minute)
                    if saturday_afternoon_out_time_overload_undergrad_condition > saturday_afternoon_out_time_condition:
                        saturday_afternoon_out_time_show = saturday_afternoon_out_time_overload_undergrad_show
                    else:
                        saturday_afternoon_out_time_show = saturday_afternoon_out_time.strftime('%I:%M %p')

                elif saturday_afternoon_time_out_dt != None and saturday_afternoon_time_out_overload_grad_dt != None:
                    saturday_afternoon_out_hour = random.randint(saturday_afternoon_time_out_dt.hour, saturday_afternoon_time_out_dt.hour)
                    saturday_afternoon_out_minute = random.randint(0, 59)
                    saturday_afternoon_out_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_out_hour, saturday_afternoon_out_minute)
                    if saturday_afternoon_out_time_overload_grad_condition > saturday_afternoon_out_time_condition:
                        saturday_afternoon_out_time_show = saturday_afternoon_out_time_overload_grad_show
                    else:
                        saturday_afternoon_out_time_show = saturday_afternoon_out_time.strftime('%I:%M %p')


                elif saturday_afternoon_time_out_dt == None and saturday_afternoon_time_out_overload_undergrad_dt == None:
                    saturday_afternoon_out_time = ""
                    saturday_afternoon_out_time_show = ""
                elif saturday_afternoon_time_out_dt == None and saturday_afternoon_time_out_overload_grad_dt == None:
                    saturday_afternoon_out_time = ""
                    saturday_afternoon_out_time_show = ""
                else:
                    saturday_afternoon_out_hour = random.randint(saturday_afternoon_time_out_dt.hour, saturday_afternoon_time_out_dt.hour)
                    saturday_afternoon_out_minute = random.randint(0, 59)
                    saturday_afternoon_out_time = datetime(datetime.now().year, month_int, day, saturday_afternoon_out_hour, saturday_afternoon_out_minute)
                    saturday_afternoon_out_time_show = saturday_afternoon_out_time.strftime('%I:%M %p')

                if saturday_afternoon_time_out_dt == None and saturday_afternoon_time_out_overload_undergrad_dt != None:
                    saturday_afternoon_out_time = ""
                    saturday_afternoon_out_time_show = saturday_afternoon_out_time_overload_undergrad_show
                elif saturday_afternoon_time_out_dt == None and saturday_afternoon_time_out_overload_grad_dt != None:
                    saturday_afternoon_out_time = ""
                    saturday_afternoon_out_time_show = saturday_afternoon_out_time_overload_grad_show


                if saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    saturday_morning_in_time_show,
                    saturday_morning_out_time_show,
                    saturday_afternoon_in_time_show,
                    saturday_afternoon_out_time_show,
                    saturday_morning_in_time_overload_undergrad_show,
                    saturday_morning_out_time_overload_undergrad_show,
                    saturday_afternoon_in_time_overload_undergrad_show,
                    saturday_afternoon_out_time_overload_undergrad_show,
                    saturday_morning_in_time_overload_grad_show,
                    saturday_morning_out_time_overload_grad_show,
                    saturday_afternoon_in_time_overload_grad_show,
                    saturday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time != "" and saturday_morning_out_time != "" and saturday_afternoon_in_time != "" and saturday_afternoon_out_time != "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad != "" and saturday_morning_out_time_overload_undergrad != "" and saturday_afternoon_in_time_overload_undergrad != "" and saturday_afternoon_out_time_overload_undergrad != "" \
                    and saturday_morning_in_time_overload_grad == "" and saturday_morning_out_time_overload_grad == "" and saturday_afternoon_in_time_overload_grad == "" and saturday_afternoon_out_time_overload_grad == "":
                    if abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif saturday_morning_in_time == "" and saturday_morning_out_time == "" and saturday_afternoon_in_time == "" and saturday_afternoon_out_time == "" \
                    and saturday_morning_in_time_overload_undergrad == "" and saturday_morning_out_time_overload_undergrad == "" and saturday_afternoon_in_time_overload_undergrad == "" and saturday_afternoon_out_time_overload_undergrad == "" \
                    and saturday_morning_in_time_overload_grad != "" and saturday_morning_out_time_overload_grad != "" and saturday_afternoon_in_time_overload_grad != "" and saturday_afternoon_out_time_overload_grad != "":
                    if abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            saturday_morning_in_time_show,
                            saturday_morning_out_time_show,
                            saturday_afternoon_in_time_show,
                            saturday_afternoon_out_time_show,
                            saturday_morning_in_time_overload_undergrad_show,
                            saturday_morning_out_time_overload_undergrad_show,
                            saturday_afternoon_in_time_overload_undergrad_show,
                            saturday_afternoon_out_time_overload_undergrad_show,
                            saturday_morning_in_time_overload_grad_show,
                            saturday_morning_out_time_overload_grad_show,
                            saturday_afternoon_in_time_overload_grad_show,
                            saturday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((saturday_morning_in_time - datetime.combine(saturday_morning_in_time.date(), saturday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((saturday_morning_out_time - datetime.combine(saturday_morning_out_time.date(), saturday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((saturday_morning_in_time_overload_grad - datetime.combine(saturday_morning_in_time_overload_grad.date(), saturday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_morning_out_time_overload_grad - datetime.combine(saturday_morning_out_time_overload_grad.date(), saturday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_morning_in_time_overload_undergrad - datetime.combine(saturday_morning_in_time_overload_undergrad.date(), saturday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_morning_out_time_overload_undergrad - datetime.combine(saturday_morning_out_time_overload_undergrad.date(), saturday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_in_time - datetime.combine(saturday_afternoon_in_time.date(), saturday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_out_time - datetime.combine(saturday_afternoon_out_time.date(), saturday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_in_time_overload_grad - datetime.combine(saturday_afternoon_in_time_overload_grad.date(), saturday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_out_time_overload_grad - datetime.combine(saturday_afternoon_out_time_overload_grad.date(), saturday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_in_time_overload_undergrad - datetime.combine(saturday_afternoon_in_time_overload_undergrad.date(), saturday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((saturday_afternoon_out_time_overload_undergrad - datetime.combine(saturday_afternoon_out_time_overload_undergrad.date(), saturday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                saturday_morning_in_time_show,
                                saturday_morning_out_time_show,
                                saturday_afternoon_in_time_show,
                                saturday_afternoon_out_time_show,
                                saturday_morning_in_time_overload_undergrad_show,
                                saturday_morning_out_time_overload_undergrad_show,
                                saturday_afternoon_in_time_overload_undergrad_show,
                                saturday_afternoon_out_time_overload_undergrad_show,
                                saturday_morning_in_time_overload_grad_show,
                                saturday_morning_out_time_overload_grad_show,
                                saturday_afternoon_in_time_overload_grad_show,
                                saturday_afternoon_out_time_overload_grad_show
                            ))
                            break
                
            elif datetime(datetime.now().year, month_int, day).strftime('%A') == "Sunday":
                
                if sunday_morning_time_in_overload_undergrad_dt == None:
                    sunday_morning_in_time_overload_undergrad = ""
                    sunday_morning_in_time_overload_undergrad_show = ""
                else:
                    sunday_morning_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_in_overload_undergrad_dt.hour, sunday_morning_time_in_overload_undergrad_dt.minute)
                    sunday_morning_in_time_overload_undergrad_hour = sunday_morning_time_in_overload_undergrad_dt.hour
                    sunday_morning_in_time_overload_undergrad_minute = random.randint(0, 59)
                    sunday_morning_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, sunday_morning_in_time_overload_undergrad_hour, sunday_morning_in_time_overload_undergrad_minute)
                    sunday_morning_in_time_overload_undergrad_show = sunday_morning_in_time_overload_undergrad.strftime('%I:%M %p')

                if sunday_morning_time_out_overload_undergrad_dt == None:
                    sunday_morning_out_time_overload_undergrad = ""
                    sunday_morning_out_time_overload_undergrad_show = ""
                else:
                    sunday_morning_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_out_overload_undergrad_dt.hour, sunday_morning_time_out_overload_undergrad_dt.minute)
                    sunday_morning_out_time_overload_undergrad_hour = sunday_morning_time_out_overload_undergrad_dt.hour
                    sunday_morning_out_time_overload_undergrad_minute = random.randint(0, 59)
                    sunday_morning_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, sunday_morning_out_time_overload_undergrad_hour, sunday_morning_out_time_overload_undergrad_minute)
                    sunday_morning_out_time_overload_undergrad_show = sunday_morning_out_time_overload_undergrad.strftime('%I:%M %p')

                if sunday_afternoon_time_in_overload_undergrad_dt == None:
                    sunday_afternoon_in_time_overload_undergrad = ""
                    sunday_afternoon_in_time_overload_undergrad_show = ""
                else:
                    sunday_afternoon_in_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_in_overload_undergrad_dt.hour, sunday_afternoon_time_in_overload_undergrad_dt.minute)
                    sunday_afternoon_in_time_overload_undergrad_hour = sunday_afternoon_time_in_overload_undergrad_dt.hour
                    sunday_afternoon_in_time_overload_undergrad_minute = random.randint(0, 59)
                    sunday_afternoon_in_time_overload_undergrad = datetime(datetime.now().year, month_int, day, sunday_afternoon_in_time_overload_undergrad_hour, sunday_afternoon_in_time_overload_undergrad_minute)
                    sunday_afternoon_in_time_overload_undergrad_show = sunday_afternoon_in_time_overload_undergrad.strftime('%I:%M %p')

                if sunday_afternoon_time_out_overload_undergrad_dt == None:
                    sunday_afternoon_out_time_overload_undergrad = ""
                    sunday_afternoon_out_time_overload_undergrad_show = ""
                else:
                    sunday_afternoon_out_time_overload_undergrad_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_out_overload_undergrad_dt.hour, sunday_afternoon_time_out_overload_undergrad_dt.minute)
                    sunday_afternoon_out_time_overload_undergrad_hour = sunday_afternoon_time_out_overload_undergrad_dt.hour
                    sunday_afternoon_out_time_overload_undergrad_minute = random.randint(0, 59)
                    sunday_afternoon_out_time_overload_undergrad = datetime(datetime.now().year, month_int, day, sunday_afternoon_out_time_overload_undergrad_hour, sunday_afternoon_out_time_overload_undergrad_minute)
                    sunday_afternoon_out_time_overload_undergrad_show = sunday_afternoon_out_time_overload_undergrad.strftime('%I:%M %p')

                if sunday_morning_time_in_overload_grad_dt == None:
                    sunday_morning_in_time_overload_grad = ""
                    sunday_morning_in_time_overload_grad_show = ""
                else:
                    sunday_morning_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_in_overload_grad_dt.hour, sunday_morning_time_in_overload_grad_dt.minute)
                    sunday_morning_in_time_overload_grad_hour = sunday_morning_time_in_overload_grad_dt.hour
                    sunday_morning_in_time_overload_grad_minute = random.randint(0, 59)
                    sunday_morning_in_time_overload_grad = datetime(datetime.now().year, month_int, day, sunday_morning_in_time_overload_grad_hour, sunday_morning_in_time_overload_grad_minute)
                    sunday_morning_in_time_overload_grad_show = sunday_morning_in_time_overload_grad.strftime('%I:%M %p')

                if sunday_morning_time_out_overload_grad_dt == None:
                    sunday_morning_out_time_overload_grad = ""
                    sunday_morning_out_time_overload_grad_show = ""
                else:
                    sunday_morning_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_out_overload_grad_dt.hour, sunday_morning_time_out_overload_grad_dt.minute)
                    sunday_morning_out_time_overload_grad_hour = sunday_morning_time_out_overload_grad_dt.hour
                    sunday_morning_out_time_overload_grad_minute = random.randint(0, 59)
                    sunday_morning_out_time_overload_grad = datetime(datetime.now().year, month_int, day, sunday_morning_out_time_overload_grad_hour, sunday_morning_out_time_overload_grad_minute)
                    sunday_morning_out_time_overload_grad_show = sunday_morning_out_time_overload_grad.strftime('%I:%M %p')

                if sunday_afternoon_time_in_overload_grad_dt == None:
                    sunday_afternoon_in_time_overload_grad = ""
                    sunday_afternoon_in_time_overload_grad_show = ""
                else:
                    sunday_afternoon_in_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_in_overload_grad_dt.hour, sunday_afternoon_time_in_overload_grad_dt.minute)
                    sunday_afternoon_in_time_overload_grad_hour = sunday_afternoon_time_in_overload_grad_dt.hour
                    sunday_afternoon_in_time_overload_grad_minute = random.randint(0, 59)
                    sunday_afternoon_in_time_overload_grad = datetime(datetime.now().year, month_int, day, sunday_afternoon_in_time_overload_grad_hour, sunday_afternoon_in_time_overload_grad_minute)
                    sunday_afternoon_in_time_overload_grad_show = sunday_afternoon_in_time_overload_grad.strftime('%I:%M %p')

                if sunday_afternoon_time_out_overload_grad_dt == None:
                    sunday_afternoon_out_time_overload_grad = ""
                    sunday_afternoon_out_time_overload_grad_show = ""
                else:
                    sunday_afternoon_out_time_overload_grad_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_out_overload_grad_dt.hour, sunday_afternoon_time_out_overload_grad_dt.minute)
                    sunday_afternoon_out_time_overload_grad_hour = sunday_afternoon_time_out_overload_grad_dt.hour
                    sunday_afternoon_out_time_overload_grad_minute = random.randint(0, 59)
                    sunday_afternoon_out_time_overload_grad = datetime(datetime.now().year, month_int, day, sunday_afternoon_out_time_overload_grad_hour, sunday_afternoon_out_time_overload_grad_minute)
                    sunday_afternoon_out_time_overload_grad_show = sunday_afternoon_out_time_overload_grad.strftime('%I:%M %p')

                if sunday_morning_time_in_dt == None and sunday_morning_time_in_overload_undergrad_dt != None:
                    sunday_morning_in_time = ""
                    sunday_morning_in_time_show = sunday_morning_in_time_overload_undergrad_show
                elif sunday_morning_time_in_dt == None and sunday_morning_time_in_overload_grad_dt != None:
                    sunday_morning_in_time = ""
                    sunday_morning_in_time_show = sunday_morning_in_time_overload_grad_show
                elif sunday_morning_time_in_dt != None and sunday_morning_time_in_overload_undergrad_dt != None:
                    sunday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_in_dt.hour, sunday_morning_time_in_dt.minute)
                    sunday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_out_dt.hour, sunday_morning_time_out_dt.minute)
                    sunday_morning_in_hour = random.randint(sunday_morning_time_in_dt.hour, sunday_morning_time_in_dt.hour)
                    sunday_morning_in_minute = random.randint(0, 59)
                    sunday_morning_in_time = datetime(datetime.now().year, month_int, day, sunday_morning_in_hour, sunday_morning_in_minute)
                    if sunday_morning_in_time_overload_undergrad_condition < sunday_morning_in_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time_overload_undergrad_show
                    elif sunday_morning_in_time_overload_undergrad_condition > sunday_morning_in_time_condition and sunday_morning_in_time_overload_undergrad_condition < sunday_morning_out_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time.strftime('%I:%M %p')
                    elif sunday_morning_in_time_overload_undergrad_condition > sunday_morning_out_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time_overload_undergrad_show
                elif sunday_morning_time_in_dt != None and sunday_morning_time_in_overload_grad_dt != None:
                    sunday_morning_in_time_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_in_dt.hour, sunday_morning_time_in_dt.minute)
                    sunday_morning_out_time_condition = datetime(datetime.now().year, month_int, day, sunday_morning_time_out_dt.hour, sunday_morning_time_out_dt.minute)
                    sunday_morning_in_hour = random.randint(sunday_morning_time_in_dt.hour, sunday_morning_time_in_dt.hour)
                    sunday_morning_in_minute = random.randint(0, 59)
                    sunday_morning_in_time = datetime(datetime.now().year, month_int, day, sunday_morning_in_hour, sunday_morning_in_minute)
                    if sunday_morning_in_time_overload_grad_condition < sunday_morning_in_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time_overload_grad_show
                    elif sunday_morning_in_time_overload_grad_condition > sunday_morning_in_time_condition and sunday_morning_in_time_overload_grad_condition < sunday_morning_out_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time.strftime('%I:%M %p')
                    elif sunday_morning_in_time_overload_grad_condition > sunday_morning_out_time_condition:
                        sunday_morning_in_time_show = sunday_morning_in_time_overload_grad_show
                elif sunday_morning_time_in_dt == None and sunday_morning_time_in_overload_undergrad_dt == None:
                    sunday_morning_in_time = ""
                    sunday_morning_in_time_show = ""
                elif sunday_morning_time_in_dt == None and sunday_morning_time_in_overload_grad_dt == None:
                    sunday_morning_in_time = ""
                    sunday_morning_in_time_show = ""
                else:
                    sunday_morning_in_hour = random.randint(sunday_morning_time_in_dt.hour, sunday_morning_time_in_dt.hour)
                    sunday_morning_in_minute = random.randint(0, 59)
                    sunday_morning_in_time = datetime(datetime.now().year, month_int, day, sunday_morning_in_hour, sunday_morning_in_minute)
                    sunday_morning_in_time_show = sunday_morning_in_time.strftime('%I:%M %p')
                

                if sunday_morning_time_out_dt != None and sunday_morning_time_out_overload_undergrad_dt != None:
                    sunday_morning_out_hour = random.randint(sunday_morning_time_out_dt.hour, sunday_morning_time_out_dt.hour)
                    sunday_morning_out_minute = random.randint(0, 59)
                    sunday_morning_out_time = datetime(datetime.now().year, month_int, day, sunday_morning_out_hour, sunday_morning_out_minute)
                    if sunday_morning_out_time_overload_undergrad_condition > sunday_morning_out_time_condition:
                        sunday_morning_out_time_show = sunday_morning_out_time_overload_undergrad_show
                    else:
                        sunday_morning_out_time_show = sunday_morning_out_time.strftime('%I:%M %p')
                elif sunday_morning_time_out_dt != None and sunday_morning_time_out_overload_grad_dt != None:
                    sunday_morning_out_hour = random.randint(sunday_morning_time_out_dt.hour, sunday_morning_time_out_dt.hour)
                    sunday_morning_out_minute = random.randint(0, 59)
                    sunday_morning_out_time = datetime(datetime.now().year, month_int, day, sunday_morning_out_hour, sunday_morning_out_minute)
                    if sunday_morning_out_time_overload_grad_condition > sunday_morning_out_time_condition:
                        sunday_morning_out_time_show = sunday_morning_out_time_overload_grad_show
                    else:
                        sunday_morning_out_time_show = sunday_morning_out_time.strftime('%I:%M %p')

                elif sunday_morning_time_out_dt == None and sunday_morning_time_out_overload_undergrad_dt == None:
                    sunday_morning_out_time = ""
                    sunday_morning_out_time_show = ""
                elif sunday_morning_time_out_dt == None and sunday_morning_time_out_overload_grad_dt == None:
                    sunday_morning_out_time = ""
                    sunday_morning_out_time_show = ""
      
                else:
                    sunday_morning_out_hour = random.randint(sunday_morning_time_out_dt.hour, sunday_morning_time_out_dt.hour)
                    sunday_morning_out_minute = random.randint(0, 59)
                    sunday_morning_out_time = datetime(datetime.now().year, month_int, day, sunday_morning_out_hour, sunday_morning_out_minute)
                    sunday_morning_out_time_show = sunday_morning_out_time.strftime('%I:%M %p')

                if sunday_morning_time_out_dt == None and sunday_morning_time_out_overload_undergrad_dt != None:
                    sunday_morning_out_time = ""
                    sunday_morning_out_time_show = sunday_morning_out_time_overload_undergrad_show
                elif sunday_morning_time_out_dt == None and sunday_morning_time_out_overload_grad_dt != None:
                    sunday_morning_out_time = ""
                    sunday_morning_out_time_show = sunday_morning_out_time_overload_grad_show
                
                if sunday_afternoon_time_in_dt == None and sunday_afternoon_time_in_overload_undergrad_dt != None:
                    sunday_afternoon_in_time = ""
                    sunday_afternoon_in_time_show = sunday_afternoon_in_time_overload_undergrad_show
                elif sunday_afternoon_time_in_dt == None and sunday_afternoon_time_in_overload_grad_dt != None:
                    sunday_afternoon_in_time = ""
                    sunday_afternoon_in_time_show = sunday_afternoon_in_time_overload_grad_show
                    
                elif sunday_afternoon_time_in_dt != None and sunday_afternoon_time_in_overload_undergrad_dt != None:
                    sunday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_in_dt.hour, sunday_afternoon_time_in_dt.minute)
                    sunday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_out_dt.hour, sunday_afternoon_time_out_dt.minute)
                    sunday_afternoon_in_hour = random.randint(sunday_afternoon_time_in_dt.hour, sunday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    sunday_afternoon_in_minute = random.randint(0, 59)
                    sunday_afternoon_in_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_in_hour, sunday_afternoon_in_minute)                    
                    if sunday_afternoon_in_time_overload_undergrad_condition < sunday_afternoon_in_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time_overload_undergrad_show
                    elif sunday_afternoon_in_time_overload_undergrad_condition > sunday_afternoon_in_time_condition and sunday_afternoon_in_time_overload_undergrad_condition < sunday_afternoon_out_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time.strftime('%I:%M %p')
                    elif sunday_afternoon_in_time_overload_undergrad_condition > sunday_afternoon_out_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time.strftime('%I:%M %p')
                        
                elif sunday_afternoon_time_in_dt != None and sunday_afternoon_time_in_overload_grad_dt != None:
                    sunday_afternoon_in_time_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_in_dt.hour, sunday_afternoon_time_in_dt.minute)
                    sunday_afternoon_out_time_condition = datetime(datetime.now().year, month_int, day, sunday_afternoon_time_out_dt.hour, sunday_afternoon_time_out_dt.minute)
                    sunday_afternoon_in_hour = random.randint(sunday_afternoon_time_in_dt.hour, sunday_afternoon_time_in_dt.hour)#reminder to experiment making the random hour to be the same variable for faster looping
                    sunday_afternoon_in_minute = random.randint(0, 59)
                    sunday_afternoon_in_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_in_hour, sunday_afternoon_in_minute)                    
                    if sunday_afternoon_in_time_overload_grad_condition < sunday_afternoon_in_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time_overload_grad_show
                    elif sunday_afternoon_in_time_overload_grad_condition > sunday_afternoon_in_time_condition and sunday_afternoon_in_time_overload_grad_condition < sunday_afternoon_out_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time.strftime('%I:%M %p')
                    elif sunday_afternoon_in_time_overload_grad_condition > sunday_afternoon_out_time_condition:
                        sunday_afternoon_in_time_show = sunday_afternoon_in_time.strftime('%I:%M %p')
                
                elif sunday_afternoon_time_in_dt == None and sunday_afternoon_time_in_overload_undergrad_dt == None:
                    sunday_afternoon_in_time = ""
                    sunday_afternoon_in_time_show = ""
                elif sunday_afternoon_time_in_dt == None and sunday_afternoon_time_in_overload_grad_dt == None:
                    sunday_afternoon_in_time = ""
                    sunday_afternoon_in_time_show = ""

                else:
                    sunday_afternoon_in_hour = random.randint(sunday_afternoon_time_in_dt.hour, sunday_afternoon_time_in_dt.hour)
                    sunday_afternoon_in_minute = random.randint(0, 59)
                    sunday_afternoon_in_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_in_hour, sunday_afternoon_in_minute)
                    sunday_afternoon_in_time_show = sunday_afternoon_in_time.strftime('%I:%M %p')
                

                if sunday_afternoon_time_out_dt != None and sunday_afternoon_time_out_overload_undergrad_dt != None:
                    sunday_afternoon_out_hour = random.randint(sunday_afternoon_time_out_dt.hour, sunday_afternoon_time_out_dt.hour)
                    sunday_afternoon_out_minute = random.randint(0, 59)
                    sunday_afternoon_out_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_out_hour, sunday_afternoon_out_minute)
                    if sunday_afternoon_out_time_overload_undergrad_condition > sunday_afternoon_out_time_condition:
                        sunday_afternoon_out_time_show = sunday_afternoon_out_time_overload_undergrad_show
                    else:
                        sunday_afternoon_out_time_show = sunday_afternoon_out_time.strftime('%I:%M %p')

                elif sunday_afternoon_time_out_dt != None and sunday_afternoon_time_out_overload_grad_dt != None:
                    sunday_afternoon_out_hour = random.randint(sunday_afternoon_time_out_dt.hour, sunday_afternoon_time_out_dt.hour)
                    sunday_afternoon_out_minute = random.randint(0, 59)
                    sunday_afternoon_out_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_out_hour, sunday_afternoon_out_minute)
                    if sunday_afternoon_out_time_overload_grad_condition > sunday_afternoon_out_time_condition:
                        sunday_afternoon_out_time_show = sunday_afternoon_out_time_overload_grad_show
                    else:
                        sunday_afternoon_out_time_show = sunday_afternoon_out_time.strftime('%I:%M %p')


                elif sunday_afternoon_time_out_dt == None and sunday_afternoon_time_out_overload_undergrad_dt == None:
                    sunday_afternoon_out_time = ""
                    sunday_afternoon_out_time_show = ""
                elif sunday_afternoon_time_out_dt == None and sunday_afternoon_time_out_overload_grad_dt == None:
                    sunday_afternoon_out_time = ""
                    sunday_afternoon_out_time_show = ""
                else:
                    sunday_afternoon_out_hour = random.randint(sunday_afternoon_time_out_dt.hour, sunday_afternoon_time_out_dt.hour)
                    sunday_afternoon_out_minute = random.randint(0, 59)
                    sunday_afternoon_out_time = datetime(datetime.now().year, month_int, day, sunday_afternoon_out_hour, sunday_afternoon_out_minute)
                    sunday_afternoon_out_time_show = sunday_afternoon_out_time.strftime('%I:%M %p')

                if sunday_afternoon_time_out_dt == None and sunday_afternoon_time_out_overload_undergrad_dt != None:
                    sunday_afternoon_out_time = ""
                    sunday_afternoon_out_time_show = sunday_afternoon_out_time_overload_undergrad_show
                elif sunday_afternoon_time_out_dt == None and sunday_afternoon_time_out_overload_grad_dt != None:
                    sunday_afternoon_out_time = ""
                    sunday_afternoon_out_time_show = sunday_afternoon_out_time_overload_grad_show


                if sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    times.append((
                    datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                    sunday_morning_in_time_show,
                    sunday_morning_out_time_show,
                    sunday_afternoon_in_time_show,
                    sunday_afternoon_out_time_show,
                    sunday_morning_in_time_overload_undergrad_show,
                    sunday_morning_out_time_overload_undergrad_show,
                    sunday_afternoon_in_time_overload_undergrad_show,
                    sunday_afternoon_out_time_overload_undergrad_show,
                    sunday_morning_in_time_overload_grad_show,
                    sunday_morning_out_time_overload_grad_show,
                    sunday_afternoon_in_time_overload_grad_show,
                    sunday_afternoon_out_time_overload_grad_show
                    ))
                    break
#morning first:
                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break
#afternoon:

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

#Morning and afternoon:

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break



                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time != "" and sunday_morning_out_time != "" and sunday_afternoon_in_time != "" and sunday_afternoon_out_time != "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

#blank morning and afternoon:

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad != "" and sunday_morning_out_time_overload_undergrad != "" and sunday_afternoon_in_time_overload_undergrad != "" and sunday_afternoon_out_time_overload_undergrad != "" \
                    and sunday_morning_in_time_overload_grad == "" and sunday_morning_out_time_overload_grad == "" and sunday_afternoon_in_time_overload_grad == "" and sunday_afternoon_out_time_overload_grad == "":
                    if abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break

                elif sunday_morning_in_time == "" and sunday_morning_out_time == "" and sunday_afternoon_in_time == "" and sunday_afternoon_out_time == "" \
                    and sunday_morning_in_time_overload_undergrad == "" and sunday_morning_out_time_overload_undergrad == "" and sunday_afternoon_in_time_overload_undergrad == "" and sunday_afternoon_out_time_overload_undergrad == "" \
                    and sunday_morning_in_time_overload_grad != "" and sunday_morning_out_time_overload_grad != "" and sunday_afternoon_in_time_overload_grad != "" and sunday_afternoon_out_time_overload_grad != "":
                    if abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                    and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600:
                        times.append((
                            datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                            sunday_morning_in_time_show,
                            sunday_morning_out_time_show,
                            sunday_afternoon_in_time_show,
                            sunday_afternoon_out_time_show,
                            sunday_morning_in_time_overload_undergrad_show,
                            sunday_morning_out_time_overload_undergrad_show,
                            sunday_afternoon_in_time_overload_undergrad_show,
                            sunday_afternoon_out_time_overload_undergrad_show,
                            sunday_morning_in_time_overload_grad_show,
                            sunday_morning_out_time_overload_grad_show,
                            sunday_afternoon_in_time_overload_grad_show,
                            sunday_afternoon_out_time_overload_grad_show
                        ))
                        break


                else:
                    if abs((sunday_morning_in_time - datetime.combine(sunday_morning_in_time.date(), sunday_morning_time_in_dt)).total_seconds()) <= 600 \
                        and abs((sunday_morning_out_time - datetime.combine(sunday_morning_out_time.date(), sunday_morning_time_out_dt)).total_seconds()) <= 600 \
                        and abs((sunday_morning_in_time_overload_grad - datetime.combine(sunday_morning_in_time_overload_grad.date(), sunday_morning_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_morning_out_time_overload_grad - datetime.combine(sunday_morning_out_time_overload_grad.date(), sunday_morning_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_morning_in_time_overload_undergrad - datetime.combine(sunday_morning_in_time_overload_undergrad.date(), sunday_morning_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_morning_out_time_overload_undergrad - datetime.combine(sunday_morning_out_time_overload_undergrad.date(), sunday_morning_time_out_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_in_time - datetime.combine(sunday_afternoon_in_time.date(), sunday_afternoon_time_in_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_out_time - datetime.combine(sunday_afternoon_out_time.date(), sunday_afternoon_time_out_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_in_time_overload_grad - datetime.combine(sunday_afternoon_in_time_overload_grad.date(), sunday_afternoon_time_in_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_out_time_overload_grad - datetime.combine(sunday_afternoon_out_time_overload_grad.date(), sunday_afternoon_time_out_overload_grad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_in_time_overload_undergrad - datetime.combine(sunday_afternoon_in_time_overload_undergrad.date(), sunday_afternoon_time_in_overload_undergrad_dt)).total_seconds()) <= 600 \
                        and abs((sunday_afternoon_out_time_overload_undergrad - datetime.combine(sunday_afternoon_out_time_overload_undergrad.date(), sunday_afternoon_time_out_overload_undergrad_dt)).total_seconds()) <= 600:
                            times.append((
                                datetime(datetime.now().year, month_int, day).strftime('%B %d, %Y'),
                                sunday_morning_in_time_show,
                                sunday_morning_out_time_show,
                                sunday_afternoon_in_time_show,
                                sunday_afternoon_out_time_show,
                                sunday_morning_in_time_overload_undergrad_show,
                                sunday_morning_out_time_overload_undergrad_show,
                                sunday_afternoon_in_time_overload_undergrad_show,
                                sunday_afternoon_out_time_overload_undergrad_show,
                                sunday_morning_in_time_overload_grad_show,
                                sunday_morning_out_time_overload_grad_show,
                                sunday_afternoon_in_time_overload_grad_show,
                                sunday_afternoon_out_time_overload_grad_show
                            ))
                            break
    return times