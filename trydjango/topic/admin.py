from django.contrib import admin
from .models import Topic, ReviewerTopic, PaperTopic
# Register your models here.
admin.site.register(Topic)
admin.site.register(ReviewerTopic)
admin.site.register(PaperTopic)