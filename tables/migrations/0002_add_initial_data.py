from django.db import migrations, models

def add_initial_data(apps, schema_editor):
    SoybeanMeal = apps.get_model('tables', 'SoybeanMeal')
    
    # Dados iniciais
    initial_data = [
        {"contract_month": "NOV24", "price": 34.94},
        {"contract_month": "DEC24", "price": 34.06},
        {"contract_month": "JAN25", "price": 33.49},
        {"contract_month": "FEB25", "price": 33.35},
        {"contract_month": "MAR25", "price": 33.02},
    ]

    # Insere os dados no banco
    for data in initial_data:
        SoybeanMeal.objects.create(**data)

def remove_initial_data(apps, schema_editor):
    SoybeanMeal = apps.get_model('tables', 'SoybeanMeal')
    
    # Remove os dados iniciais
    SoybeanMeal.objects.filter(contract_month__in=["NOV24", "DEC24", "JAN25", "FEB25", "MAR25"]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]