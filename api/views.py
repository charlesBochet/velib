# -*- coding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def home(request):
    """Home page view"""
    text = """<h1>The Vélib 2.0</h1>
        <p>Bienvenue sur la page d'accueil de l'API</p>"""
    return render(request, 'api/bdd_check.html', locals())
