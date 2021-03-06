# Generated by Django 3.0.3 on 2020-02-23 06:41

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', versatileimagefield.fields.VersatileImageField(blank=True, upload_to='avatars')),
                ('item_per_page', models.IntegerField(default=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.SmallIntegerField()),
                ('title', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField()),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['pid'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'ordering': ['tag_name'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('code', models.TextField()),
            ],
            options={
                'ordering': ['test_id'],
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=128)),
                ('description', models.TextField(default='')),
                ('users', models.ManyToManyField(blank=True, related_name='usergroups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['gid'],
            },
        ),
        migrations.CreateModel(
            name='TestSet',
            fields=[
                ('testset_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_score', models.FloatField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='oj.Problem')),
                ('tests', models.ManyToManyField(blank=True, related_name='_testset_tests_+', to='oj.Test')),
            ],
            options={
                'ordering': ['testset_id'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=64)),
                ('description', models.TextField(default='')),
                ('deadline', models.DateTimeField()),
                ('problems', models.ManyToManyField(blank=True, related_name='tasks', to='oj.Problem')),
                ('usergroups', models.ManyToManyField(blank=True, related_name='tasks', to='oj.UserGroup')),
            ],
            options={
                'ordering': ['task_id'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.TextField(default='')),
                ('score', models.FloatField(null=True)),
                ('full_score', models.FloatField(null=True)),
                ('code', models.TextField()),
                ('is_solution', models.BooleanField(default=False)),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='oj.Problem')),
                ('tasks', models.ManyToManyField(blank=True, related_name='submissions', to='oj.Task')),
                ('testset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='oj.TestSet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sid'],
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='problems', to='oj.Tag'),
        ),
        migrations.AddField(
            model_name='problem',
            name='testset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='oj.TestSet'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-aid'],
            },
        ),
    ]
