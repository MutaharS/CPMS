# Generated by Django 3.0 on 2021-07-06 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0026_auto_20210704_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ReviewSubmission',
            field=models.CharField(default='2021-07-06T01:28', max_length=200),
        ),
        migrations.AlterField(
            model_name='reviewer',
            name='DateJoined',
            field=models.CharField(default='2021-07-06T01:28', max_length=200),
        ),
    ]
