import os
import time
import requests

def generate_image(prompt):
    """Simple function to generate an image from a prompt"""
    API_KEY = "e96c04dc-dfce-4025-9494-225ea940ed92"
    
    try:
        response = requests.post(
            'https://api.bfl.ml/v1/flux-pro-1.1',
            headers={
                'accept': 'application/json',
                'x-key': API_KEY,
                'Content-Type': 'application/json',
            },
            json={
                'prompt': prompt,
                'width': 1440,  # Maximum allowed width
                'height': 800,  # Multiple of 32, maintains ~16:9 ratio
            },
        )
        
        # Print response for debugging
        print(f"API Response: {response.text}")
        
        request = response.json()
        
        if 'id' not in request:
            print(f"Unexpected API response format: {request}")
            return None
            
        return request["id"]
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        print(f"Full error details: {e.__class__.__name__}")
        return None

def retrieve_image_result(request_id):
    """Poll the API until the image generation is complete and return the result URL."""
    API_KEY = "e96c04dc-dfce-4025-9494-225ea940ed92"
    
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
                'width': 1024,
                'height': 1024/2,
            },
        ).json()
        
        if result["status"] == "Ready":
            return result['result']['sample']
        print(f"Status: {result['status']}")

if __name__ == "__main__":
    # Write your prompt here
    test_prompt = "A background for a Maths button in a web application in minimalistic style but without losing creativity. You will cover every gap of the whole image with operations like +, -, *, /, ^, sqrt, log, sin, cos, tan, graphs, equations, figures, etc. Give more importance to geometric shapes and 3d figures, and to graphs (barcharts or heatmaps or whatever). Everything with a white background and grey-ish colors."
    test_prompt = "nothing yet"
    test_prompt = "Professional marketing photo of a child in a bright modern classroom, showing enthusiastic body language. The child, wearing a neat school uniform or casual clothing, is sitting at a desk leaning forward with engaged posture. Natural daylight streams through classroom windows, creating a warm and inviting learning atmosphere. Clean, uncluttered composition with soft background blur. The scene should feel authentic and candid, perfect for educational marketing. Photorealistic, high-end production quality."

    test_prompt = "Professional marketing photo of a diverse group of elementary school students in a bright, modern classroom. Captured from an angle showing students of different ethnicities and backgrounds engaged in learning, with natural, candid expressions. Students are neatly dressed in casual school attire, sitting at collaborative desk arrangements, focused on their work and not looking at the camera. Natural daylight fills the welcoming space through large windows, creating a warm and inclusive atmosphere. The classroom features colorful educational materials and student artwork on walls. The scene should capture authentic peer interaction and learning enthusiasm while maintaining a clean, uncluttered composition with soft background blur. Photorealistic, high-end production quality, perfect for educational marketing that celebrates diversity and inclusion."


    test_prompt = "Professional marketing photo of a teacher standing in front of a blackboard, engaging with a diverse group of elementary school students in a bright, modern classroom. The teacher is animatedly explaining a lesson, while students are attentively listening and participating. Students are neatly dressed in casual school attire, seated at their desks with focused expressions. Natural daylight streams through large windows, creating a warm and inviting learning atmosphere. The classroom is decorated with colorful educational materials and student artwork on the walls. The scene should capture authentic teacher-student interaction and enthusiasm for learning, while maintaining a clean, uncluttered composition with soft background blur. Photorealistic, high-end production quality, perfect for educational marketing that highlights effective teaching and engagement."
    test_prompt = "Professional marketing photo of a 10-year-old occidental child with straight hair, smiling and engaging in a bright white background. Natural daylight streams, creating a warm and inviting atmosphere. The scene should capture the child's enthusiasm, while maintaining a clean, uncluttered composition with soft white background. Photorealistic, high-end production quality, perfect for marketing."
    test_prompt = "Professional marketing photo of a clean, modern web interface showing a student profile page. The design features a minimalist white background with subtle grey accents. The layout includes: a professional student photo placeholder (showing a 10-year-old student smiling against a white background), clear typography displaying student information, and a modern grade visualization with progress bars or charts in educational blue and green tones. The interface should look sophisticated yet friendly, with ample white space and professional UI elements like tabs, cards, and evaluation criteria sections. The overall composition should be clean and organized, perfect for showcasing an educational assessment platform. High-end production quality with subtle shadows and modern design elements. App is called 'KIDO'. Just display the interface and nothing else. "
    test_prompt = "Professional marketing photo of a modern, primary school (Escuela Educación Primaria if you write any text) for bathed in natural daylight, showcasing a welcoming and inspiring environment. The scene captures the exterior of a well-designed school or learning facility, featuring contemporary architecture, spacious walkways, and green outdoor areas where students interact joyfully. The entrance displays a professional sign symbolizing academic excellence, while large windows hint at dynamic learning spaces inside. In the background, groups of kids playing, reflecting engagement, success, and a thriving academic community. The atmosphere conveys a sense of innovation, progress, and the positive impact of personalized education. Photorealistic, high-end production quality, perfect for educational marketing that highlights institutional growth and academic improvement."
    test_prompt = "Professional marketing visualization of a login page for an educational platform. The design features a clean, modern interface with a minimalist aesthetic, showcasing a user-friendly login form. The background is white with subtle gray accents, and the form includes fields for username and password, along with a prominent 'Login' button. Clear typography enhances readability, and the overall composition is well-organized, ensuring that the login elements are the focal point. Additional elements like a 'Forgot Password?' link and a sign-up prompt for new users are included, maintaining a professional and inviting atmosphere. Photorealistic, high-end production quality, perfect for showcasing an intuitive user experience."
    test_prompt = "Professional marketing visualization of a modern minimalist classroom interior. The scene features a clean, calid, pristine white wall as the main focal point, positioned vertically in the frame (more height than width), with subtle architectural details and soft shadows creating depth. The wall space will serve as a backdrop for interface elements. The classroom has soft, diffused natural lighting from side windows, creating gentle ambient illumination throughout the space without harsh reflections. Minimal classroom furniture features modern geometric wood designs with curved edges. Decorative elements include elegant white ceramic vases containing dried pampas grass and sage-green eucalyptus leaves, placed on floating wooden shelves with clean lines. The color palette is predominantly white and warm beige, with light gray accents and touches of natural wood and greenery. The composition maintains a zen-like simplicity with perfect symmetry and balance. The atmosphere should feel peaceful, organized, and conducive to learning, enhanced by the warmth of wood and greenery. Photorealistic, high-end production quality with a contemporary architectural feel."
    test_prompt = "A background for button for science subject in a webpage in minimalistic style (and a bit realistic style) but without losing creativity. You will cover every gap of the whole image with science and nature elements. The composition should be elegant and well-spaced, with 3D elements like floating probetas and symbols thoughtfully placed throughout ALL areas, including the center. Use varying sizes of elements to create depth, with some larger elements in the foreground and smaller ones in the background. The color scheme should have a white background with subtle grey tones (80% white) and very light green highlights (20% opacity) for contrast. Elements should be distributed evenly but with enough breathing room between them to maintain clarity and elegance."
    # Generate the image
    request_id = generate_image(test_prompt)
    if request_id:
        print(f"Image generation started. Request ID: {request_id}")
        image_url = retrieve_image_result(request_id)
        print(f"Generated image URL: {image_url}")
