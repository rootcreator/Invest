# Generated by Django 5.1.7 on 2025-03-06 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_investmentpackage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='transaction_id',
            field=models.CharField(default=0, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deposit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='deposit',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
