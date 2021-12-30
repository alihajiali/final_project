# Generated by Django 4.0 on 2021-12-30 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_phone_number'),
        ('shop', '0004_remove_product_images_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_market', to='accounts.user'),
        ),
    ]
