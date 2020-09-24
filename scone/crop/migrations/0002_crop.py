# Generated by Django 3.1.1 on 2020-09-24 01:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='crop/crop/image')),
                ('original_picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='crop.picture')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
