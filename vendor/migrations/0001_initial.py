# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-28 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('_name', models.CharField(max_length=100)),
                ('_type', models.CharField(max_length=50)),
                ('_size', models.SmallIntegerField()),
            ],
            options={
                'db_table': '__attributes',
            },
        ),
        migrations.CreateModel(
            name='DictionaryItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('form_group', models.CharField(db_index=True, max_length=100)),
                ('parent_node', models.CharField(db_index=True, max_length=100, null=True)),
                ('t_key', models.CharField(db_index=True, max_length=100)),
                ('t_locale', models.CharField(max_length=50)),
                ('t_type', models.CharField(db_index=True, max_length=30)),
                ('t_value', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'dictionary_items',
            },
        ),
        migrations.CreateModel(
            name='FormMappings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('form_group', models.CharField(db_index=True, max_length=50)),
                ('form_question', models.CharField(max_length=100)),
                ('dest_table_name', models.CharField(db_index=True, max_length=100)),
                ('dest_column_name', models.CharField(db_index=True, max_length=50)),
                ('odk_question_type', models.CharField(max_length=50)),
                ('db_question_type', models.CharField(max_length=50)),
                ('ref_table_name', models.CharField(max_length=100, null=True)),
                ('ref_column_name', models.CharField(max_length=50, null=True)),
                ('validation_regex', models.CharField(max_length=100, null=True)),
                ('is_record_identifier', models.BooleanField(default=False)),
                ('is_null', models.SmallIntegerField(null=True)),
                ('is_lookup_field', models.NullBooleanField(default=False)),
                ('use_current_time', models.NullBooleanField(default=False)),
            ],
            options={
                'db_table': 'mappings_table',
            },
        ),
        migrations.CreateModel(
            name='FormViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('view_name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('proper_view_name', models.CharField(db_index=True, max_length=100)),
                ('structure', jsonfield.fields.JSONField()),
            ],
            options={
                'db_table': 'form_views',
            },
        ),
        migrations.CreateModel(
            name='ImagesLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(db_index=True, max_length=50, unique=True)),
                ('species', models.CharField(max_length=50, null=True)),
                ('breed', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=80, null=True)),
            ],
            options={
                'db_table': 'images_lookup',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('model_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': '__models',
            },
        ),
        migrations.CreateModel(
            name='ODKForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('form_id', models.IntegerField(db_index=True, unique=True)),
                ('form_name', models.CharField(max_length=200, unique=True)),
                ('full_form_id', models.CharField(max_length=200, unique=True)),
                ('structure', jsonfield.fields.JSONField(null=True)),
                ('processed_structure', jsonfield.fields.JSONField(null=True)),
                ('auto_update', models.BooleanField(default=False)),
                ('is_source_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'odkform',
            },
        ),
        migrations.CreateModel(
            name='ODKFormGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order_index', models.SmallIntegerField(null=True)),
                ('group_name', models.CharField(max_length=100, unique=True)),
                ('comments', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'db_table': 'form_groups',
            },
        ),
        migrations.CreateModel(
            name='ProcessingErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('err_code', models.IntegerField(db_index=True)),
                ('err_message', models.TextField()),
                ('data_uuid', models.CharField(db_index=True, max_length=100)),
                ('err_comments', models.CharField(max_length=1000, null=True)),
                ('is_resolved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'processing_errors',
            },
        ),
        migrations.CreateModel(
            name='RawSubmissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(db_index=True, max_length=100, unique=True)),
                ('submission_time', models.CharField(max_length=100)),
                ('is_processed', models.BooleanField(default=0)),
                ('is_modified', models.BooleanField(default=0)),
                ('raw_data', jsonfield.fields.JSONField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.ODKForm')),
            ],
            options={
                'db_table': 'raw_submissions',
            },
        ),
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('setting_name', models.CharField(max_length=200)),
                ('setting_key', models.CharField(max_length=100, unique=True)),
                ('setting_value', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'system_settings',
            },
        ),
        migrations.CreateModel(
            name='ViewsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('raw_data', jsonfield.fields.JSONField()),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.FormViews')),
            ],
            options={
                'db_table': 'views_data',
            },
        ),
        migrations.CreateModel(
            name='ViewTablesLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('table_name', models.CharField(db_index=True, max_length=250, unique=True)),
                ('proper_table_name', models.CharField(db_index=True, max_length=250, null=True)),
                ('hashed_name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.FormViews')),
            ],
            options={
                'db_table': 'views_table_lookup',
            },
        ),
        migrations.AddField(
            model_name='odkform',
            name='form_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.ODKFormGroup'),
        ),
        migrations.AddField(
            model_name='formviews',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.ODKForm'),
        ),
        migrations.AlterUniqueTogether(
            name='formmappings',
            unique_together=set([('form_group', 'form_question', 'dest_table_name', 'dest_column_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='dictionaryitems',
            unique_together=set([('form_group', 'parent_node', 't_key')]),
        ),
        migrations.AddField(
            model_name='attribute',
            name='_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Model'),
        ),
    ]
