from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Alert

@receiver(post_save, sender=Alert)
def trigger_ws_on_alert(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        print("[!] Channel layer non initialisé")
        return

    async_to_sync(channel_layer.group_send)(
        "alerts",
        {
            "type": "send_alert",
            "message": {
                "alert": instance.to_dict(),
                "operation": "create" if created else "update",
            }
        }
    )
