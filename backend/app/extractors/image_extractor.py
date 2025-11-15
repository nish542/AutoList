from PIL import Image
import torch
import io
from typing import Dict, Any, List
import numpy as np
from app.utils.lazy_loader import get_device, get_blip_models, get_clip_models

class ImageExtractor:
    def __init__(self):
        # Device detection (do not load models at import time)
        self.device = get_device()
        self.blip_processor = None
        self.blip_model = None
        self.clip_processor = None
        self.clip_model = None
        
        # Color detection
        self.color_names = {
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255],
            'black': [0, 0, 0],
            'white': [255, 255, 255],
            'gray': [128, 128, 128],
            'yellow': [255, 255, 0],
            'orange': [255, 165, 0],
            'purple': [128, 0, 128],
            'pink': [255, 192, 203]
        }
    
    def extract_features(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Extract features from image
        """
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Generate caption
        caption = self._generate_caption(image)
        
        # Extract visual features
        visual_features = self._extract_visual_features(image)
        
        # Detect dominant colors
        colors = self._detect_colors(image)
        
        # Object detection tags
        object_tags = self._detect_objects(image)
        
        return {
            "caption": caption,
            "visual_features": visual_features,
            "dominant_colors": colors,
            "object_tags": object_tags,
            "image_size": image.size
        }
    
    def _generate_caption(self, image: Image) -> str:
        """
        Generate image caption using BLIP
        """
        # Lazy-load BLIP models if needed
        if self.blip_processor is None or self.blip_model is None:
            try:
                proc, model = get_blip_models()
                self.blip_processor = proc
                self.blip_model = model.to(self.device)
            except Exception as e:
                # If BLIP not available, return empty caption
                print(f"BLIP load error: {e}")
                return ""

        inputs = self.blip_processor(image, return_tensors="pt")
        # Move tensors to device if necessary
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        out = self.blip_model.generate(**inputs, max_length=50)
        caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
        return caption
    
    def _extract_visual_features(self, image: Image) -> List[float]:
        """
        Extract CLIP visual features
        """
        # Lazy-load CLIP models if needed
        if self.clip_processor is None or self.clip_model is None:
            try:
                proc, model = get_clip_models()
                self.clip_processor = proc
                self.clip_model = model.to(self.device)
            except Exception as e:
                print(f"CLIP load error: {e}")
                return []

        inputs = self.clip_processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        image_features = self.clip_model.get_image_features(**inputs)
        # Move tensor to CPU before converting to numpy (handles CUDA/MPS devices)
        return image_features.detach().cpu().numpy().flatten().tolist()
    
    def _detect_colors(self, image: Image) -> List[str]:
        """
        Detect dominant colors in image
        """
        # Resize for faster processing
        image = image.resize((150, 150))
        pixels = np.array(image)
        
        # Simple dominant color detection
        avg_color = pixels.mean(axis=(0, 1))
        
        # Find closest named color
        min_dist = float('inf')
        closest_color = 'unknown'
        
        for color_name, color_rgb in self.color_names.items():
            dist = np.linalg.norm(avg_color - color_rgb)
            if dist < min_dist:
                min_dist = dist
                closest_color = color_name
        
        return [closest_color]
    
    def _detect_objects(self, image: Image) -> List[str]:
        """
        Detect objects using CLIP zero-shot classification
        """
        # Common product-related objects
        object_labels = [
            "bottle", "headphones", "watch", "bag", "mat", 
            "mug", "shirt", "case", "electronics", "accessories",
            "clothing", "furniture", "sports equipment"
        ]
        
        # Lazy-load CLIP models if needed
        if self.clip_processor is None or self.clip_model is None:
            try:
                proc, model = get_clip_models()
                self.clip_processor = proc
                self.clip_model = model.to(self.device)
            except Exception as e:
                print(f"CLIP load error: {e}")
                return []

        inputs = self.clip_processor(
            text=object_labels,
            images=image,
            return_tensors="pt",
            padding=True
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.clip_model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        # Get top 3 most likely objects
        top_probs, top_indices = torch.topk(probs[0], k=min(3, len(object_labels)))

        # Convert tensors to Python lists for safe indexing and threshold checks
        top_probs_list = top_probs.detach().cpu().tolist()
        top_indices_list = top_indices.detach().cpu().tolist()

        detected_objects = []
        for idx, prob in zip(top_indices_list, top_probs_list):
            if prob > 0.1:  # Threshold
                detected_objects.append(object_labels[int(idx)])
        
        return detected_objects


