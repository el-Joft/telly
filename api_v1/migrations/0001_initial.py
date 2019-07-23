# Generated by Django 2.2.3 on 2019-07-22 21:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role_type', models.CharField(choices=[('superadmin', 'Super Admin'), ('admin', 'Admin'), ('user', 'User'), ('business', 'Business')], db_index=True, max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('mobile_number', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(blank=True, max_length=128)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('points', models.IntegerField(default=0)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.Role')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('pk',),
            },
        ),
    ]
