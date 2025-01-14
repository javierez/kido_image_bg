from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

# Load Supabase credentials from environment variables
SUPABASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL', 'https://tyreswkvywpplsvuddgq.supabase.co')
SUPABASE_KEY = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR5cmVzd2t2eXdwcGxzdnVkZGdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYyNDg4MTMsImV4cCI6MjA0MTgyNDgxM30.Nc9BqTrrZMJ1MiGH3oAZbpZFRmC9cHaISNPhlu-8G3A')

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    """
    Returns the Supabase client instance
    """
    return supabase

def get_stories():
    """
    Fetch all stories from the Stories table
    
    Returns:
        list: List of story data if successful
    """
    try:
        response = supabase.table('Stories').select(
            "story_id",
            "name",
            "description",
            "story_image_url"
        ).execute()
        
        if hasattr(response, 'error') and response.error is not None:
            print('Error fetching stories:', response.error)
            raise Exception(response.error)
            
        return response.data  # Return all stories, not just the first one
        
    except Exception as error:
        print('Error in get_stories:', str(error))
        raise error

def update_story_image_url(story_id, image_url):
    """
    Update the story_image_url field for a specific story
    
    Args:
        story_id (str): ID of the story to update
        image_url (str): S3 URL of the generated image
    """
    try:
        response = supabase.table('Stories').update({
            'story_image_url': image_url
        }).eq('story_id', story_id).execute()
        
        if hasattr(response, 'error') and response.error is not None:
            print('Error updating story image URL:', response.error)
            raise Exception(response.error)
            
        return response.data[0] if response.data else None
        
    except Exception as error:
        print(f'Error updating story {story_id} image URL:', str(error))
        raise error

print (get_stories())
