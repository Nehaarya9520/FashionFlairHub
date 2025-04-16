from django.shortcuts import render

# Create your views here.
def searchVideo(request):
    return render(request, 'search.html')