import os
import httpx
import asyncio
import pytesseract
import discogs_client
from PIL import Image
from google import genai
from pathlib import Path
from typing import Dict, List
from google.genai import types
from google.adk.agents.llm_agent import Agent

DISCOGS_TOKEN = os.getenv('DISCOGS_API_KEY', '')
discogs = discogs_client.Client('DiscogsGeminiClient/1.0', user_token=DISCOGS_TOKEN)

async def search_discogs(query: str) -> dict:
    """
    Asynchronously searches for a specified query in the Discogs database.
    Returns a dictionary with search results including artists, releases, and labels.
    """
    print(f"Agent tool started: Searching for {query}...")
    
    results = await asyncio.to_thread(discogs.search, query)
    serializable_results = []
    count = 0
    for item in results:
        if count >= 10:  # Limit to first 10 results
            break
        
        try:
            result_data = {
                'type': item.type if hasattr(item, 'type') else 'unknown',
                'title': item.title if hasattr(item, 'title') else str(item),
                'id': item.id if hasattr(item, 'id') else None,
            }
            
            if hasattr(item, 'data'):
                if 'year' in item.data:
                    result_data['year'] = item.data['year']
                if 'country' in item.data:
                    result_data['country'] = item.data['country']
                if 'format' in item.data:
                    result_data['format'] = item.data['format']
            
            serializable_results.append(result_data)
            count += 1
        except Exception as e:
            print(f"Error processing result: {e}")
            continue
    
    return {
        'query': query,
        'count': len(serializable_results),
        'results': serializable_results
    }

async def get_release_details(release_id: int) -> dict:
    """
    Query for a release using its Discogs release ID.
    Returns detailed information about the release including title, artists, formats, tracklist, etc.
    """
    if release_id is None:
        return {"error": "Release ID cannot be None"}
    
    print(f"Agent tool started: Querying release ID {release_id}...")
    
    try:
        release = await asyncio.to_thread(discogs.release, release_id)
        
        tracklist_data = []
        
        if hasattr(release, 'tracklist'):
            for track in release.tracklist:
                try:
                    if isinstance(track, dict):
                        track_info = {
                            'position': track.get('position'),
                            'title': track.get('title'),
                            'duration': track.get('duration')
                        }
                    else:
                        track_info = {
                            'position': getattr(track, 'position', None),
                            'title': getattr(track, 'title', None),
                            'duration': getattr(track, 'duration', None)
                        }
                    tracklist_data.append(track_info)
                except Exception as e:
                    print(f"Error processing track: {e}")
                    continue
        
        release_data = {
            'id': release.id,
            'title': release.title if hasattr(release, 'title') else None,
            'year': release.year if hasattr(release, 'year') else None,
            'country': release.country if hasattr(release, 'country') else None,
            'artists': [{'name': artist.name, 'id': artist.id} for artist in release.artists] if hasattr(release, 'artists') else [],
            'labels': [{'name': label.name, 'id': label.id} for label in release.labels] if hasattr(release, 'labels') else [],
            'formats': release.data.get('formats', []) if hasattr(release, 'data') else [],
            'genres': release.genres if hasattr(release, 'genres') else [],
            'styles': release.styles if hasattr(release, 'styles') else [],
            'tracklist': tracklist_data,
        }
        
        return release_data
    except Exception as e:
        return {"error": f"Error querying Discogs: {str(e)}"}

async def get_marketplace_stats(release_id: int, curr_abbr: str = "USD") -> dict:
    """
    Retrieve marketplace statistics for the provided Release ID.
    
    Args:
        release_id: The release ID whose stats are desired
        curr_abbr: Currency for marketplace data (USD, GBP, EUR, CAD, AUD, JPY, CHF, MXN, BRL, NZD, SEK, ZAR). Defaults to USD.
    
    Returns:
        Dictionary with releaseID, lowestPrice, and activeListings.
    """
    if release_id is None:
        return {"error": "Release ID cannot be None"}
    
    print(f"Agent tool started: Fetching marketplace stats for release ID {release_id}...")
    
    url = f"https://api.discogs.com/marketplace/stats/{release_id}"
    if curr_abbr:
        url += f"?curr_abbr={curr_abbr}"
    
    headers = {
        "User-Agent": "DiscogsGeminiClient/1.0"
    }
    
    if DISCOGS_TOKEN:
        headers["Authorization"] = f"Discogs token={DISCOGS_TOKEN}"
    
    try:
        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            lowest_price_data = data.get('lowest_price')
            lowest_price_value = lowest_price_data.get('value') if lowest_price_data else None
            
            return {
                'releaseID': release_id,
                'lowestPrice': lowest_price_value,
                'activeListings': data.get('num_for_sale')
            }
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": f"Error fetching marketplace stats: {str(e)}"}

root_agent = Agent(
    model='gemini-2.0-flash-lite',
    name='discogs_agent',
    description='A Discogs marketplace assistant that can analyze images of albums/vinyl and find pricing. Supports image analysis, searching releases, and analyzing marketplace pricing.',
    instruction='Help users by analyzing images of music releases to extract album information, then search the Discogs database and find the lowest marketplace prices. You can also directly search and analyze pricing when given text queries.',
    tools=[
        search_discogs,
        get_release_details,
        get_marketplace_stats,
)