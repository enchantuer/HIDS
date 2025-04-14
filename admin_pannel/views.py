from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
import json


def admin_pannel(request):
    users = User.objects.all()
    return render(request, 'admin_pannel/admin_acceuil.html', {'active_page': 'pannel', 'users': users})


def utilisateurs(request):
    users = User.objects.all()
    return render(request, 'admin_pannel/admin_user.html', {'users': users, 'active_page': 'Utilisateurs'})


def verification(request):
    return render(request, 'admin_pannel/admin_verification.html', {'active_page': 'Verification'})


def add_user(request):
    try:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') in ['true', 'on']

        if not firstname or not lastname or not email or not password:
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

        user = User.objects.filter(email=email).first()

        if user:
            user.is_staff = is_staff
            user.first_name = firstname
            user.last_name = lastname
            user.set_password(password)
            user.save()
            action = 'modifié'
        else:
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname,
                is_staff=is_staff
            )
            action = 'ajouté'

        return JsonResponse({
            'id': user.id,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'action': action
        })

    except ValidationError as e:
        return JsonResponse({'error': f'Erreur de validation: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erreur inattendue: {str(e)}'}, status=500)


def verify_old_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('oldPassword')
        user = request.user
        if user.check_password(old_password):
            return JsonResponse({'isValid': True})
        else:
            return JsonResponse({'isValid': False}, status=400)


def check_email_exists(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})


def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def get_user_counts(request):
    admin_count = User.objects.filter(is_staff=True).count()
    user_count = User.objects.filter(is_staff=False).count()
    return JsonResponse({
        'adminCount': admin_count,
        'userCount': user_count
    })


from api.models import Agent

def agents_page(request):
    agents = Agent.objects.all()
    return render(request, 'admin_pannel/admin_agents.html', {'agents': agents, 'active_page': 'Agents'})


def add_agent(request):
    try:
        name = request.POST.get('name')
        system = request.POST.get('system')
        adresse = request.POST.get('adresse')
        down = request.POST.get('down') in ['true', 'on']

        if not name or not system or not adresse:
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

        agent_id = request.POST.get('agent_id')
        if agent_id:
            agent = Agent.objects.get(pk=agent_id)
            agent.name = name
            agent.system = system
            agent.adresse = adresse
            agent.down = down
            agent.save()
            action = "modifié"
        else:
            agent = Agent.objects.create(
                name=name,
                system=system,
                adresse=adresse,
                down=down
            )
            action = "ajouté"

        return JsonResponse({
            'id': agent.id,
            'name': agent.name,
            'system': agent.system,
            'adresse': agent.adresse,
            'down': agent.down,
            'action': action
        })

    except Exception as e:
        return JsonResponse({'error': f'Erreur inattendue: {str(e)}'}, status=500)


def delete_agent(request, agent_id):
    if request.method == 'POST':
        try:
            agent = Agent.objects.get(pk=agent_id)
            agent.delete()
            return JsonResponse({'success': True})
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def get_agent_counts(request):
    actif = Agent.objects.filter(down=True).count()
    inactif = Agent.objects.filter(down=False).count()
    return JsonResponse({'actifCount': actif, 'inactifCount': inactif})
