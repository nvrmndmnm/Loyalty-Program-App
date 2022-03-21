from django.shortcuts import render


def index_view(request):
    return render(request, 'landing_page.html')
