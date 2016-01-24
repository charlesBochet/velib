from django.shortcuts import render


# Create your views here.
def home(request):
    """Home page view"""
    return render(request, 'interface/home.html', locals())


def statusmap(request):
    """Status Map page view"""
    return render(request, 'interface/statusMap.html', locals())
