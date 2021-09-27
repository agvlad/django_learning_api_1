from django.db import models
from django.db.models.deletion import CASCADE


class Router(models.Model):
    OS_TYPE = (
        ('Linux', 'Linux'),
        ('IOS', 'Cisco IOS'),
        ('JunOS', 'Juniper JunOS'),
    )
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    management_ip = models.CharField(max_length=15,
                                     unique=True, null=False)
    os_type = models.CharField(max_length=50, choices=OS_TYPE,
                               default='Linux')

    def __str__(self):
        return f'{self.name} ({self.management_ip})'

    @property
    def networks(self):
        return self.network_set.all()


class Network(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    vlan_tag = models.CharField(max_length=4, unique=True, null=False)
    network_address = models.CharField(max_length=18,
                                       unique=True, null=False)
    router = models.ForeignKey(Router, null=False, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} ({self.network_address})'
