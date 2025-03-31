from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def get_stats():
    return {
        "agents_count": Agent.objects.all().count(),
        "agents_down_count": Agent.objects.filter(down=True).count(),
        "alerts_count": Alert.objects.all().count(),
    }

def send_stats(channel_layer):
    async_to_sync(channel_layer.group_send)(
        "stats",
        {
            "type": "send_stats",
            "message": get_stats(),
        }
    )

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=60)
    add_date = models.DateTimeField(auto_now_add=True)
    system =models.CharField(max_length=50)
    down = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        channel_layer = get_channel_layer()
        send_stats(channel_layer)



class Alert(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    level = models.IntegerField()
    pcap = models.FileField(upload_to="static/alerts/%y/%m/%d", null=True, blank=True)

    def save(self, *args, **kwargs):
        is_update = self.pk is not None and Alert.objects.filter(pk=self.pk).exists()

        super().save(*args, **kwargs)

        # Envoyer une notification WebSocket
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "alerts",
            {
                "type": "send_alert",
                "message": {
                    "alert": self.to_dict(),
                    "operation": "update" if is_update else "create",
                }
            }
        )

        send_stats(channel_layer)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "agent__id": self.agent.id,
            "agent__name": self.agent.name,
            "source": self.source,
            "type": self.type,
            "description": self.description,
            "level": self.level,
            "pcap": self.pcap.url if self.pcap else None,
        }


    def __str__(self):
        return str(self.id)

class LogNbRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    nbRequests = models.IntegerField()

    def __str__(self):
        return f'{self.agent.name} : {self.nbRequests} requests'