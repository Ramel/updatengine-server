# Generated by Django 4.2.7 on 2024-03-28 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20220411_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='uninstall',
            field=models.CharField(blank=True, default='undefined', max_length=800, null=True, verbose_name='software|uninstall'),
        ),
    ]
