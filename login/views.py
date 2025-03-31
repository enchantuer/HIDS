from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige vers la page de tableau de bord
        else:
            # Affiche un message d'erreur
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, "registration/login.html")
