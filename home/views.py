from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/base.html')

def gwm(request):
    print("inside the nrw ")
    return render(request, 'home/content/gwm.html')

def rwm(request):
    print("inside the nrw ")
    return render(request, 'home/content/rwm.html')

def wrm(request):    
    print("inside the nrw ")
    return render(request, 'home/content/wrm.html')

def shsd(request):
    print("inside the nrw ")    
    return render(request, 'home/content/shsd.html')
def basic(request):
    print("inside the nrw ")    
    return render(request, 'home/content/basic.html')

def about(request):
    print("inside the nrw ")    
    return render(request, 'home/content/about.html')

def contact(request):
    print("inside the nrw ")    
    return render(request, 'home/content/contact.html')
