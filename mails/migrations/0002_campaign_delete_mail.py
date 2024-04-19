# Generated by Django 5.0.4 on 2024-04-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('sent', models.IntegerField()),
                ('seen', models.IntegerField()),
                ('replied', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Mail',
        ),
    ]