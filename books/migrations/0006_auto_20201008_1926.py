# Generated by Django 2.2.4 on 2020-10-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20201008_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookuserlist',
            name='status',
            field=models.CharField(choices=[('kutuphane', 'Kütüphanem')], max_length=10),
        ),
        migrations.AlterField(
            model_name='bookuserlist',
            name='status2',
            field=models.CharField(choices=[('bitenler', 'Bitenler'), ('okunacaklar', 'Okunacaklar'), ('simdi_okuduklarım', 'Şimdi Okuduklarım')], max_length=30),
        ),
    ]