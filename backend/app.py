from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import concurrent.futures
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Keys (should be stored in environment variables)
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')

# API Endpoints
PEXELS_API = "https://api.pexels.com/v1/search"
PIXABAY_API = "https://pixabay.com/api/"
UNSPLASH_API = "https://api.unsplash.com/search/photos"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

def search_pexels(query, per_page=10):
    """Search Pexels API for images"""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}
    
    try:
        response = requests.get(PEXELS_API, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format the response
        results = []
        for photo in data.get("photos", []):
            results.append({
                "id": photo["id"],
                "thumbnail": photo["src"]["medium"],
                "full_size": photo["src"]["original"],
                "width": photo["width"],
                "height": photo["height"],
                "source": "Pexels",
                "source_url": photo["url"],
                "photographer": photo["photographer"],
                "photographer_url": photo["photographer_url"]
            })
        
        return results
    except Exception as e:
        print(f"Pexels API Error: {e}")
        return []

def search_pixabay(query, per_page=10):
    """Search Pixabay API for images"""
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "per_page": per_page,
        "image_type": "photo"
    }
    
    try:
        response = requests.get(PIXABAY_API, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format the response
        results = []
        for hit in data.get("hits", []):
            results.append({
                "id": hit["id"],
                "thumbnail": hit["webformatURL"],
                "full_size": hit["largeImageURL"],
                "width": hit["imageWidth"],
                "height": hit["imageHeight"],
                "source": "Pixabay",
                "source_url": hit["pageURL"],
                "photographer": hit["user"],
                "photographer_url": f"https://pixabay.com/users/{hit['user']}-{hit['user_id']}/"
            })
        
        return results
    except Exception as e:
        print(f"Pixabay API Error: {e}")
        return []

def search_unsplash(query, per_page=10):
    """Search Unsplash API for images"""
    params = {
        "query": query,
        "per_page": per_page,
        "client_id": UNSPLASH_API_KEY
    }
    
    try:
        response = requests.get(UNSPLASH_API, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Format the response
        results = []
        for result in data.get("results", []):
            results.append({
                "id": result["id"],
                "thumbnail": result["urls"]["small"],
                "full_size": result["urls"]["full"],
                "width": result["width"],
                "height": result["height"],
                "source": "Unsplash",
                "source_url": result["links"]["html"],
                "photographer": result["user"]["name"],
                "photographer_url": result["user"]["links"]["html"]
            })
        
        return results
    except Exception as e:
        print(f"Unsplash API Error: {e}")
        return []

def search_wikipedia(query, per_page=10):
    """Search Wikipedia API for images related to a query"""
    # First search for articles related to the query
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 5  # Limit to 5 articles to search for images
    }
    
    try:
        search_response = requests.get(WIKIPEDIA_API, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        # Get page ids from search results
        page_ids = [str(result["pageid"]) for result in search_data.get("query", {}).get("search", [])]
        
        if not page_ids:
            return []
        
        # Get images from these pages
        images_params = {
            "action": "query",
            "format": "json",
            "prop": "images|imageinfo",
            "iiprop": "url|dimensions",
            "pageids": "|".join(page_ids)
        }
        
        images_response = requests.get(WIKIPEDIA_API, params=images_params)
        images_response.raise_for_status()
        images_data = images_response.json()
        
        # Format the response
        results = []
        pages = images_data.get("query", {}).get("pages", {})
        
        for page_id, page_data in pages.items():
            page_title = page_data.get("title", "Wikipedia Article")
            page_url = f"https://en.wikipedia.org/?curid={page_id}"
            
            for image in page_data.get("images", [])[:per_page]:
                image_title = image.get("title", "")
                
                # Filter out non-image files and common Wikipedia icons
                if not any(ext in image_title.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    continue
                if any(icon in image_title.lower() for icon in ['icon', 'logo', 'symbol']):
                    continue
                
                # Get image details
                img_params = {
                    "action": "query",
                    "format": "json",
                    "prop": "imageinfo",
                    "iiprop": "url|dimensions",
                    "titles": image_title
                }
                
                img_response = requests.get(WIKIPEDIA_API, params=img_params)
                img_data = img_response.json()
                
                img_pages = img_data.get("query", {}).get("pages", {})
                for _, img_page_data in img_pages.items():
                    img_info = img_page_data.get("imageinfo", [{}])[0]
                    
                    if img_info and "url" in img_info:
                        results.append({
                            "id": f"wiki_{page_id}_{len(results)}",
                            "thumbnail": img_info["url"],
                            "full_size": img_info["url"],
                            "width": img_info.get("width", 0),
                            "height": img_info.get("height", 0),
                            "source": "Wikipedia",
                            "source_url": page_url,
                            "photographer": "Wikipedia/Commons",
                            "photographer_url": page_url,
                            "description": f"From article: {page_title}"
                        })
                        
                        # Limit to requested number of images
                        if len(results) >= per_page:
                            break
            
            if len(results) >= per_page:
                break
                
        return results
    except Exception as e:
        print(f"Wikipedia API Error: {e}")
        return []

@app.route('/api/search', methods=['GET'])
def search_images():
    """Search for images across multiple APIs"""
    query = request.args.get('query', '')
    per_page = int(request.args.get('per_page', 10))
    sources = request.args.get('sources', 'all')
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Determine which sources to search
    source_list = sources.lower().split(',')
    all_sources = sources.lower() == 'all'
    
    results = []
    
    # Use concurrent futures to make API calls in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        if all_sources or 'pexels' in source_list:
            futures.append(executor.submit(search_pexels, query, per_page))
        
        if all_sources or 'pixabay' in source_list:
            futures.append(executor.submit(search_pixabay, query, per_page))
        
        if all_sources or 'unsplash' in source_list:
            futures.append(executor.submit(search_unsplash, query, per_page))
        
        if all_sources or 'wikipedia' in source_list:
            futures.append(executor.submit(search_wikipedia, query, per_page))
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    
    return jsonify({
        "query": query,
        "results": results,
        "total": len(results)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
