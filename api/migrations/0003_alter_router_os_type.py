# Generated by Django 3.2.7 on 2021-09-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_router_os_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='router',
            name='os_type',
            field=models.CharField(choices=[('Linux', 'Linux'), ('IOS', 'Cisco IOS'), ('JunOS', 'Juniper JunOS')], default='Linux', max_length=50),
        ),
    ]
