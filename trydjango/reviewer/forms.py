from django import forms
from .models import Reviewer, Review
from author.models import Author, Paper
from trydjango.settings import TOPICS
'''
    The form is valid if:
        - All required fields are filled
        - The email has not already been used (clean_Email)
        - The email is valid (clean_Email)
        - Valid CellNumber is given (clean_CellNumber)
        - Valid WorkNumber is given (clean_WorkNumber) if provided
        - At least one topic is selected or Other has been described
'''

# Allows the Reviewer to select which paper they would like to review
class ChooseReviewForm(forms.Form):
    class Meta:
        fields = []
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        print(self.user)
        super(ChooseReviewForm, self).__init__(*args, **kwargs)
        self.fields["PaperChoices"] = forms.ModelChoiceField(
            # Get queryset with the reviews assigned to this reviewer
            queryset=Review.objects.all().filter(ReviewerID=Reviewer.objects.get(Email=self.user.username)),
            label="Assigned Papers"
        )

# Paper review form based on the review model
class PaperReviewForm(forms.ModelForm):
    #PaperTitle = forms.CharField(max_length=200, label='Paper Title', required=True)
    class Meta:
        model = Review
        labels = {
            'AppropriatenessOfTopic': 'Appropriateness of Topic',
            'TimelinessOfTopic': 'Timeliness of Topic',
            'SupportiveEvidence': 'Supportive Evidence',
            'TechnicalQuality': 'Technical Quality',
            'ScopeOfCoverage': 'Scope of Coverage',
            'CitationOfPreviousWork': 'Citation of Previous Work',
            'OrganizationOfPaper': 'Organization of Paper',
            'ClarityOfMainMessage': 'Clarity of Main Message',
            'SuitabilityForPresentation': 'Suitability for Presentation',
            'PotentialInterestInTopic': 'Potential Interest in Topic',
            'OverallRating': 'Overall Rating',
            'ContentComments': 'Comments',
            'WrittenComments': 'Comments',
            'OralComments': 'Comments'
        }
        fields = [
            'AppropriatenessOfTopic',
            'TimelinessOfTopic',
            'SupportiveEvidence',
            'TechnicalQuality',
            'ScopeOfCoverage',
            'CitationOfPreviousWork',
            'Originality',
            'ContentComments',

            'OrganizationOfPaper',
            'ClarityOfMainMessage',
            'Mechanics',
            'WrittenComments',

            'SuitabilityForPresentation',
            'PotentialInterestInTopic',
            'OralComments',

            'OverallRating',
            'OverallComments'
        ]

class ReviewerRegistrationForm(forms.ModelForm):
    Analysis = forms.BooleanField(label="Analysis of Algorithms", required=False)
    Applications = forms.BooleanField(label="Applications", required=False)
    Architecture = forms.BooleanField(label="Architecture", required=False)
    ArtificialIntelligence = forms.BooleanField(label="Artificial Intelligence", required=False)
    ComputerEngineering = forms.BooleanField(label="Computer Engineering", required=False)
    Curriculum = forms.BooleanField(label="Curriculum", required=False)
    DataStructures = forms.BooleanField(label="Data Structures", required=False)
    Databases = forms.BooleanField(label="Databases", required=False)
    DistanceLearning = forms.BooleanField(label="Distance Learning", required=False)
    DistributedSystems = forms.BooleanField(label="Distributed Systems", required=False)
    EthicalIssues = forms.BooleanField(label="Ethical/Societal Issues", required=False)
    FirstYear = forms.BooleanField(label="First Year Computing", required=False)
    GenderIssues = forms.BooleanField(label="Gender Issues", required=False)
    GrantWriting = forms.BooleanField(label="Grant Writing", required=False)
    GraphicsImage = forms.BooleanField(label="Graphics Image Processing", required=False)
    HumanComputer = forms.BooleanField(label="Human Computer Interaction", required=False)
    LaboratoryEnvironments = forms.BooleanField(label="Laboratory Environments", required=False)
    Literacy = forms.BooleanField(label="Literacy", required=False)
    Mathematics = forms.BooleanField(label="Mathematics in Computing", required=False)
    Multimedia = forms.BooleanField(label="Multimedia", required=False)
    Networking = forms.BooleanField(label="Networking/Data Communications", required=False)
    NonMajor = forms.BooleanField(label="Non-Major Courses", required=False)
    ObjectOriented = forms.BooleanField(label="Object Oriented Issues", required=False)
    OperatingSystems = forms.BooleanField(label="Operating Systems", required=False)
    ParallelProcessing = forms.BooleanField(label="Parallel Processing", required=False)
    Pedagogy = forms.BooleanField(label="Pedagogy", required=False)
    ProgrammingLanguages = forms.BooleanField(label="Programming Languages", required=False)
    Research = forms.BooleanField(label="Research", required=False)
    Security = forms.BooleanField(label="Security", required=False)
    SoftwareEngineering = forms.BooleanField(label="Software Engineering", required=False)
    SystemsAnalysis = forms.BooleanField(label="Systems Analysis and Design", required=False)
    UsingTechnology = forms.BooleanField(label="Using Technology in the Classroom", required=False)
    WebInternet = forms.BooleanField(label="Web and Internet Programming", required=False)
    Other = forms.CharField(max_length=200,label="Other (Describe)",required=False, widget=forms.Textarea(
        attrs={
            "rows": 5
            }
        )
    )
    
    Password = forms.CharField(widget=forms.PasswordInput)
    Email = forms.EmailField()
    class Meta:
        model = Reviewer
        fields = [
                'FirstName',
                'MiddleInitial',
                'LastName',
                'Affiliation',
                'Department',
                'CellNumber',
                'WorkNumber',
                'Address',
                'City',
                'State',
                'ZipCode',
                'Email',
                'Password',
        ]

    def clean_Email(self, *args, **kwargs):
        email = self.cleaned_data.get('Email')
        if not email.endswith('com') and not email.endswith('org') and not email.endswith('edu'):
            raise forms.ValidationError("This is not a valid email domain.")
        if not '@' in email:
            raise forms.ValidationError("This is not a valid email. Please include @.")
        if Reviewer.objects.filter(Email=email).exists():
            raise forms.ValidationError("Sorry, this email has been taken.")
        if Author.objects.filter(Email=email).exists():
            raise forms.ValidationError("Sorry, this email has been taken.")
        return email

    # TODO: clean up the cellphone to remove '-' from it
    def clean_CellNumber(self, *args, **kwargs):
        cellnumber = self.cleaned_data.get('CellNumber')
        return cellnumber

    # Check for a topic
    def clean_Other(self, *args, **kwargs):
        other = self.cleaned_data.get('Other') # Get the cleaned 'other' data to return
        flag = False
        formData = self.cleaned_data
        # First check that no topic was selected
        for field in self:
            if field.label in TOPICS:
                if formData.get(field.name) == True:
                    flag = True
                    break
        # If we found a selected topic, return other with no issues
        if(flag):
            return other

        # Otherwise, no topic was selected so must validate that Other (Describe) field was filled
        if(len(other) == 0):
            raise forms.ValidationError("Please select at least one topic, or describe one in Other (Describe)")
        return other

class ReviewerEditProfileForm(forms.ModelForm):
    OldPassword = forms.CharField(widget=forms.PasswordInput, label='Old Password', required=False)
    NewPassword = forms.CharField(widget=forms.PasswordInput, label='New Password', required=False)
    ConfirmNewPassword = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password', required=False)
    class Meta:
        model = Reviewer
        fields = [
                'Affiliation',
                'Department',
                'CellNumber',
                'WorkNumber',
                'Address',
                'City',
                'State',
                'ZipCode'
        ]
    
    # TODO: clean up the cellphone to remove '-' from it
    def clean_CellNumber(self, *args, **kwargs):
        cellnumber = self.cleaned_data.get('CellNumber')
        return cellnumber