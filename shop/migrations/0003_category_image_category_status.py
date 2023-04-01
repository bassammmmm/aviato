# Generated by Django 4.1.1 on 2022-10-01 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_productimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.CharField(blank=True, choices=[('True', 'True'), ('False', 'False')], max_length=20, null=True),
        ),
    ]
