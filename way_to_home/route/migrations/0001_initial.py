# Generated by Django 2.1.4 on 2018-12-18 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
        ('way', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('transport_id', models.PositiveIntegerField(null=True)),
                ('position', models.PositiveSmallIntegerField()),
                ('end_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_routes', to='place.Place')),
                ('start_place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_routes', to='place.Place')),
                ('way', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='way.Way')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
