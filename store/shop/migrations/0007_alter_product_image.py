# Generated by Django 4.0 on 2022-01-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to='products/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
