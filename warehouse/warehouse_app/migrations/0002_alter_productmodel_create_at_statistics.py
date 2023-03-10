# Generated by Django 4.1.5 on 2023-01-29 09:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='create_at',
            field=models.CharField(default=datetime.date(2023, 1, 29), max_length=30, verbose_name='дата добавления'),
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse_app.productmodel', verbose_name='продукт')),
            ],
        ),
    ]
