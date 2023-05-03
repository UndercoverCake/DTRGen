from django.shortcuts import render


def adminpanel(request):
  return render(request, 'adminpanel.html')

def draft(request):
  return render(request, 'draft.html')

def form(request):
  return render(request, 'form.html')

def home(request):
  return render(request, 'homepage.html')

def login2(request):
  return render(request, 'login.html')

def myprofile(request):
  return render(request, 'myprofile.html')

def preview(request):
  return render(request, 'preview.html')
