from django.shortcuts import render

from api.models import Alert


# Create your views here.
def index(request):
    context = {
        "alerts": Alert.objects.all().order_by('-created_at', '-id')
    }
    return render(request, "alerts/index.html", context)