# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-23 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0024_auto_20160822_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='propertyauditlog',
            old_name='child',
            new_name='state',
        ),
        migrations.AlterField(
            model_name='propertyauditlog',
            name='parent1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='propertyauditlog__parent1', to='seed.PropertyAuditLog'),
        ),
        migrations.AlterField(
            model_name='propertyauditlog',
            name='parent2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='propertyauditlog__parent2', to='seed.PropertyAuditLog'),
        ),
        migrations.AlterField(
            model_name='taxlotauditlog',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taxlotauditlog__child', to='seed.TaxLotState'),
        ),
    ]