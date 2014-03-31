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
from inventory.models import entity, machine, net, software, osdistribution
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import ugettext_lazy as _
from inventory.filters import enableFilter, as_or_notFilter, softwareFilter, versionFilter
from inventory.filters import (entityFilter, domainFilter,usernameFilter,languageFilter,typemachineFilter,\
        osdistributionFilter, timeprofileFilter,packageprofileFilter, hostFilter,\
        osnameFilter,osversionFilter,osarchFilter)
from deploy.models import package
class ueAdmin(admin.ModelAdmin):
    list_max_show_all = 500
    list_per_page = 50
    actions_selection_counter = True
    list_select_related = True

    def get_export_as_csv_filename(self, request, queryset):
        return 'inventory'

class netInline(admin.TabularInline):
    model = net
    max_num = 5000
    extra = 0
    readonly_fields = ('manualy_created',)

class osInline(admin.TabularInline):
    model = osdistribution
    max_num = 5000
    extra = 0
    readonly_fields = ('manualy_created',)

class softInline(admin.TabularInline):
    model = software
    max_num = 10000
    extra = 0
    readonly_fields = ('name', 'version', 'uninstall', 'manualy_created',)
    # Uncomment when django bug number #20807 will be fixed
    #def has_add_permission(self, request):
    #            return False

class entityAdmin(ueAdmin):
    fields = ['name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile']
    list_display = ('name','description','parent','packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    list_editable = ('packageprofile','force_packageprofile','timeprofile','force_timeprofile')
    ordering =('name',)

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        if request.user.is_superuser:
            return entity.objects.all()
        else:
            return entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed)
    
    def get_form(self, request, obj=None): 
        form = super(entityAdmin, self).get_form(request, obj) 
        if obj is not None:
            if request.user.is_superuser: 
                form.base_fields["parent"].queryset = entity.objects.exclude(pk__in = obj.id_all_children()).exclude(pk = obj.id) 
            else: 
                form.base_fields["parent"].queryset = entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed).\
                        exclude(pk__in = obj.id_all_children).\
                        exclude(pk = obj.id).\
                        order_by('name').distinct()
                form.base_fields["parent"].required = True
                form.base_fields["parent"].empty_label = None
        else:
            if request.user.is_superuser:
                return form
            else:
                form.base_fields["parent"].queryset = entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed).\
                        order_by('name').distinct() 
                form.base_fields["parent"].empty_label = None

        return form 


class machineAdmin(ueAdmin):
    select_related = True
    fields = ['name', 'serial','uuid','domain','username','language', 'vendor','product','manualy_created','entity','typemachine','timeprofile','packageprofile','packages']
    list_display = ('lastsave','entity','name','domain','username','vendor','product','typemachine','packageprofile','timeprofile')
    list_editable = ('entity','packageprofile','timeprofile')
    list_filter = (('lastsave', DateFieldListFilter), entityFilter, domainFilter,usernameFilter,languageFilter,typemachineFilter,osdistributionFilter, timeprofileFilter,packageprofileFilter, enableFilter, as_or_notFilter, softwareFilter, versionFilter)
    search_fields = ('name', 'serial','vendor','product','domain','username','language')
    readonly_fields = ('typemachine', 'manualy_created',)
    inlines = [osInline, netInline, softInline]
    filter_horizontal = ('packages',)
    date_hierarchy = 'lastsave'
    ordering =('-lastsave',)
    actions = ['force_contact', 'force_wakeup']

    def queryset(self, request):
        # Re-create queryset with entity list returned by list_entities_allowed
        if request.user.is_superuser:
            return machine.objects.all()
        else:
            return machine.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed)
   
    def force_wakeup(self, request, queryset):
        for machine in queryset:
            machine.wakeup()
    force_wakeup.short_description = _('force_wakeup')

    def force_contact(modeladmin, request, queryset):
        for machine in queryset:
            machine.force_contact()
    force_contact.short_description = _('force_inventory')
    
       
    def get_changelist_formset(self, request, **kwargs):
        formset = super(machineAdmin, self).get_changelist_formset(request, **kwargs)
        if request.user.is_superuser:
            return formset
        formset.form.base_fields["entity"].queryset = entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct()
        formset.form.base_fields["entity"].empty_label = None
        return formset

    def get_form(self, request, obj=None): 
        form = super(machineAdmin, self).get_form(request, obj) 
        if request.user.is_superuser: 
            return form
        else: 
            # Show only entites allowed if not superuser
            form.base_fields["entity"].queryset = entity.objects.filter(pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct() 
            form.base_fields["entity"].empty_label = None
            
            # Show only entites allowed if not superuser
            form.base_fields["packages"].queryset = package.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct() 
        return form 

class netAdmin(ueAdmin):
    list_display = ('ip','mask','mac','host')
    search_fields = ('ip','mask','mac','host__name')
    list_filter = (hostFilter,)
    readonly_fields = ('manualy_created',)
    ordering =('ip',)

    def queryset(self, request):
        if request.user.is_superuser:
            return net.objects.all()
        else:
            return net.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)
    
    def get_form(self, request, obj=None): 
        form = super(netAdmin, self).get_form(request, obj) 
        if request.user.is_superuser: 
            return form
        else: 
            form.base_fields["host"].queryset = machine.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct() 
            form.base_fields["host"].empty_label = None
        return form 

class osAdmin(ueAdmin):
    list_display = ('name','version','arch','systemdrive','host')
    search_fields = ('name','version','arch','systemdrive','host__name')
    list_filter = (osnameFilter,osversionFilter,osarchFilter,hostFilter)
    readonly_fields = ('manualy_created',)
    ordering =('name',)

    def queryset(self, request):
        if request.user.is_superuser:
            return osdistribution.objects.all()
        else:
            return osdistribution.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)
    
    def get_form(self, request, obj=None): 
        form = super(osAdmin, self).get_form(request, obj) 
        if request.user.is_superuser: 
            return form
        else: 
            form.base_fields["host"].queryset = machine.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct() 
            form.base_fields["host"].empty_label = None
        return form 

class softwareAdmin(ueAdmin):
    list_display = ('name','version','host')
    search_fields = ('name','version','host__name')
    list_filter = (hostFilter,)
    readonly_fields = ('manualy_created',)
    ordering =('name',)

    def queryset(self, request):
        if request.user.is_superuser:
            return software.objects.all()
        else:
            return software.objects.filter(host__entity__pk__in = request.user.subuser.id_entities_allowed)
    
    def get_form(self, request, obj=None): 
        form = super(softwareAdmin, self).get_form(request, obj) 
        if request.user.is_superuser: 
            return form
        else: 
            form.base_fields["host"].queryset = machine.objects.filter(entity__pk__in = request.user.subuser.id_entities_allowed).order_by('name').distinct() 
            form.base_fields["host"].empty_label = None
        return form 

admin.site.register(osdistribution,osAdmin)
admin.site.register(machine, machineAdmin)
admin.site.register(entity, entityAdmin)
admin.site.register(net, netAdmin)
admin.site.register(software, softwareAdmin)
