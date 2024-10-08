# Generated by Django 5.1.1 on 2024-10-08 20:10
import csv
import os
from django.db import migrations

def load_csv_data(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_file_path = os.path.join(base_dir, 'Django Database.csv')
    print(f'Loading data from {csv_file_path}')

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not Task.objects.filter(id=row['id']).exists():
                Task.objects.create(**row)

def unload_csv_data(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_is_urgent'),
    ]

    operations = [
        migrations.RunPython(load_csv_data, reverse_code=unload_csv_data),
    ]
