# Generated by Django 4.1.3 on 2022-11-14 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0004_alter_carmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmodel',
            options={},
        ),
        migrations.RemoveField(
            model_name='order',
            name='estimate_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
