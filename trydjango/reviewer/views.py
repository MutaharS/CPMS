from django.contrib.auth import get_user_model
from django.shortcuts import render
from django import forms
from .models import Reviewer
from .forms import ReviewerRegistrationForm, PaperReviewForm
from topic.models import ReviewerTopic
from topic.models import Topic
from trydjango.settings import TOPICS

# Create your views here.

# TODO: Enforce authorization for sensitive pages


# TODO:
# Will have to change this view since a Review instance should be created when 
# assigning a reviewer to a paper and then modifying it in this view rather than creating it
# Steps: 
#   1) Get the PaperID from the entered title
#   2) Get the ReviewerID from request.user
#   3) Get the Review instance with those parameters
#   4) Modify the review instance

def review_form_view(request):
    form = PaperReviewForm(request.POST or None)
    # Check that the form is valid
    print(form.errors)
    if form.is_valid():
        print('Valid Form')
        rID = Reviewer.objects.get(Email=request.user.username)
        form = form.save(commit=False) # Save the review, but don't commit to the db yet
        print(rID)
        # TODO: Add PaperID

        form.ReviewerID = rID # Set the ReviewerID
        form.save() # Now we can save it
        form = PaperReviewForm()    # Reset the form visually
    else:
        print('Form is not valid')
    return render(request, "review_form.html", {"form": form})

# View for when a reviewer wants to create an account (from navbar)
def reviewer_signup_view(request):
    # Render the form
    form = ReviewerRegistrationForm(request.POST or None)

    # Check that the form is valid
    if form.is_valid():
        formData = form.cleaned_data
        # First save the new reviewer
        form.save()
        form = ReviewerRegistrationForm() # Reset the form visually (not necessary if we link to login page)

        # Get the reviewer's email from the form data (it is unique data)
        email = formData.get('Email')

        # Get the reviewer object that was just created
        reviewer = Reviewer.objects.get(Email=email)

        # For each of the form entries, see if it corresponds to a topic
        # field is the following object:
        #   <input type="checkbox" name="UsingTechnology" id="id_UsingTechnology">
        
        for field in form:
            if field.label in TOPICS:
                # If the topic was marked True, then create an entry relating this reviewer
                # to the corresponding topic in ReviewerTopic
                #print(field.label + ": " + str(formData.get(field.name)) )
                if formData.get(field.name) == True:
                    print(field.label)
                    topic = Topic.objects.get(TopicName=field.label) # Get the topic with this name
                    rt = ReviewerTopic(ReviewerID=reviewer,TopicID=topic) # Create the ReviewerTopic instance
                    rt.save() # save the instance to the database
        
        # If Other was filled out, let's save it as part of the reviewer object 
        # (admin can then decide whether to add that topic to the database or not)
        print(formData)
        if len(formData.get('Other')) > 0:
            reviewer.OtherDescription = formData.get('Other') # Update the other field of the reviewer
            reviewer.save() # Save the change to the database
        
        # Finally, create the user object corresponding to this reviewer
        # Set the username in User database as the reviewer's email and set their respective password
        User = get_user_model()
        obj = User.objects.create(username=email)
        obj.is_reviewer = True # Set this user as a reviewer
        obj.set_password(formData.get('Password'))
        obj.save() # save object instance to db

    print('form is not valid')
    context = {
        'form': form
    } # When we use navbar to get here, there is no context
    return render(request,"sign_up.html",context)