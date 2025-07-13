"""
YouTube Transcript Handler
Fetch and process YouTube video transcripts.
"""

import re
import os
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def get_youtube_api_instance(proxy_username: Optional[str] = None, proxy_password: Optional[str] = None) -> YouTubeTranscriptApi:
    """
    Get YouTubeTranscriptApi instance with optional proxy configuration.
    
    Args:
        proxy_username (Optional[str]): Proxy username (can also be set via environment variable PROXY_USERNAME)
        proxy_password (Optional[str]): Proxy password (can also be set via environment variable PROXY_PASSWORD)
        
    Returns:
        YouTubeTranscriptApi: Configured API instance
    """
    # Use provided credentials or fall back to environment variables
    username = proxy_username or os.getenv('PROXY_USERNAME')
    password = proxy_password or os.getenv('PROXY_PASSWORD')

    # output log to console when using proxy 
    print(f"Using proxy: {username if username else 'None'}")
    
    if username and password:
        proxy_config = WebshareProxyConfig(
            proxy_username=username,
            proxy_password=password,
        )
        return YouTubeTranscriptApi(proxy_config=proxy_config)
    else:
        # Return default instance without proxy
        return YouTubeTranscriptApi()

def list_transcript_languages(video_id: str, proxy_username: Optional[str] = None, proxy_password: Optional[str] = None) -> List[Dict[str, str]]:
    """
    List all available transcript languages for a video.
    
    Args:
        video_id (str): YouTube video ID
        proxy_username (Optional[str]): Proxy username
        proxy_password (Optional[str]): Proxy password
        
    Returns:
        List[Dict[str, str]]: List of available languages with codes and names
    """
    try:
        api_instance = get_youtube_api_instance(proxy_username, proxy_password)
        transcript_list = api_instance.list(video_id)
        languages = []
        
        for transcript in transcript_list:
            languages.append({
                'language_code': transcript.language_code,
                'language': transcript.language,
                'is_generated': transcript.is_generated,
                'is_translatable': transcript.is_translatable
            })
            
        return languages
        
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except VideoUnavailable:
        raise Exception("Video is unavailable or private")
    except NoTranscriptFound:
        raise Exception("No transcripts found for this video")
    except Exception as e:
        raise Exception(f"Error fetching transcript languages: {str(e)}")

def save_transcript_to_file(transcript: str, video_id: str, output_dir: str = "transcripts", filename: Optional[str] = None) -> str:
    """
    Save transcript to a text file.
    
    Args:
        transcript (str): Transcript text to save
        video_id (str): YouTube video ID
        output_dir (str): Directory to save the file (default: "transcripts")
        filename (Optional[str]): Custom filename (default: "{video_id}_transcript.txt")
        
    Returns:
        str: Path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        filename = f"{video_id}_transcript.txt"
    
    # Ensure filename has .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    file_path = os.path.join(output_dir, filename)
    
    # Save transcript to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"Transcript saved to: {file_path}")
    return file_path

def fetch_transcript(video_id: str, language_code: str = 'en', proxy_username: Optional[str] = None, proxy_password: Optional[str] = None, save_to_file: bool = False, output_dir: str = "transcripts") -> Optional[str]:
    """
    Fetch transcript for a video in specified language.
    
    Args:
        video_id (str): YouTube video ID
        language_code (str): Language code (e.g., 'en', 'es', 'fr')
        proxy_username (Optional[str]): Proxy username
        proxy_password (Optional[str]): Proxy password
        save_to_file (bool): Whether to save transcript to file (default: False)
        output_dir (str): Directory to save the file if save_to_file is True
        
    Returns:
        Optional[str]: Transcript text or None if failed
    """
    try:
        api_instance = get_youtube_api_instance(proxy_username, proxy_password)
        
        # Try to get transcript in specified language using new API
        fetched_transcript = api_instance.fetch(video_id, languages=[language_code])
        
        # Combine all transcript segments
        full_transcript = ""
        for snippet in fetched_transcript:
            text = snippet.text.strip()
            # Clean up transcript text
            text = text.replace('\n', ' ').replace('  ', ' ')
            full_transcript += text + " "
            
        final_transcript = full_transcript.strip()
        
        # Save to file if requested
        if save_to_file and final_transcript:
            save_transcript_to_file(final_transcript, video_id, output_dir)
            
        return final_transcript
        
    except NoTranscriptFound:
        # Try to get any available transcript and translate if needed
        try:
            api_instance = get_youtube_api_instance(proxy_username, proxy_password)
            transcript_list = api_instance.list(video_id)
            
            # Find any available transcript
            for transcript in transcript_list:
                if transcript.is_translatable:
                    # Try to translate to requested language
                    try:
                        translated_transcript = transcript.translate(language_code)
                        fetched_transcript = translated_transcript.fetch()
                        
                        full_transcript = ""
                        for snippet in fetched_transcript:
                            text = snippet.text.strip()
                            text = text.replace('\n', ' ').replace('  ', ' ')
                            full_transcript += text + " "
                            
                        final_transcript = full_transcript.strip()
                        
                        # Save to file if requested
                        if save_to_file and final_transcript:
                            save_transcript_to_file(final_transcript, video_id, output_dir)
                            
                        return final_transcript
                    except:
                        continue
                else:
                    # Use original transcript if translation fails
                    fetched_transcript = transcript.fetch()
                    
                    full_transcript = ""
                    for snippet in fetched_transcript:
                        text = snippet.text.strip()
                        text = text.replace('\n', ' ').replace('  ', ' ')
                        full_transcript += text + " "
                        
                    final_transcript = full_transcript.strip()
                    
                    # Save to file if requested
                    if save_to_file and final_transcript:
                        save_transcript_to_file(final_transcript, video_id, output_dir)
                        
                    return final_transcript
                    
        except Exception:
            pass
            
        return None
        
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")

def clean_transcript_text(transcript: str) -> str:
    """
    Clean and format transcript text.
    
    Args:
        transcript (str): Raw transcript text
        
    Returns:
        str: Cleaned transcript text
    """
    if not transcript:
        return ""
        
    # Remove common transcript artifacts with surrounding spaces
    cleaned = re.sub(r'\s*\[Music\]\s*', ' ', transcript)
    cleaned = re.sub(r'\s*\[Applause\]\s*', ' ', cleaned)
    cleaned = re.sub(r'\s*\[Laughter\]\s*', ' ', cleaned)
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    # Fix common spacing issues
    cleaned = cleaned.replace(' .', '.')
    cleaned = cleaned.replace(' ,', ',')
    cleaned = cleaned.replace(' ?', '?')
    cleaned = cleaned.replace(' !', '!')
    
    return cleaned.strip()
