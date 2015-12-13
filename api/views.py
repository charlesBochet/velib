from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    """Home page view"""
    text = """<h1>The Vélib 2.0</h1>
        <p>Bienvenue sur la page d'accueil de l'API</p>"""
    return HttpResponse(text)

