# Generated by Django 2.0.6 on 2018-06-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electeur',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
