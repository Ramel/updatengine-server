# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 17:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeprofile',
            name='entity',
            field=models.ManyToManyField(blank=True, related_name='time_profile_entity', to='inventory.entity', verbose_name='timeprofile|entity'),
        ),
        migrations.AddField(
            model_name='packagewakeonlan',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='packagewakonelan| condition last editor'),
        ),
        migrations.AddField(
            model_name='packagewakeonlan',
            name='entity',
            field=models.ManyToManyField(blank=True, related_name='packagewakonelan_entity', to='inventory.entity', verbose_name='packagewakonelan|entity'),
        ),
        migrations.AddField(
            model_name='packagewakeonlan',
            name='machines',
            field=models.ManyToManyField(blank=True, to='inventory.machine', verbose_name='packagewakeonlan|machines to start'),
        ),
        migrations.AddField(
            model_name='packageprofile',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='packageprofile| condition last editor'),
        ),
        migrations.AddField(
            model_name='packageprofile',
            name='entity',
            field=models.ManyToManyField(blank=True, related_name='package_profile_entity', to='inventory.entity', verbose_name='packageprofile|entity'),
        ),
        migrations.AddField(
            model_name='packageprofile',
            name='packages',
            field=models.ManyToManyField(blank=True, to='deploy.package', verbose_name='packageprofile|packages'),
        ),
        migrations.AddField(
            model_name='packageprofile',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='deploy.packageprofile', verbose_name='packageprofile|parent'),
        ),
        migrations.AddField(
            model_name='packagehistory',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.machine', verbose_name='packagehistory|machine'),
        ),
        migrations.AddField(
            model_name='packagehistory',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='deploy.package', verbose_name='packagehistory|package'),
        ),
        migrations.AddField(
            model_name='packagecondition',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='packagecondition| condition last editor'),
        ),
        migrations.AddField(
            model_name='packagecondition',
            name='entity',
            field=models.ManyToManyField(blank=True, to='inventory.entity', verbose_name='packagecondition|entity'),
        ),
        migrations.AddField(
            model_name='package',
            name='conditions',
            field=models.ManyToManyField(blank=True, to='deploy.packagecondition', verbose_name='package|conditions'),
        ),
        migrations.AddField(
            model_name='package',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='package| package last editor'),
        ),
        migrations.AddField(
            model_name='package',
            name='entity',
            field=models.ManyToManyField(blank=True, to='inventory.entity', verbose_name='package|entity'),
        ),
        migrations.AddField(
            model_name='impex',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='impex| condition last editor'),
        ),
        migrations.AddField(
            model_name='impex',
            name='entity',
            field=models.ManyToManyField(blank=True, related_name='impex_entity', to='inventory.entity', verbose_name='impex|entity'),
        ),
        migrations.AddField(
            model_name='impex',
            name='package',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='deploy.package', verbose_name='impex|package'),
        ),
    ]