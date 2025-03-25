from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=60)
    add_date = models.DateTimeField(auto_now_add=True)
    system =models.CharField(max_length=50)
    down = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Alert(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    source = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    level = models.IntegerField()
    pcap = models.FileField(upload_to="static/alerts/%y/%m/%d", null=True, blank=True)

    def __str__(self):
        return str(self.id)

class LogNbRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    nbRequests = models.IntegerField()

    def __str__(self):
        return f'{self.agent.name} : {self.nbRequests} requests'