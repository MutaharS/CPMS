from django.contrib import admin
from django.shortcuts import render

# Custom admin pages for report generation
# @admin.site.register_view('home', urlname='home_from_admin', name='Home Page')
# def custom_hello(request):
#     context = dict(
#         admin.site.each_context(request),
#     )
#     return render(request, "home.html", context)

@admin.site.register_view('reviews_summary_report', urlname='reviews_summary_report', name='Reviews Summary Report')
def reviews_summary_report_view(request):
    context = dict(
        admin.site.each_context(request),
    )
    return render(request, "reviews_summary_report.html", context)

@admin.site.register_view('reviewer_report', urlname='reviewer_report', name='Reviewer Report')
def reviews_summary_report_view(request):
    context = dict(
        admin.site.each_context(request),
    )
    return render(request, "reviewer_report.html", context)

@admin.site.register_view('author_report', urlname='author_report', name='Author Report')
def reviews_summary_report_view(request):
    context = dict(
        admin.site.each_context(request),
    )
    return render(request, "author_report.html", context)