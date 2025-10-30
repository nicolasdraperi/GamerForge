from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os
from datetime import datetime
from django.conf import settings

class LocalImageGenerator:
    def __init__(self):
        
        model_id = "runwayml/stable-diffusion-v1-5"

    
        if torch.backends.mps.is_available() and torch.backends.mps.is_built():
            self.device = "mps"
            dtype = torch.float16
        else:
            self.device = "cpu"
            dtype = torch.float32

      
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            safety_checker=None  
        ).to(self.device)

    def generate(self, prompt: str, num_inference_steps: int = 30, guidance_scale: float = 7.5):
        result = self.pipe(
            prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        )
        image: Image.Image = result.images[0]

        
        filename = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        out_dir = os.path.join(settings.MEDIA_ROOT, "generated")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, filename)

        image.save(out_path)

       
        file_url = settings.MEDIA_URL + "generated/" + filename
        return file_url
