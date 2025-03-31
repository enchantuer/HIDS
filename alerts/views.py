from django.shortcuts import render

from api.models import Alert

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.
@login_required(login_url=reverse_lazy("login"))
def index(request):
    context = {
        "alerts": Alert.objects.all().order_by('-created_at', '-id')
    }
    return render(request, "alerts/index.html", context)