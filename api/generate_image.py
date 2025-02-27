import os
import requests

def generate_image_for_story(story_id, description, color):
    """
    Generate image for a specific story
    
    Args:
        story_id (str): The ID of the story
        description (str): The story description to use in the prompt
    """
    API_KEY = os.environ.get("BFL_API_KEY", "e96c04dc-dfce-4025-9494-225ea940ed92")
    
    # Create prompt from description
    prompt = f"Pixar styled background that represents the athmosphere of the following story. Colors should be deep {color}-ish. {description}"
    # prompt = f"Pixar styled image that represents the following story. Colors should be deep {color}-ish. They should be in a deep forest. El equipo de aventureros se encuentra frente a un río mágico que bloquea su camino. El río está lleno de números flotantes que forman un acertijo. Para cruzarlo, los aventureros deben encontrar los números correctos que desbloquearán un puente mágico. Cada miembro del equipo tiene un papel especial para ayudar a resolver el acertijo y avanzar más cerca del Árbol de Cristal."
    try:
        request = requests.post(
            'https://api.bfl.ml/v1/flux-pro-1.1',
            headers={
                'accept': 'application/json',
                'x-key': API_KEY,
                'Content-Type': 'application/json',
            },
            json={
                'prompt': prompt,
                'width': 1024,
                'height': 1024,
            },
        ).json()
        
        print(f"Generated image request for story {story_id}")
        return request["id"]
        
    except Exception as e:
        print(f"Error generating image for story {story_id}: {str(e)}")
        raise e 