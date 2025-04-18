from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
import json
import os


@staff_member_required
def admin_panel(request):
    users = User.objects.all()
    return render(request, 'admin_panel/admin_home.html', {'active_page': 'pannel', 'users': users})

@staff_member_required
def utilisateurs(request):
    users = User.objects.all()
    return render(request, 'admin_panel/admin_user.html', {'users': users, 'active_page': 'Utilisateurs'})

@staff_member_required
def verification(request):
    return render(request, 'admin_panel/admin_verification.html', {'active_page': 'Verification'})

@staff_member_required
def add_user(request):
    try:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') in ['true', 'on']

        if not firstname or not lastname or not email:
            return JsonResponse({'error': 'Tous les champs excepter le password sont requis'}, status=400)

        user_id = request.POST.get('id')
        if user_id:
            user = User.objects.get(pk=user_id)
            user.is_staff = is_staff
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            if password:
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
            'action': action,
            'is_staff': user.is_staff,
            'email': user.email,
        })

    except ValidationError as e:
        return JsonResponse({'error': f'Erreur de validation: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erreur inattendue: {str(e)}'}, status=500)

@staff_member_required
def verify_old_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('oldPassword')
        user = request.user
        if user.check_password(old_password):
            return JsonResponse({'isValid': True})
        else:
            return JsonResponse({'isValid': False}, status=400)

@staff_member_required
def check_email_exists(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})

@staff_member_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@staff_member_required
def get_user_counts(request):
    admin_count = User.objects.filter(is_staff=True).count()
    user_count = User.objects.filter(is_staff=False).count()
    return JsonResponse({
        'adminCount': admin_count,
        'userCount': user_count
    })


from api.models import Agent

@staff_member_required
def agents_page(request):
    agents = Agent.objects.all()
    return render(request, 'admin_panel/admin_agents.html', {'agents': agents, 'active_page': 'Agents'})

@staff_member_required
def add_agent(request):
    try:
        name = request.POST.get('name')
        system = request.POST.get('system')
        adresse = request.POST.get('adresse')
        down = not request.POST.get('is_up') in ['true', 'on']

        if not name or not system or not adresse:
            return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

        agent_id = request.POST.get('id')

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

@staff_member_required
def delete_agent(request, agent_id):
    if request.method == 'POST':
        try:
            agent = Agent.objects.get(pk=agent_id)
            agent.delete()
            return JsonResponse({'success': True})
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Agent introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@staff_member_required
def get_agent_counts(request):
    actif = Agent.objects.filter(down=True).count()
    inactif = Agent.objects.filter(down=False).count()
    return JsonResponse({'actifCount': actif, 'inactifCount': inactif})

@staff_member_required
def update_config(request):
    with open('dossier_partage/config.json', 'r') as f:
       data = json.load(f)
    key = request.POST.get('editKey')
    print("Key:", key)
    if key == "yara":
        data['YARA'] = not data['YARA']
    elif key == "suricata":
        data['SURICATA'] = not data['SURICATA']
    elif key == "snort":
        data['SNORT'] = not data['SNORT']
    elif key == "virustotal":
        data['VIRUS_TOTAL'] = not data['VIRUS_TOTAL']
    elif key == "ipdb":
        data['IPDB'] = not data['IPDB']
    elif key == "custom":
        data['LOCAL'] = not data['LOCAL']
    elif key == "ope":
        data['IA'] = not data['IA']
    elif key == "modele1":
        data['RANDOM_FOREST'] = not data['RANDOM_FOREST']
    elif key == "modele2":
        data['SUPPORT_VECTOR_MACHINE'] = not data['SUPPORT_VECTOR_MACHINE']
    else:
        return JsonResponse({'error': f"Clé '{key}' inconnue"}, status=400)

    print("Data:", data)
    with open('dossier_partage/config.json', 'w') as f:
        json.dump(data, f, indent=4)
    return JsonResponse({'success': True}, status=200)

@staff_member_required
def get_config(request):
    config_path = 'dossier_partage/config.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return JsonResponse(config)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        return JsonResponse({'error': str(e)}, status=500)