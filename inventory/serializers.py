from rest_framework import serializers
from inventory.models import machine


class MachinesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = machine
        fields = ['serial', 'name', 'vendor', 'product', 'domain', 'uuid',
            'username', 'language', 'entity', 'packageprofile', 'timeprofile',
            'lastsave', 'typemachine', 'netsum', 'ossum', 'softsum', 'packages',
            'manualy_created', 'comment']
