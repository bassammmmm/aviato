# Generated by Django 4.1.1 on 2022-10-05 12:08

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_usercustom_city_remove_usercustom_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercustom',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='image',
            field=models.ImageField(null=True, upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
