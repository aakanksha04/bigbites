# Generated by Django 3.1 on 2020-08-27 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
