import io
import base64
import requests
import numpy as np
from PIL import Image


class ImageCaptioning:
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", ),
                "api_key": ("STRING", {"default": ""})
            }
        }
        
    RETURN_TYPES = ("STRING", )
    FUNCTION = "analyze_image"
    CATEGORY = "AIRedoon"
    OUTPUT_NODE = True
    
    def analyze_image(self, image, api_key):
        # convert the image tensor to a PIL Image
        image = Image.fromarray(
            np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
        )
        
        # convert the image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        api_url = f""
        payload = {
            
        }
        
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            
            caption = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.RequestException as err:
            caption = f"Error: Unable to generate caption, {err}"
        
        return (caption, )
