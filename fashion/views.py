from django.shortcuts import render
import http.client
import json
from .socialScrapper import get_all_video_urls

# Create your views here.
def searchVideo(request):
    return render(request, 'search.html')

def viewVideos(request):
    if request.method == 'POST':
        hashtag = request.POST.get('hashtag', '')
        if not hashtag:
            return render(request, 'result.html', {'error': 'Please provide a hashtag'})
        
        try:
            # Connect to the Instagram API
            conn = http.client.HTTPSConnection("instagram-scraper-stable-api.p.rapidapi.com")
            
            headers = {
                'x-rapidapi-key': "d30c9b20a1mshf7b0cf45d9eb8c4p1b1d51jsn7724536d9cb5",
                'x-rapidapi-host': "instagram-scraper-stable-api.p.rapidapi.com"
            }
            
            conn.request("GET", f"/search_hashtag.php?hashtag={hashtag}", headers=headers)
            
            res = conn.getresponse()
            data = res.read()
            
            # Parse the JSON response
            og_data = data.decode("utf-8")
            og_data_dict = json.loads(og_data)
            
            # Get video URLs using the helper functions
            video_urls = get_all_video_urls(og_data_dict)
            
            return render(request, 'result.html', {
                'video_urls': video_urls,
                'hashtag': hashtag,
                'count': len(video_urls)
            })
            
        except Exception as e:
            return render(request, 'result.html', {'error': f'Error fetching videos: {str(e)}'})
    
    return render(request, 'search.html')