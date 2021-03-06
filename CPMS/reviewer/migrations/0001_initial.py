# Generated by Django 3.0 on 2021-07-08 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('ReviewerID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=200)),
                ('MiddleInitial', models.CharField(blank=True, max_length=1, null=True)),
                ('LastName', models.CharField(max_length=200)),
                ('Affiliation', models.CharField(max_length=200)),
                ('Department', models.CharField(max_length=200)),
                ('CellNumber', models.CharField(max_length=200)),
                ('WorkNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('Address', models.CharField(max_length=200)),
                ('City', models.CharField(max_length=200)),
                ('State', models.CharField(max_length=200)),
                ('ZipCode', models.CharField(max_length=200)),
                ('Email', models.CharField(max_length=200, null=True, unique=True)),
                ('Password', models.CharField(max_length=100)),
                ('NumberOfReviews', models.IntegerField(default=0)),
                ('DateJoined', models.CharField(default='2021-07-08T17:19', max_length=200)),
                ('OtherDescription', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ReviewID', models.AutoField(primary_key=True, serialize=False)),
                ('PaperTitle', models.CharField(default='', max_length=200)),
                ('AppropriatenessOfTopic', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('TimelinessOfTopic', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('SupportiveEvidence', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('TechnicalQuality', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('ScopeOfCoverage', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('CitationOfPreviousWork', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('Originality', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('ContentComments', models.TextField(blank=True, max_length=200, null=True)),
                ('OrganizationOfPaper', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('ClarityOfMainMessage', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('Mechanics', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('WrittenComments', models.TextField(blank=True, max_length=200, null=True)),
                ('SuitabilityForPresentation', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('PotentialInterestInTopic', models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], default=3)),
                ('OralComments', models.TextField(blank=True, max_length=200, null=True)),
                ('OverallRating', models.IntegerField(choices=[(1, 'Definitely should not accept paper'), (2, 'Probably should not accept paper'), (3, 'Uncertain about acceptance of paper'), (4, 'Probably should accept paper'), (5, 'Definitely should accept paper')], default=3)),
                ('OverallComments', models.TextField(blank=True, max_length=200, null=True)),
                ('ReviewSubmission', models.CharField(default='2021-07-08T17:19', max_length=200)),
                ('Complete', models.BooleanField(default=False)),
                ('PaperID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.Paper')),
                ('ReviewerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Reviewer')),
            ],
        ),
    ]
