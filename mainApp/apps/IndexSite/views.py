from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
 
def index(request):
    return render(request, "IndexSite/index.html")

def feedback(request):
    return render(request, "IndexSite/feedback.html")

def campus2x(request):
    return render(request, "IndexSite/campus2x.html")

def campus3x(request):
    return render(request, "IndexSite/campus3x.html")