import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.nb_of_alerts = self.scope['url_route']['kwargs'].get('nb_of_alerts') or 0
        #
        # self.group_name = f'alerts_{self.nb_of_alerts}' if self.nb_of_alerts else 'alerts'
        # await self.channel_layer.group_add(self.group_name, self.channel_name)

        # cached_alerts = cache.get('top_alerts') or []
        # await self.send(text_data=json.dumps({"alerts": cached_alerts}))

        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()  # Accepte la connexion WebSocket

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    async def send_alert(self, event):
        """ Envoie une alerte au client WebSocket """
        # alert = event['message']
        #
        # if self.nb_of_alerts == 0:
        #     await self.send(text_data=json.dumps({"alert": alert}))
        #     return
        #
        # cached_alerts = cache.get('top_alerts')
        # if alert["id"] in [a["id"] for a in cached_alerts[:self.nb_of_alerts]]:
        #     await self.send(text_data=json.dumps({"alert": alert}))

        await self.send(text_data=json.dumps(event['message']))


class StatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stats", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stats", self.channel_name)

    async def send_stats(self, event):
        """ Envoie les statistiques au client WebSocket """
        await self.send(text_data=json.dumps(event["message"]))