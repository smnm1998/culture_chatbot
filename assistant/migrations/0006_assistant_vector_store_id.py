# Generated by Django 4.2.16 on 2024-09-22 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0005_alter_assistant_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='vector_store_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
