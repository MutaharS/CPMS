from django.db import models
from datetime import datetime
from accounts.models import User
# Create your models here.
class Reviewer(models.Model):
    ReviewerID = models.AutoField(primary_key=True)
    #ReviewerUser = models.OneToOneField(User, on_delete=models.CASCADE) # maybe add user to table after?
    FirstName = models.CharField(max_length=200)
    MiddleInitial = models.CharField(max_length=1,blank=True, null=True)
    LastName = models.CharField(max_length=200)
    Affiliation = models.CharField(max_length=200)
    Department = models.CharField(max_length=200)
    CellNumber = models.CharField(max_length=200)
    WorkNumber = models.CharField(max_length=200, blank=True, null=True)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=200)
    State = models.CharField(max_length=200)
    ZipCode = models.CharField(max_length=200)
    Email = models.CharField(max_length=200,unique=True,null=True) # Recreate database and make this not nullable
    Password = models.CharField(max_length=100)
    NumberOfReviews = models.IntegerField(default=0)
    DateJoined = models.CharField(max_length=200,default=datetime.now().isoformat(timespec='minutes'))
    OtherDescription = models.TextField(max_length=200, blank=True, null=True)

    # Override printing of a Reviewer object as the first name and last name
    def __str__(self):
        return self.FirstName + " " + self.LastName

class Review(models.Model):
    GRADE_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    OVERALL_CHOICES = [
        (1, 'Definitely should not accept paper'),
        (2, 'Probably should not accept paper'),
        (3, 'Uncertain about acceptance of paper'),
        (4, 'Probably should accept paper'),
        (5, 'Definitely should accept paper'),
    ]
    ReviewID = models.AutoField(primary_key=True)
    ReviewerID = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    #PaperID = models.ForeignKey(Paper, on_delete=models.CASCADE)
    # Content fields
    PaperTitle = models.CharField(max_length=200,blank=False,null=False,default="")
    AppropriatenessOfTopic = models.IntegerField(choices=GRADE_CHOICES,default=3)
    TimelinessOfTopic = models.IntegerField(choices=GRADE_CHOICES,default=3)
    SupportiveEvidence = models.IntegerField(choices=GRADE_CHOICES,default=3)
    TechnicalQuality = models.IntegerField(choices=GRADE_CHOICES,default=3)
    ScopeOfCoverage = models.IntegerField(choices=GRADE_CHOICES,default=3)
    CitationOfPreviousWork = models.IntegerField(choices=GRADE_CHOICES,default=3)
    Originality = models.IntegerField(choices=GRADE_CHOICES,default=3)
    ContentComments = models.TextField(max_length=200,blank=True,null=True)

    # Written Document fields
    OrganizationOfPaper = models.IntegerField(choices=GRADE_CHOICES,default=3)
    ClarityOfMainMessage = models.IntegerField(choices=GRADE_CHOICES,default=3)
    Mechanics = models.IntegerField(choices=GRADE_CHOICES,default=3)
    WrittenComments = models.TextField(max_length=200,blank=True,null=True)

    # Potential for Oral Presentation fields
    SuitabilityForPresentation = models.IntegerField(choices=GRADE_CHOICES,default=3)
    PotentialInterestInTopic = models.IntegerField(choices=GRADE_CHOICES,default=3)
    OralComments = models.TextField(max_length=200,blank=True,null=True)

    # Overall rating field
    OverallRating = models.IntegerField(choices=OVERALL_CHOICES,default=3)
    OverallComments = models.TextField(max_length=200,blank=True,null=True)
    ReviewSubmission = models.CharField(max_length=200,default=datetime.now().isoformat(timespec='minutes'))