from django.shortcuts import render
from django.http import JsonResponse
from api.models import Agent, Alert
from api.models import get_stats as api_get_stats
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

def str_to_bool(value):
    if value is None:
        return None
    return value.lower() in ["true", "1", "yes"]

# Create your views here.
def get_agents(request):
    # Récupérer les filtres optionnels
    id = request.GET.get('id')
    name = request.GET.get('name')
    down = request.GET.get('down')
    ordering = request.GET.get('ordering', '-id')  # Tri par défaut (plus récent en premier)
    # Récupérer les dates de début et de fin de la requête
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Filtrer les alertes
    agents = Agent.objects.all()
    if id:
        agents = agents.filter(id=id)
    if name:
        agents = agents.filter(name=name)
    if down:
        agents = agents.filter(down=str_to_bool(down))
    # Filtrage par plage de dates si les deux paramètres sont présents
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        agents = agents.filter(add_date__gte=start_date)  # >= start_date
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        agents = agents.filter(add_date__lte=end_date)  # <= end_date

    # Trier les résultats
    agents = agents.order_by(ordering)

    # Pagination
    page_size = request.GET.get('page_size', 10)  # Nombre d'éléments par page (par défaut 10)
    page_number = request.GET.get('page', 1)  # Numéro de page (par défaut 1)

    # S'assurer que page_size et page_number sont des entiers
    try:
        page_size = int(page_size)
        page_number = int(page_number)
    except ValueError:
        page_size = 10
        page_number = 1

    paginator = Paginator(agents, page_size)  # Diviser les alertes en pages
    page = paginator.get_page(page_number)  # Obtenir la page demandée

    data = list(page.object_list.values('id', 'name', 'system', 'down'))
    return JsonResponse({
        "agents": data,
        'pagination': {
            'page': page.number,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_agents': paginator.count
        }
    })

def get_alerts(request):
    # Récupérer les filtres optionnels
    id = request.GET.get('id')
    agent_id = request.GET.get('agent_id')
    agent_name = request.GET.get('agent_name')
    level = request.GET.get('level')
    type_alert = request.GET.get('type')
    source_alert = request.GET.getlist('source')
    print(source_alert)
    ordering = request.GET.get('ordering', '-created_at')  # Tri par défaut (plus récent en premier)
    # Récupérer les dates de début et de fin de la requête
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Filtrer les alertes
    alerts = Alert.objects.all()
    if id:
        alerts = alerts.filter(id=id)
    if agent_id:
        alerts = alerts.filter(agent__id=agent_id)
    if agent_name:
        alerts = alerts.filter(agent__name=agent_name)
    if level:
        alerts = alerts.filter(level=level)
    if type_alert:
        alerts = alerts.filter(type__icontains=type_alert)
    if source_alert:
        source_filter = Q()
        for source in source_alert:
            source_filter |= Q(source__iexact=source)
        alerts = alerts.filter(source_filter)
    # Filtrage par plage de dates si les deux paramètres sont présents
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        alerts = alerts.filter(created_at__gte=start_date)  # >= start_date
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        alerts = alerts.filter(created_at__lte=end_date)  # <= end_date

    # Trier les résultats
    alerts = alerts.order_by(ordering)

    # Pagination
    page_size = request.GET.get('page_size', 10)  # Nombre d'éléments par page (par défaut 10)
    page_number = request.GET.get('page', 1)  # Numéro de page (par défaut 1)

    # S'assurer que page_size et page_number sont des entiers
    try:
        page_size = int(page_size)
        page_number = int(page_number)
    except ValueError:
        page_size = 10
        page_number = 1

    paginator = Paginator(alerts, page_size)  # Diviser les alertes en pages
    page = paginator.get_page(page_number)  # Obtenir la page demandée

    # Construire la réponse JSON
    data = list(page.object_list.values('created_at', 'agent__id', 'agent__name', 'source', 'type', 'description', 'level', 'id'))
    return JsonResponse({
        "alerts": data,
        'pagination': {
            'page': page.number,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_alerts': paginator.count
        }
    })

def get_stats(request):
    return JsonResponse(api_get_stats())