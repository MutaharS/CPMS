from django.db import models
from reviewer.models import Reviewer
# Create your models here.
class Topic(models.Model):
    TopicID = models.AutoField(primary_key=True)
    TopicName = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.TopicName

class ReviewerTopic(models.Model):
    ReviewerTopicID = models.AutoField(primary_key=True)
    ReviewerID = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    TopicID = models.ForeignKey(Topic, on_delete=models.CASCADE)