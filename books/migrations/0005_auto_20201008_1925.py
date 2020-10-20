# Generated by Django 2.2.4 on 2020-10-08 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_bookuserlist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookuserlist',
            name='status2',
            field=models.CharField(choices=[('kutuphane', 'Kütüphanem')], default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookuserlist',
            name='status',
            field=models.CharField(default='kutuphane', max_length=10),
        ),
    ]
