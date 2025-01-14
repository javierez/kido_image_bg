import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno del archivo .env

class S3Handler:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_to_s3(self, image_url, request_id):
        """
        Upload an image from URL to S3 bucket
        
        Args:
            image_url (str): URL of the image to upload
            request_id (str): Unique identifier for the image
            
        Returns:
            str: S3 URL of the uploaded image
        """
        try:
            # Download image from URL
            response = requests.get(image_url)
            
            # Generate a unique object name with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            object_name = f"generated_images/{timestamp}_{request_id}.png"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=response.content,
                ContentType='image/png'
            )
            
            # Generate S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
            return s3_url
            
        except requests.RequestException as e:
            raise Exception(f"Failed to download image: {str(e)}")
        except boto3.exceptions.BotoError as e:
            raise Exception(f"S3 upload failed: {str(e)}")