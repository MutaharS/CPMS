from django.shortcuts import render
from topic.models import Topic
from trydjango.settings import TOPICS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "home.html")

# View to initialize topics, for when we reset the database
def reset_topic_view(request, *args, **kwargs):
    for topic in TOPICS:
        print(topic)
        Topic.objects.create(TopicName=topic)
    return render(request, "home.html")