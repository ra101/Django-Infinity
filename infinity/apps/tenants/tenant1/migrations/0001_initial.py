# Generated by Django 3.2.6 on 2022-06-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleForTenant1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Example Model for Tenant 1',
                'verbose_name_plural': 'Example Model for Tenant 1',
            },
        ),
    ]
