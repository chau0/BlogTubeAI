"""
Blog Formatter and File Writer
Format and save blog content as Markdown files.
"""

import os
from datetime import datetime
from typing import Optional

def format_as_blog(content: str, title: str, video_url: str) -> str:
    """
    Format content as a proper blog post with metadata.
    
    Args:
        content (str): Blog content from LLM
        title (str): Video title
        video_url (str): Original video URL
        
    Returns:
        str: Formatted blog post with metadata
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create blog header with metadata
    header = f"""---
title: "Blog Post from YouTube Video"
date: {current_date}
source: "{video_url}"
original_title: "{title}"
generated_by: "YouTube to Blog Converter"
---

"""
    
    # Add source attribution
    attribution = f"""
---

*This blog post was generated from the YouTube video: [{title}]({video_url})*

*Generated on {current_date} using AI-powered content conversion.*
"""
    
    # Combine header, content, and attribution
    full_blog = header + content + attribution
    
    return full_blog

def save_blog_to_file(content: str, filename: str) -> bool:
    """
    Save blog content to a Markdown file.
    
    Args:
        content (str): Blog content to save
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure filename has .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write content to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return False

def create_blog_summary(content: str) -> str:
    """
    Create a brief summary of the blog content.
    
    Args:
        content (str): Full blog content
        
    Returns:
        str: Brief summary
    """
    # Extract first paragraph after title as summary
    lines = content.split('\n')
    summary_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            summary_lines.append(line)
            if len(' '.join(summary_lines)) > 150:
                break
    
    summary = ' '.join(summary_lines)
    if len(summary) > 200:
        summary = summary[:197] + "..."
    
    return summary

def validate_markdown(content: str) -> bool:
    """
    Basic validation of Markdown content.
    
    Args:
        content (str): Markdown content to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not content or len(content.strip()) < 100:
        return False
    
    # Check for basic Markdown structure
    has_headers = any(line.strip().startswith('#') for line in content.split('\n'))
    has_content = len(content.strip()) > 500
    
    return has_headers and has_content
