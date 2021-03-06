# Generated by Django 2.1 on 2018-08-24 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('old_data', models.TextField(blank=True)),
                ('new_data', models.TextField(blank=True)),
                ('object_id', models.IntegerField()),
            ],
        ),
    ]
