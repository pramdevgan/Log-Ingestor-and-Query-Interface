# Generated by Django 4.2.7 on 2023-11-18 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(db_index=True, max_length=255)),
                ('message', models.TextField()),
                ('resource_id', models.CharField(db_index=True, max_length=255)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('trace_id', models.CharField(db_index=True, max_length=255)),
                ('span_id', models.CharField(db_index=True, max_length=255)),
                ('commit', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Log Entry',
                'verbose_name_plural': 'Log Entries',
            },
        ),
        migrations.CreateModel(
            name='LogEntryMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_resource_id', models.CharField(max_length=255)),
                ('log_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log_ingestor_app.logentry')),
            ],
            options={
                'verbose_name': 'Log Entry Metadata',
                'verbose_name_plural': 'Log Entry Metadata',
            },
        ),
    ]
