# Generated by Django 5.1.7 on 2025-03-06 23:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investmentpackage',
            options={'ordering': ['min_amount'], 'verbose_name': 'Investment Package', 'verbose_name_plural': 'Investment Packages'},
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='description',
            field=models.TextField(blank=True, help_text='Brief details about this investment package.'),
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='duration_weeks',
            field=models.PositiveIntegerField(default=4, help_text='Minimum duration for this investment (in weeks).'),
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='monthly_profit_percent',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Expected monthly return as a percentage.', max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='risk_level',
            field=models.CharField(choices=[('Low', 'Low Risk'), ('Medium', 'Medium Risk'), ('High', 'High Risk')], default='Medium', max_length=10),
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10),
        ),
        migrations.AddField(
            model_name='investmentpackage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='investmentpackage',
            name='min_amount',
            field=models.DecimalField(decimal_places=2, help_text='Minimum amount required to invest.', max_digits=10),
        ),
        migrations.AlterField(
            model_name='investmentpackage',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='investmentpackage',
            name='weekly_profit_percent',
            field=models.DecimalField(decimal_places=2, help_text='Expected weekly return as a percentage.', max_digits=5),
        ),
    ]
