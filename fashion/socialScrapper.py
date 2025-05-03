import json

def extract_video_urls_from_collector(og_data_dict):
    """
    Extracts video URLs from the 'collector' key in the API response.
    """
    video_urls = []
    if 'collector' in og_data_dict and isinstance(og_data_dict['collector'], list):
        for post in og_data_dict['collector']:
            if 'video_url' in post and post['video_url']:
                video_urls.append(post['video_url'])
            if 'carousel_media' in post and isinstance(post['carousel_media'], list):
                for item in post['carousel_media']:
                    if 'video_url' in item and item['video_url']:
                        video_urls.append(item['video_url'])
    return video_urls

def extract_video_urls_from_sections(og_data_dict):
    """
    Extracts video URLs from the 'sections' key in the API response.
    """
    video_urls = []
    try:
        sections = og_data_dict.get('data', {}).get('top', {}).get('sections', [])
        for section in sections:
            layout_content = section.get('layout_content', {})
            # For reels/clips
            one_by_two_item = layout_content.get('one_by_two_item', {})
            clips = one_by_two_item.get('clips', {}).get('items', [])
            for item in clips:
                media = item.get('media', {})
                video_versions = media.get('video_versions', [])
                if video_versions:
                    url = video_versions[0].get('url')
                    if url:
                        video_urls.append(url)
            # For regular media
            medias = layout_content.get('medias', [])
            for media_item in medias:
                media = media_item.get('media', {})
                video_versions = media.get('video_versions', [])
                if video_versions:
                    url = video_versions[0].get('url')
                    if url:
                        video_urls.append(url)
    except Exception as e:
        print(f"Error extracting from sections: {e}")
    return video_urls

def get_all_video_urls(og_data_dict):
    """
    Combines all extraction methods to get all video URLs from the API response.
    """
    urls = set()
    urls.update(extract_video_urls_from_collector(og_data_dict))
    urls.update(extract_video_urls_from_sections(og_data_dict))
    return list(urls)