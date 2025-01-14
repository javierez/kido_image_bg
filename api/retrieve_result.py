import time
import requests

API_KEY="e96c04dc-dfce-4025-9494-225ea940ed92"

def retrieve_image_result(request_id):
    """
    Poll the API until the image generation is complete and return the result URL.
    
    Args:
        request_id (str): The ID received from the generate_image request
        
    Returns:
        str: URL to the generated image
    """
    while True:
        time.sleep(0.5)
        result = requests.get(
            'https://api.bfl.ml/v1/get_result',
            headers={
                'accept': 'application/json',
                'x-key': API_KEY,
            },
            params={
                'id': request_id,
            },
        ).json()
        
        if result["status"] == "Ready":
            return result['result']['sample']
        print(f"Status: {result['status']}")

if __name__ == "__main__":
    # Example usage
    sample_request_id = "963bf3a2-aec4-46bc-a4d6-a114d1147145"
    image_url = retrieve_image_result(sample_request_id)
    print(f"Generated image URL: {image_url}") 