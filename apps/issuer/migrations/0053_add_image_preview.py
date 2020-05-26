from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0052_auto_20200106_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='badgeclass',
            name='image_preview',
            field=models.FileField(blank=True, null=True, upload_to='uploads/badges'),
        ),
        migrations.AddField(
            model_name='issuer',
            name='image_preview',
            field=models.FileField(blank=True, null=True, upload_to='uploads/badges'),
        ),
    ]
