from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from trydjango.settings import TOPICS
from .models import Author, Paper
from topic.models import Topic, PaperTopic
from .forms import AuthorRegistrationForm, AuthorEditProfileForm, PaperSubmissionForm
import os, ntpath # For file saving
import uuid # unique identifier generation (handle case where two papers have the same name)

# Define author reviews
def author_signup_view(request):
    # Get the form
    form = AuthorRegistrationForm(request.POST or None)
    if form.is_valid():
        formData = form.cleaned_data  # Get dictionary of field -> value
        email = formData.get('Email') # Get email (acts as username for login)
        # First save the new author
        form.save()
        form = AuthorRegistrationForm() # Reset the form visually (not necessary if we link to login page)
        
        # Create the user object corresponding to this author
        # Set the username in User database as the author's email and set their respective password
        User = get_user_model()
        obj = User.objects.create(username=email)
        obj.is_author = True # Set this user as an author
        obj.set_password(formData.get('Password'))
        obj.save() # save object instance to db
        return redirect('/login')
    else:
        print('invalid form')
    # Check that the form is valid
    return render(request, "author_signup.html", { "form": form })

# TODO: Use form data to change the author instance
def author_profile(request):
    # Get the author object
    author = Author.objects.get(Email=request.user.username)

    # Get the current author information to pass to the form (so user can see what data they currently have)
    context = author.__dict__
    if not request.method == 'POST':
        # Before they submit the form, show the form with their user data
        form = AuthorEditProfileForm(initial=context)
    else:
        # Get the submitted form
        form = AuthorEditProfileForm(request.POST or None)
    
    # If the form has been validated, then make the appropriate changes to the author object
    if form.is_valid() and request.method == "POST":
        formData = form.cleaned_data  # Get dictionary of field -> value
        email = request.user.username
        
        # Modify the author and user object corresponding to this author
        author.Affiliation = formData.get('Affiliation')
        author.Department = formData.get('Department')
        author.CellNumber = formData.get('CellNumber')
        author.WorkNumber = formData.get('WorkNumber')
        author.Address = formData.get('Address')
        author.City = formData.get('City')
        author.State = formData.get('State')
        author.ZipCode = formData.get('ZipCode')

        # Set the username in User database as the author's email and set their respective password
        User = get_user_model()
        obj = User.objects.get(username=email)

        # Only update the password if the OldPassword, NewPassword and ConfirmNewPassword fields are all
        # not blank (form validation will take care of the rest)
        # if(len(formData.get('OldPassword)) != 0 and ...)
        # obj.set_password(formData.get('NewPassword'))

        # Save the changes
        author.save() # save author data to db
        obj.save() # save object instance to db
    else:
        # Remove else statement in production
        print(form.errors)
        print('invalid')
    return render(request, "profile.html", {"form" : form })

# Function to handle uploading the file
def handle_uploaded_file(file):
    filename = str(file).replace(' ', '_') # Replace whitespace with underscores otherwise problems happen
    # Upload the file with a unique identifier prepended to the filename
    fpath = os.path.join("uploads",uuid.uuid1().hex + filename) # Get the path for where the file will be written
    with open(fpath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return fpath # return the actual file name

# NOTE: File upload is now working, just need to save the Paper model
# TODO (COMPLETED): Save the paper object via form.save()
#       Fill in any details the paper needs
#       Create a PaperTopic entry relating the paper to its topics
#       Save the paper file into the project directory

#form = form.save(commit=False) # Save the review, but don't commit to the db yet
def submit_paper_view(request):
    if request.method == "POST":
        form = PaperSubmissionForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            formData = form.cleaned_data
            print(formData)
            # Note that FileUpload is the actual file object not a string
            form = form.save(commit=False) # Save the review, but don't commit to the db yet
            aID = Author.objects.get(Email=request.user.username)
            form.AuthorID = aID
            form.FilenameOriginal = str(request.FILES['FileUpload'])
            fname = handle_uploaded_file(request.FILES['FileUpload']) # Get the actual filepath while saving file
            form.Filename = fname # Set the file path
            form.NumberOfAssignedReviewers = 0 # initialize this to zero
            form.save()

            form = PaperSubmissionForm() # Reset the form visually and allow iterating over it
            
            # Get the paper object that was just created, Filename is unique to it
            paper = Paper.objects.get(Filename=fname)
            
            for field in form:
                if field.label in TOPICS:
                    # If the topic was marked True, then create an entry relating this paper
                    # to the corresponding topic in PaperTopic
                    if formData.get(field.name) == True:
                        topic = Topic.objects.get(TopicName=field.label) # Get the topic with this name
                        pt = PaperTopic(PaperID=paper,TopicID=topic) # Create the ReviewerTopic instance
                        pt.save() # save the instance to the database
    else:
        form = PaperSubmissionForm(None)
    return render(request, "paper_submission.html", {"form" : form})