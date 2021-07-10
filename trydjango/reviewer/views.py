from django.contrib.auth import get_user_model
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404
from django import forms
from .models import Reviewer, Review
from .forms import ReviewerRegistrationForm, ChooseReviewForm, PaperReviewForm
from topic.models import Topic, ReviewerTopic
from trydjango.settings import TOPICS
import os

# Create your views here.

# TODO: Enforce authorization for sensitive pages


# TODO: (COMPLETED)
# Will have to change this view since a Review instance should be created when 
# assigning a reviewer to a paper and then modifying it in this view rather than creating it
# Steps: 
#   1) Get the PaperID from the entered title
#   2) Get the ReviewerID from request.user
#   3) Get the Review instance with those parameters
#   4) Modify the review instance

# TODO:

def download_paper(request, paperpath):
    REMOVE_FOLDER_CHARS = 8 + 32 # 8 chars in 'uploads/', 32 chars in UUID
    response = HttpResponse(open(os.getcwd() + '/' + paperpath, 'rb').read())
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=%s' % paperpath[REMOVE_FOLDER_CHARS:]
    return response

def assigned_papers_view(request):
    if request.method == "GET" and request.GET.get('data') != None:
        paperpath = request.GET.get('data')
        return download_paper(request,paperpath)

    # Store data as list of tuples (Title, Filename)
    assigned_papers = []

    # Get queryset with the reviews assigned to this reviewer
    queryset = Review.objects.all().filter(ReviewerID=Reviewer.objects.get(Email=request.user.username))
    for review in queryset:
        papertuple = [review.PaperID.Title, review.PaperID.NotesToReviewers, review.PaperID.Filename]
        assigned_papers.append(papertuple)
    
    return render(request, "assigned_papers.html", { "assigned_papers" : assigned_papers })

def choose_review_view(request):
    form = ChooseReviewForm(request.POST or None, user=request.user)
    # Check that the form is valid
    print(form.errors)

    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            print('Valid Form')

            # Get the form data
            formData = form.cleaned_data

            # Get the selected review
            selected_review = formData.get('PaperChoices')

            # Store the ReviewID into the session data for use in the actual review form
            request.session['selected_review'] = selected_review.ReviewID

            # Go to the actual review page
            return redirect(review_form_view)
        else:
            print('Form is not valid')
    return render(request, "choose_review_form.html", {"form": form})

def review_form_view(request):
    # Get the selected review using the stored ReviewID
    review = Review.objects.get(ReviewID=request.session['selected_review'])
        
    # Get the current review information to pass to the form
    context = review.__dict__
    
    # Before they submit the form, show the form with the current review data
    if not request.method == 'POST':
        form = PaperReviewForm(initial=context)
    # Otherwise, get the submitted form
    else:
        form = PaperReviewForm(request.POST or None)
    
    # If the form has been validated, then save the changes to the review object
    if form.is_valid() and request.method == "POST":

        # For each of the form entries (attributes)
        for attr in form.cleaned_data.keys():
            # Set the corresponding review object attribute to the form's
            review.__dict__[attr] = form.cleaned_data[attr]
        
        # Mark the review as completed
        review.__dict__['Complete'] = True

        # Save the review object
        review.save()
        message = "Your review was submitted successfully, thank you."
        # Redirect user with success message
        return render(request, "home.html", { "message" : message })

    return render(request, "review_form_backup.html", {"form": form} )
    
# def review_form_view(request):
#     form = PaperReviewForm(request.POST or None)
#     # Check that the form is valid
#     print(form.errors)
#     if form.is_valid():
#         print('Valid Form')
#         rID = Reviewer.objects.get(Email=request.user.username)
#         form = form.save(commit=False) # Save the review, but don't commit to the db yet
#         print(rID)
#         # TODO: Add PaperID

#         form.ReviewerID = rID # Set the ReviewerID
#         form.save() # Now we can save it
#         form = PaperReviewForm()    # Reset the form visually
#     else:
#         print('Form is not valid')
#     return render(request, "review_form.html", {"form": form})

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