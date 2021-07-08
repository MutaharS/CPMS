from django.db import models
from datetime import datetime
# Create your models here.
class Author(models.Model):
    AuthorID = models.AutoField(primary_key=True)
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
    Email = models.CharField(max_length=200,unique=True) # Recreate database and make this not nullable
    Password = models.CharField(max_length=100)
    DateJoined = models.CharField(max_length=200,default=datetime.now().isoformat(timespec='minutes'))

    # Override printing of an Author object as the first name and last name plus email
    def __str__(self):
        return self.FirstName + " " + self.LastName + ": " + self.Email

class Paper(models.Model):
    PaperID = models.AutoField(primary_key=True)
    AuthorID = models.ForeignKey(Author, on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    FilenameOriginal = models.CharField(max_length=100,default="")
    Filename = models.CharField(max_length=100,default="")
    NumberOfAssignedReviewers = models.IntegerField(default=0)
    Certification = models.CharField(max_length=3,default="")
    NotesToReviewers = models.TextField(blank=True,default="")
    Active = models.BooleanField(default=False)

    # Override printing of a Paper object as the first name and last name plus email
    def __str__(self):
        return self.AuthorID.LastName + ", " + self.AuthorID.LastName + ": " + self.Title