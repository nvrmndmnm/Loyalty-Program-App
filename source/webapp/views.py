from django.shortcuts import render


def index_view(request):
    return render(request, 'index.html')


def error_401(request, exception):
    return render(request, 'errors/401.html')


def error_403(request, exception):
    return render(request, 'errors/403.html')


def error_404(request, exception):
    return render(request, 'errors/404.html')


def error_500(request):
    return render(request, 'errors/500.html')
