# Generated by Django 2.2.6 on 2019-10-11 10:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_beta_tester'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apelido',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Nome Fantasia'),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=200),
        ),
    ]