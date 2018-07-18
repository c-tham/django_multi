from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
 
def index(request):
    context = {
        "name" : "IndexSite"
    }
    return render(request, "IndexSite/index.html", context)
