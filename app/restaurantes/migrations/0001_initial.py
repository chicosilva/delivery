# Generated by Django 3.0.5 on 2020-04-24 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('data_cancelamento', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=90)),
                ('telefone', models.EmailField(max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
