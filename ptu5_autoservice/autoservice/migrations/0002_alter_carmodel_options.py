# Generated by Django 4.1.3 on 2022-11-14 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['make', 'model', 'year', 'engine'], 'verbose_name': 'model', 'verbose_name_plural': 'models'},
        ),
    ]
