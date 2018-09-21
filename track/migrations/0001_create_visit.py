# Generated by Django 2.0 on 2018-09-21 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('path', models.CharField(blank=True, max_length=256, null=True)),
                ('ip_hash', models.CharField(blank=True, max_length=64, null=True)),
                ('referer', models.CharField(blank=True, max_length=256, null=True)),
                ('country', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('agent', models.CharField(blank=True, max_length=1024, null=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
    ]