###################################################################################
# UpdatEngine - Software Packages Deployment and Administration tool              #  
#                                                                                 #
# Copyright (C) Yves Guimard - yves.guimard@gmail.com                             #
#                                                                                 #
# This program is free software; you can redistribute it and/or                   #
# modify it under the terms of the GNU General Public License                     #
# as published by the Free Software Foundation; either version 2                  #
# of the License, or (at your option) any later version.                          #
#                                                                                 #
# This program is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   #
# GNU General Public License for more details.                                    #
#                                                                                 #
# You should have received a copy of the GNU General Public License               #
# along with this program; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. #
###################################################################################

from django.utils.translation import ugettext_lazy as _
from django.db import models
from inventory.models import entity
from django.contrib.auth.models import User

class deployconfig(models.Model):
    unique = True
    choice = (
            ('yes', _('yes')),
            ('no', _('no'))
        )
    name =  models.CharField(max_length='100', verbose_name = _('deployconfig|name'))
    activate_deploy = models.CharField(max_length=3, choices=choice, default='yes', verbose_name = _('deployconfig|activate_deploy'))
    activate_time_deploy = models.CharField(max_length=3, choices=choice, default='no', verbose_name = _('deployconfig|activate_time_deploy'))
    start_time = models.TimeField(verbose_name = _('deployconfig|start_time'))
    end_time = models.TimeField(verbose_name = _('deployconfig|end_time'))
    entity = models.ForeignKey('inventory.entity',null=True, blank=True, default=None, on_delete=models.SET_NULL, verbose_name = _('deployconfig|entity'))
    packageprofile = models.ForeignKey('deploy.packageprofile',null=True, blank=True, default=None,on_delete=models.SET_NULL, 
    verbose_name = _('deployconfig|package profile'), help_text= _('machine|packages profile help text'))
    timeprofile = models.ForeignKey('deploy.timeprofile',null=True, blank=True, default=None, on_delete=models.SET_NULL, verbose_name = _('deployconfig|time deploy profile'))

    class Meta:
        verbose_name = _('deployconfig|deployconfig')
        verbose_name_plural = _('deployconfig|deployconfigs')

    def __unicode__(self):
        return self.activate_deploy

# Create subuser to extend default django user
class subuser(models.Model):
    user = models.OneToOneField(User, related_name='subuser')
    entity = models.ManyToManyField(entity,null=True, blank=True, default=None, verbose_name = _('entity|entity'))
    
    def entities_allowed(self):
        """Return a list composed of all entities allowed for user"""
        if self.user.is_superuser:
            return entity.objects.all()           
        else:
            entity_allowed = list()
            for ent in self.entity.all():
                entity_allowed.append(ent)
                entity_allowed = entity_allowed + ent.get_all_children(ent.get_children(),list())
            return entity_allowed

    def id_entities_allowed(self):
        """Return a list composed of entities allowed id"""
       # if self.user.is_superuser:
        #    return entity.objects.all().values_list('id')
        return list(e.id for e in self.entities_allowed())

    class Meta:
        verbose_name = _('subuser|entity')
        verbose_name_plural = _('subuser|entity')

