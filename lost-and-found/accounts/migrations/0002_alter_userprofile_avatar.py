# Generated by Django 5.1.5 on 2025-01-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='accounts/user_default.jpg', upload_to='accounts/'),
        ),
    ]
