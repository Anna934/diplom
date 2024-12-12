# Generated by Django 5.1.3 on 2024-12-02 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=80, unique=True)),
                ('hashed_password', models.CharField(max_length=128)),
            ],
        ),
    ]
