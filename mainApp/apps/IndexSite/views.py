from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
 
def index(request):
    return render(request, "IndexSite/index.html")

def feedback(request):
    return render(request, "IndexSite/feedback.html")

def campus2(request):
    return render(request, "IndexSite/campus2.html")

def campus3(request):
    return render(request, "IndexSite/campus3.html")