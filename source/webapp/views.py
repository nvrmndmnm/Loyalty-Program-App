from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')
