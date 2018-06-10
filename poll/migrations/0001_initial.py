# Generated by Django 2.0.6 on 2018-06-09 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=25)),
                ('prenom', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Electeur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('palce_of_birth', models.CharField(max_length=15)),
                ('picture', models.ImageField(upload_to='faces/')),
                ('status', models.CharField(choices=[('Agent', 'Agent'), ('President', 'Surpeme court présidents'), ('Voter', 'voter')], default='Voter', max_length=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=45)),
                ('p_acronyme', models.CharField(max_length=5)),
                ('p_logo', models.ImageField(upload_to='logos/')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Party')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Electeur')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Party'),
        ),
    ]
