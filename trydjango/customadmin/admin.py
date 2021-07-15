from reviewer.forms import ChooseReviewForm
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse
from reviewer.models import Review, Reviewer
from author.models import Paper, Author

# For CSV building/download
from django.http.response import HttpResponse
import csv

SPECIFIC_AVG_WEIGHT = 0.5
OVERALL_RATING_WEIGHT = 0.5
SCORE_FIELDS = [
        'AppropriatenessOfTopic',
        'TimelinessOfTopic',
        'SupportiveEvidence',
        'TechnicalQuality',
        'ScopeOfCoverage',
        'CitationOfPreviousWork',
        'Originality',

        # Written Document fields
        'OrganizationOfPaper',
        'ClarityOfMainMessage',
        'Mechanics',

        # Potential for Oral Presentation fields
        'SuitabilityForPresentation',
        'PotentialInterestInTopic',

        # Overall rating field
        'OverallRating']

def get_empty_review():
    reviewSummary = {
        'AppropriatenessOfTopic' : 0,
        'TimelinessOfTopic' : 0,
        'SupportiveEvidence' : 0,
        'TechnicalQuality' : 0,
        'ScopeOfCoverage' : 0,
        'CitationOfPreviousWork' : 0,
        'Originality' : 0,

        # Written Document fields
        'OrganizationOfPaper' : 0,
        'ClarityOfMainMessage' : 0,
        'Mechanics' : 0,

        # Potential for Oral Presentation fields
        'SuitabilityForPresentation' : 0,
        'PotentialInterestInTopic' : 0,

        # Overall rating field
        'OverallRating' : 0
    }
    return reviewSummary

# Review summary report
@admin.site.register_view('reviews_summary_report', urlname='reviews_summary_report', name='Reviews Summary Report')
def reviews_summary_report_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=review_summary_report.csv'
    writer = csv.writer(response)

    # Setup context for passing reviewSummaries to template
    context = {}
    reviewSummaries = []
    allPapers  = Paper.objects.all()

    # Store the CSV Header row
    csvcontents = []    # csvcontents will store each row of the csv
    currentrow = []     # The current row we are processing
    # First column is title
    currentrow.append('Title')
    for header in SCORE_FIELDS:
        currentrow.append(header)   # append header columns to the row
    csvcontents.append(currentrow)  # append the row containing header columns to csvcontents
    currentrow.append('Filename')
    currentrow.append('Weighted Score')
    
    # For each paper, get the average of its reviews and create a reviewSummary containing the required data
    # Add that review summary to reviewSummaries
    # NOTE: 1) Check that the reviews reported are complete
    #       2) Only display review summary for a paper that has 3 completed reviews?
    #       3) CSV file contents are created in parallel to avoid duplicated work
    for paper in allPapers:
        # For CSV creation reset the current row
        currentrow = []

        # Get the reviews for this paper
        reviews = Review.objects.filter(PaperID=paper,Complete=True)

        # Only process the review summary for papers who whave 3 completed reviews
        if len(reviews) == 3:
            # Set first column of csv content (Title)
            currentrow.append(paper.Title)

            # Get an empty review that will contain average after processing
            reviewSummary = get_empty_review()

            # For each of the reviews iterate through it's dict object 
            # and store the averaged values in reviewSummary
            numReviewsIterated = 0
            for review in reviews:
                for category in review.__dict__.keys():
                    if category in SCORE_FIELDS:
                        reviewSummary[category] = reviewSummary[category] + review.__dict__.get(category)
                numReviewsIterated = numReviewsIterated + 1
            
            specificTopicsSum = 0
            specificTopicCount = 0 # Should be 12 after iterating over topics (categories)
            # Average the values and keep running sum of specific scores (used for weightedScore)
            for category in reviewSummary.keys():
                reviewSummary[category] = round(reviewSummary[category] / numReviewsIterated, 2)

                # Add average of this particular category to currentrow
                currentrow.append(str(reviewSummary[category]))

                # Track running sum
                if category != 'OverallRating':
                    specificTopicsSum = specificTopicsSum + reviewSummary[category]
                    specificTopicCount = specificTopicCount + 1
            
            # Get the weighted score
            specificTopicAvg = specificTopicsSum / specificTopicCount
            weightedScore = (specificTopicAvg * SPECIFIC_AVG_WEIGHT) + (reviewSummary['OverallRating'] * OVERALL_RATING_WEIGHT)
            weightedScore = round(weightedScore, 2) # Round to 2 decimal places

            # Save the Title for the paper, it's file name, and weightedScore
            reviewSummary['Title'] = paper.Title
            reviewSummary['Filename'] = paper.FilenameOriginal
            reviewSummary['WeightedScore'] = weightedScore

            # Add the Filename, weightedScore, newline to currentrow
            currentrow.append(paper.FilenameOriginal)
            currentrow.append(str(weightedScore))
            csvcontents.append(currentrow) # Store the row pertaining to the current paper's summary into csv

            # Now add this reviewSummary to the list of all reviewSummaries
            reviewSummaries.append(reviewSummary)
    context['reviewSummaries'] = reviewSummaries
    
    # If the user clicked Download CSV Link, then return HttpResponse
    if request.method == "GET" and request.GET.get('data') != None:
        writer.writerows(csvcontents)
        return response

    return render(request, "reviews_summary_report.html", context)

# Reviewer Comments Report
@admin.site.register_view('reviewer_comments_report', urlname='reviewer_comments_report', name='Reviewer Comments Report')
def reviews_summary_report_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    csvcontents = []
    # The actual header to write to csv
    header = ['LastName', 'FirstName', 'MiddleInitial', 
        'Email', 'Filename', 'Title', 'ContentComments', 'WrittenDocumentComments', 
        'Potential For Oral Presentation Comments',  'Overall Rating Comments'
    ]
    # The one to reference when iterating through review object
    keyheader = ['LastName', 'FirstName', 'MiddleInitial', 
        'Email', 'Filename', 'Title', 'ContentComments', 'WrittenComments', 
        'OralComments',  'OverallComments'
    ]

    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=reviewer_comments_report.csv'
    writer = csv.writer(response)

    # Store header
    csvcontents.append(header)

    # For each paper, get its reviews
    allPapers = Paper.objects.all()
    for paper in allPapers:
        # For CSV creation reset the current row
        currentrow = []

        # Get the reviews for this paper
        reviews = Review.objects.filter(PaperID=paper,Complete=True)
        for review in reviews:
            for key in review.ReviewerID.__dict__.keys():
                if key in keyheader:
                    currentrow.append(review.ReviewerID.__dict__.get(key))
            currentrow.append(review.PaperID.FilenameOriginal)
            currentrow.append(review.PaperID.Title)
            for key in review.__dict__.keys():
                if key in keyheader:
                    currentrow.append(review.__dict__.get(key))
            csvcontents.append(currentrow)
            print(currentrow)
            currentrow = []
    # If the user clicked Download CSV Link, then return HttpResponse
    if request.method == "GET" and request.GET.get('data') != None:
        print(csvcontents)
        writer.writerows(csvcontents)
        return response
    
    # Pop the header off csvcontents before passing to template
    csvcontents.pop(0)
    context = {
        'review_data' : csvcontents
    }
    
    return render(request, "reviewer_comments_report.html", context)

# Reviewer Report
@admin.site.register_view('reviewer_report', urlname='reviewer_report', name='Reviewer Report')
def reviews_summary_report_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    csvcontents = []
    header = ['LastName', 'FirstName', 'MiddleInitial', 
        'Affiliation', 'Department', 'Address', 'City', 'State', 
        'ZipCode',  'CellNumber', 'WorkNumber', 'Email'
    ]
    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=reviewer_report.csv'
    writer = csv.writer(response)
    
    # Store headers
    csvcontents.append(header)
    currentrow = []

    context = {}
    allReviewers = Reviewer.objects.all()
    reviewerTable = []
    for reviewer in allReviewers:
        reviewerTable.append(reviewer)
        # get data for csv row
        for data in reviewer.__dict__.keys():
            if data in header:
                currentrow.append(reviewer.__dict__.get(data))
        csvcontents.append(currentrow)
        currentrow = []
            

    context['reviewers'] = reviewerTable

    # If the user clicked Download CSV Link, then return HttpResponse
    if request.method == "GET" and request.GET.get('data') != None:
        writer.writerows(csvcontents)
        return response
    return render(request, "reviewer_report.html", context)

# Author Report
@admin.site.register_view('author_report', urlname='author_report', name='Author Report')
def reviews_summary_report_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    csvcontents = []
    header = ['LastName', 'FirstName', 'MiddleInitial', 
        'Affiliation', 'Department', 'Address', 'City', 'State', 
        'ZipCode',  'CellNumber', 'WorkNumber', 'Email'
    ]
    response = HttpResponse(
        content_type='text/csv'
    )
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=author_report.csv'
    writer = csv.writer(response)
    
    # Store headers
    csvcontents.append(header)
    currentrow = []

    context = {}
    allAuthors = Author.objects.all()
    authorTable = []
    for author in allAuthors:
        authorTable.append(author)
        # get data for csv row
        for data in Author.__dict__.keys():
            if data in header:
                currentrow.append(author.__dict__.get(data))
        csvcontents.append(currentrow)
        currentrow = []
            

    context['authors'] = authorTable
    
    # If the user clicked Download CSV Link, then return HttpResponse
    if request.method == "GET" and request.GET.get('data') != None:
        writer.writerows(csvcontents)
        return response
    return render(request, "author_report.html", context)