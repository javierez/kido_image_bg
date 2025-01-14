from generate_image import generate_image_for_story
from retrieve_result import retrieve_image_result
from supabase_connector import get_stories
from image_storage import S3Handler
from supabase_connector import update_story_image_url
import uvicorn
from web_viewer import app

def process_story(story, s3_handler):
    """
    Process a single story: generate image, retrieve it, and upload to S3
    
    Args:
        story (dict): Story data containing id and description
        s3_handler: S3Handler instance
    
    Returns:
        str: S3 URL of the uploaded image
    """
    # Check if story already has an image URL
    if story.get('story_image_url'):
        print(f"Story {story['story_id']} already has an image URL: {story['story_image_url']}")
        return story['story_image_url']
    
    # Generate image
    request_id = generate_image_for_story(story['story_id'], story['description'])
    print(f"Generation started for story {story['story_id']} with request ID: {request_id}")
    
    # Wait for and retrieve the result
    image_url = retrieve_image_result(request_id)
    
    # Upload to S3
    s3_url = s3_handler.upload_to_s3(image_url, f"story_{story['story_id']}")
    
    # Update story in Supabase with S3 URL
    update_story_image_url(story['story_id'], s3_url)
    print(f"Updated story {story['story_id']} with new image URL")
    
    return s3_url

def main():
    try:
        # Procesar las historias primero
        results = []
        stories = get_stories()
        s3_handler = S3Handler(bucket_name="kido-story")
        
        for story in stories:
            try:
                s3_url = process_story(story, s3_handler)
                results.append({
                    'story_id': story['story_id'],
                    'image_url': s3_url
                })
                print(f"Successfully processed story {story['story_id']}")
                print(f"Image stored in S3 at: {s3_url}")
            except Exception as e:
                print(f"Error processing story {story['story_id']}: {str(e)}")
        
        print("\nProcessing complete!")
        print("Results:")
        for result in results:
            print(f"Story {result['story_id']}: {result['image_url']}")
            
        # Iniciar el visor web
        print("\nStarting web viewer at http://localhost:8000")
       #uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()