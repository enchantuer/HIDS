from collections import defaultdict

from django.shortcuts import render

from api.models import Alert, Agent, LogNbRequest

from django.db.models.functions import TruncHour
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from dashboard.models import Alert, Agent
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.
@login_required(login_url=reverse_lazy("login"))
def index(request):
    # Count the number of alert per hour for the last 7 hours
    def alert_count_per_hour(duration):
        # Define the hour range from the last duration hours this hour included
        last_hours = now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=duration - 1)
        # Filter the entry within the range and group by hour
        alerts_per_hour = (
            Alert.objects.filter(created_at__gte=last_hours)
            .annotate(hour=TruncHour('created_at'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )
        # Initiate default value to 0
        counts = defaultdict(int)
        for alerts in alerts_per_hour:
            counts[alerts['hour'].isoformat()] = alerts['count']

        # Create the dict to store the number of alert per hour with UTC timestamps
        hours = []
        count_per_hour = []
        for i in range(duration):
            hour = (last_hours + timedelta(hours=i)).isoformat()
            hours.append(hour)
            count_per_hour.append(counts[hour])
        return hours, count_per_hour

    # Count the number of alert per type of alert
    def alert_count_per_type():
        alerts_per_type = (
            Alert.objects.values('type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        alerts_types = [entry['type'] for entry in alerts_per_type]
        alerts_counts = [entry['count'] for entry in alerts_per_type]

        return [alerts_types, alerts_counts]

    # Summarize the number of request compare to the number of alert per agent
    def agent_stats(duration):
        last_hours = now() - timedelta(hours=duration)
        # Get all agent (id, name)
        agents = Agent.objects.order_by('name', 'id').values_list('id', 'name')
        # Count alerts for this day per agent
        alerts_per_agent = (
            Alert.objects.filter(created_at__gte=last_hours)
            .values('agent__id')
            .annotate(count=Count('id'))
            .order_by('agent__name', 'agent__id')
        )
        # Count request for this day per agent
        requests_per_agent = (
            LogNbRequest.objects.filter(created_at__gte=last_hours)
            .values('agent__id')
            .annotate(count=Sum('nbRequests'))  # Sum the request per agent
            .order_by('agent__name', 'agent__id')
        )

        alert_counts = {entry['agent__id']: entry['count'] for entry in alerts_per_agent}
        request_counts = {entry['agent__id']: entry['count'] for entry in requests_per_agent}

        alert_per_agent = []
        request_without_alert_per_agent = []
        for agent in agents:
            alert_per_agent.append(alert_counts.get(agent[0], 0))
            request_without_alert_per_agent.append(max(0, request_counts.get(agent[0], 0) - alert_counts.get(agent[0], 0)))

        return [
            [name for _, name in agents],
            {
                "alert_per_agent": alert_per_agent,
                "request_without_alert_per_agent": request_without_alert_per_agent
            }
        ]

    context = {
        "chart": {
            "alert_type": alert_count_per_type(),
            "agent_stats": agent_stats(24),
            "ia_stats": [
                {
                    "name": "Model 1",
                    "data": [65, 59, 90, 81, 56, 55, 40]
                },
                {
                    "name": "Model 2",
                    "data": [28, 48, 40, 19, 96, 27, 100]
                }
            ],
            "alert_evolution": alert_count_per_hour(7),
        }
    }
    return render(request, "dashboard/index.html", context)