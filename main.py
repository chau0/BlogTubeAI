#!/usr/bin/env python3
"""
YouTube to Blog Converter - Main Entry Point
Transform YouTube videos into well-formatted blog posts using AI.
"""

import os
import sys
import logging
from datetime import datetime
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

from src.youtube_parser import get_video_id, get_video_title
from src.transcript_handler import list_transcript_languages, fetch_transcript
from src.llm_providers import LLMProviderFactory
from src.blog_formatter import format_as_blog, save_blog_to_file
from src.utils import validate_url, create_safe_filename

# Load environment variables
load_dotenv()

console = Console()

def setup_logging():
    """Set up daily rotating log files with consistent naming format."""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Generate log filename with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(logs_dir, f"youtube-blog-converter_{current_date}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")
    return logger

@click.command()
@click.argument('url', required=False)
@click.option('--language', '-l', default=None, help='Transcript language code (e.g., en, es, fr)')
@click.option('--provider', '-p', default='openai', 
              type=click.Choice(['openai', 'claude', 'gemini', 'azureopenai']), 
              help='LLM provider to use')
@click.option('--output', '-o', default=None, help='Output file path')
@click.option('--interactive', '-i', is_flag=True, help='Interactive mode')
def main(url, language, provider, output, interactive):
    """Convert YouTube videos to blog posts using AI."""
    
    # Initialize logging
    logger = setup_logging()
    logger.info("YouTube to Blog Converter started")
    
    console.print(Panel.fit(
        "[bold blue]🎬 YouTube to Blog Converter[/bold blue]\n"
        "Transform videos into engaging blog posts!",
        border_style="blue"
    ))
    
    try:
        # Interactive mode or get URL
        if interactive or not url:
            url = Prompt.ask("Enter YouTube URL")
        
        logger.info(f"Processing URL: {url}")
        
        # Validate URL and extract video ID
        if not validate_url(url):
            logger.error("Invalid YouTube URL format")
            console.print("[red]❌ Invalid YouTube URL format[/red]")
            sys.exit(1)
            
        video_id = get_video_id(url)
        if not video_id:
            logger.error("Could not extract video ID from URL")
            console.print("[red]❌ Could not extract video ID from URL[/red]")
            sys.exit(1)
            
        logger.info(f"Video ID extracted: {video_id}")
        console.print(f"[green]✅ Video ID extracted: {video_id}[/green]")
        
        # Get video title
        video_title = get_video_title(video_id)
        logger.info(f"Video title: {video_title}")
        console.print(f"[blue]📹 Video: {video_title}[/blue]")
        
        # List available languages
        console.print("[yellow]🔍 Fetching available transcript languages...[/yellow]")
        logger.info("Fetching available transcript languages")
        languages = list_transcript_languages(video_id)
        
        if not languages:
            logger.error("No transcripts available for this video")
            console.print("[red]❌ No transcripts available for this video[/red]")
            sys.exit(1)
            
        logger.info(f"Found {len(languages)} available transcript languages")
        
        # Display available languages
        table = Table(title="Available Transcript Languages")
        table.add_column("Code", style="cyan")
        table.add_column("Language", style="green")
        
        for lang in languages:
            table.add_row(lang['language_code'], lang['language'])
            
        console.print(table)
        
        # Select language
        if not language:
            language = Prompt.ask(
                "Select language code", 
                default=languages[0]['language_code'],
                choices=[lang['language_code'] for lang in languages]
            )
        
        logger.info(f"Selected language: {language}")
        
        # Select LLM provider if not specified or in interactive mode
        if not provider or interactive:
            available_providers = ['openai', 'claude', 'gemini', 'azureopenai']
            
            # Display available providers
            provider_table = Table(title="Available LLM Providers")
            provider_table.add_column("Provider", style="cyan")
            provider_table.add_column("Description", style="green")
            
            provider_descriptions = {
                'openai': 'OpenAI GPT models',
                'claude': 'Anthropic Claude models',
                'gemini': 'Google Gemini models',
                'azureopenai': 'Azure OpenAI Service'
            }
            
            for prov in available_providers:
                provider_table.add_row(prov, provider_descriptions[prov])
            
            console.print(provider_table)
            
            provider = Prompt.ask(
                "Select LLM provider",
                default='openai',
                choices=available_providers
            )
        
        logger.info(f"Selected LLM provider: {provider}")
            
        # Fetch transcript
        console.print(f"[yellow]📝 Fetching transcript in '{language}'...[/yellow]")
        logger.info(f"Fetching transcript in language: {language}")
        transcript = fetch_transcript(video_id=video_id, language_code=language,save_to_file=True)
        
        if not transcript:
            logger.error("Could not fetch transcript")
            console.print("[red]❌ Could not fetch transcript[/red]")
            sys.exit(1)
            
        logger.info(f"Transcript fetched successfully ({len(transcript)} characters)")
        console.print(f"[green]✅ Transcript fetched ({len(transcript)} characters)[/green]")
        
        # Generate blog using LLM
        console.print(f"[yellow]🤖 Generating blog using {provider}...[/yellow]")
        logger.info(f"Generating blog using LLM provider: {provider}")
        llm = LLMProviderFactory.create_provider(provider)
        blog_content = llm.generate_blog(transcript, video_title, url)
        
        if not blog_content:
            logger.error("Failed to generate blog content")
            console.print("[red]❌ Failed to generate blog content[/red]")
            sys.exit(1)
            
        logger.info("Blog content generated successfully")
        
        # Format as markdown blog
        formatted_blog = format_as_blog(blog_content, video_title, url)
        
        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to file
        if not output:
            safe_title = create_safe_filename(video_title)
            output = os.path.join(output_dir, f"{safe_title}_{video_id}.md")
        else:
            # If user provided custom output path, ensure it's in the output directory
            if not output.startswith(output_dir):
                output = os.path.join(output_dir, os.path.basename(output))
            
        logger.info(f"Saving blog to file: {output}")
        success = save_blog_to_file(formatted_blog, output)
        
        if success:
            logger.info(f"Blog saved successfully to: {output}")
            console.print(f"[green]🎉 Blog saved successfully to: {output}[/green]")
            
            if Confirm.ask("Would you like to preview the blog?"):
                console.print(Panel(formatted_blog[:500] + "...", title="Blog Preview"))
        else:
            logger.error("Failed to save blog file")
            console.print("[red]❌ Failed to save blog file[/red]")
            
        logger.info("YouTube to Blog Converter completed successfully")
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        console.print(f"[red]💥 Unexpected error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
