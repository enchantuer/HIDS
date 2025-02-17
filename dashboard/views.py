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
        "alerts": Alert.objects.all()
    }
    return render(request, "dashboard/index.html", context)