# Generated by Django 4.1.3 on 2022-11-14 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0003_alter_carmodel_options_order_estimate_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['make', 'model', 'year', 'engine'], 'verbose_name': 'model', 'verbose_name_plural': 'models'},
        ),
    ]
