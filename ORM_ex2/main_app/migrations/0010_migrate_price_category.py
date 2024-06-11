# Generated by Django 4.2.4 on 2023-10-23 18:29

from django.db import migrations


def set_price(apps, schema_editor):
    MULTIPLY_PRICE = 120

    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        smartphone.price = len(smartphone.brand) * MULTIPLY_PRICE
        smartphone.save()


def set_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        if smartphone.price >= 750:
            smartphone.category = "Expensive"
        else:
            smartphone.category = "Cheap"
        smartphone.save()


def set_category_and_price(apps, schema_editor):
    set_price(apps, schema_editor)
    set_category(apps, schema_editor)


def reverse_code(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'Smartphone')

    for smartphone in smartphone_model.objects.all():
        smartphone.price = 0
        smartphone.category = "empty"
        smartphone.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_smartphone'),
    ]

    operations = [
        migrations.RunPython(set_category_and_price, reverse_code=reverse_code)
    ]
