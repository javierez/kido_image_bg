import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from supabase_connector import get_stories

class StoryViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Story Viewer")
        
        # Configure main window
        self.root.geometry("800x600")
        
        # Get stories
        self.stories = get_stories()
        self.current_story_index = 0
        
        # Create widgets
        self.create_widgets()
        
        # Show first story
        self.show_current_story()
    
    def create_widgets(self):
        # Title label
        self.title_label = ttk.Label(
            self.root, 
            font=("Helvetica", 16, "bold"),
            wraplength=700
        )
        self.title_label.pack(pady=20)
        
        # Image label
        self.image_label = ttk.Label(self.root)
        self.image_label.pack(pady=20)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=20)
        
        ttk.Button(
            nav_frame, 
            text="Previous", 
            command=self.previous_story
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            nav_frame, 
            text="Next", 
            command=self.next_story
        ).pack(side=tk.LEFT, padx=10)
    
    def load_and_resize_image(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        # Resize image maintaining aspect ratio
        max_size = (600, 400)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(img)
    
    def show_current_story(self):
        if not self.stories:
            self.title_label.config(text="No stories available")
            return
        
        story = self.stories[self.current_story_index]
        
        # Update title
        self.title_label.config(text=story.get('title', 'Untitled'))
        
        # Update image
        if story.get('story_image_url'):
            try:
                photo = self.load_and_resize_image(story['story_image_url'])
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference
            except Exception as e:
                self.image_label.config(text=f"Error loading image: {str(e)}")
        else:
            self.image_label.config(text="No image available")
    
    def next_story(self):
        if self.stories:
            self.current_story_index = (self.current_story_index + 1) % len(self.stories)
            self.show_current_story()
    
    def previous_story(self):
        if self.stories:
            self.current_story_index = (self.current_story_index - 1) % len(self.stories)
            self.show_current_story()

def main():
    root = tk.Tk()
    app = StoryViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 