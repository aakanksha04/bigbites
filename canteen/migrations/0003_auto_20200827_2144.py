# Generated by Django 3.1 on 2020-08-27 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0002_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]