from django.http import HttpResponse
from django.shortcuts import render

from dashboard.models import Alert, Agent


# Create your views here.
def index(request):
    """
    [
        {
            "time": "Jan 22 2024 09:50:20",
            "agent": 10,
            "agent_name": "Debian Server",
            "source": "IA",
            "type": "DDOS",
            "description": "Signed Script Proxy Execute C://",
            "level": 8,
            "id": 1234
        }
    ]
    """
    # return HttpResponse("Hello, world. You're at the dashboard index.")
    context = {
        "alerts_number": Alert.objects.count(),
        "agents_number": Agent.objects.count(),
        "agents_down_number": Agent.objects.filter(down=True).count(),
        "alerts": Alert.objects.all(),
        "chart": {
            "alert_type": [30, 30, 10, 30],
            "agent_stats": {
                "normal": [40, 100, 45, 30, 60, 130, 39, 50, 90, 100, 34, 60, 110],
                "alert": [30, 30, 10, 30, 40, 119, 4, 30, 30, 10, 30, 40, 100]
            },
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
            "alert_evolution": [100, 80, 60, 90, 40, 70, 80]
        }
    }
    return render(request, "dashboard/index.html", context)