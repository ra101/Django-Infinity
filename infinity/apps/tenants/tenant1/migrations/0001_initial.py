# Generated by Django 3.2.6 on 2022-06-02 08:00

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
                ('alive', models.BooleanField(default=True, editable=False)),
                ('data', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]