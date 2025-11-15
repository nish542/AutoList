from PIL import Image
import torch
import io
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from sklearn.cluster import KMeans
import colorsys
from app.utils.lazy_loader import get_device, get_blip_models, get_clip_models


class ImageExtractor:
    def __init__(self):
        # Device detection (do not load models at import time)
        self.device = get_device()
        self.blip_processor = None
        self.blip_model = None
        self.clip_processor = None
        self.clip_model = None
        
        # Comprehensive color detection with more colors and variations
        self.color_names = {
            # Primary colors
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255],
            
            # Basic colors
            'black': [0, 0, 0],
            'white': [255, 255, 255],
            'gray': [128, 128, 128],
            'silver': [192, 192, 192],
            'yellow': [255, 255, 0],
            'orange': [255, 165, 0],
            'purple': [128, 0, 128],
            'pink': [255, 192, 203],
            'brown': [165, 42, 42],
            
            # Extended colors
            'navy': [0, 0, 128],
            'teal': [0, 128, 128],
            'lime': [0, 255, 0],
            'cyan': [0, 255, 255],
            'magenta': [255, 0, 255],
            'maroon': [128, 0, 0],
            'olive': [128, 128, 0],
            'gold': [255, 215, 0],
            'beige': [245, 245, 220],
            'tan': [210, 180, 140],
            'coral': [255, 127, 80],
            'salmon': [250, 128, 114],
            'peach': [255, 218, 185],
            'lavender': [230, 230, 250],
            'mint': [189, 252, 201],
            'ivory': [255, 255, 240],
            'pearl': [234, 234, 234],
            'charcoal': [54, 54, 54],
            'burgundy': [128, 0, 32],
            'turquoise': [64, 224, 208],
            'indigo': [75, 0, 130],
            'violet': [238, 130, 238],
            'crimson': [220, 20, 60],
            'rose': [255, 0, 127],
            'bronze': [205, 127, 50],
            'copper': [184, 115, 51],
            'platinum': [229, 228, 226],
            'khaki': [240, 230, 140],
            'forest_green': [34, 139, 34],
            'sky_blue': [135, 206, 235],
            'midnight_blue': [25, 25, 112],
            'royal_blue': [65, 105, 225],
            'hot_pink': [255, 105, 180],
            'deep_purple': [103, 58, 183],
            'amber': [255, 191, 0],
            'emerald': [80, 200, 120],
            'ruby': [224, 17, 95],
            'sapphire': [15, 82, 186],
        }
        
        # Extended object detection labels
        self.object_labels = [
            # Electronics
            "headphones", "earphones", "earbuds", "speaker", "microphone",
            "phone", "smartphone", "tablet", "laptop", "computer", "monitor",
            "keyboard", "mouse", "camera", "charger", "cable", "adapter",
            "powerbank", "smartwatch", "fitness tracker",
            
            # Fashion & Accessories
            "shirt", "t-shirt", "jacket", "coat", "dress", "pants", "jeans",
            "shorts", "skirt", "sweater", "hoodie", "suit", "tie",
            "bag", "backpack", "purse", "wallet", "belt", "hat", "cap",
            "scarf", "gloves", "shoes", "boots", "sneakers", "sandals",
            "watch", "jewelry", "necklace", "bracelet", "ring", "earrings",
            "sunglasses", "glasses",
            
            # Home & Kitchen
            "bottle", "cup", "mug", "glass", "plate", "bowl", "pot", "pan",
            "knife", "fork", "spoon", "container", "box", "jar", "can",
            "furniture", "chair", "table", "sofa", "bed", "lamp", "mirror",
            "pillow", "blanket", "towel", "mat", "rug", "curtain",
            
            # Sports & Outdoors
            "ball", "bat", "racket", "golf club", "weights", "dumbbell",
            "yoga mat", "exercise mat", "gym equipment", "bicycle", "helmet",
            "tent", "sleeping bag", "backpack", "water bottle", "cooler",
            
            # General
            "book", "notebook", "pen", "pencil", "paper", "toy", "game",
            "tool", "instrument", "device", "gadget", "appliance",
            "packaging", "box", "case", "cover", "stand", "holder",
            "electronics", "accessories", "clothing", "sports equipment"
        ]
        
        # Material detection keywords for visual analysis
        self.material_indicators = {
            'metallic': ['shiny', 'reflective', 'chrome', 'steel', 'aluminum'],
            'plastic': ['matte', 'glossy', 'transparent', 'colored'],
            'fabric': ['textured', 'soft', 'woven', 'knitted'],
            'leather': ['grain', 'smooth', 'textured', 'brown', 'black'],
            'wood': ['grain', 'brown', 'natural', 'textured'],
            'glass': ['transparent', 'clear', 'reflective', 'smooth'],
            'ceramic': ['glossy', 'matte', 'smooth', 'white']
        }
    
    def extract_features(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Extract comprehensive features from image
        """
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Basic image properties
        image_properties = self._extract_image_properties(image)
        
        # Generate multiple captions for richer description
        captions = self._generate_comprehensive_captions(image)
        
        # Extract visual features with CLIP
        visual_features = self._extract_visual_features(image)
        
        # Comprehensive color analysis
        color_analysis = self._comprehensive_color_analysis(image)
        
        # Advanced object detection
        detected_objects = self._detect_objects_comprehensive(image)
        
        # Texture and pattern analysis
        texture_analysis = self._analyze_texture_patterns(image)
        
        # Composition analysis
        composition = self._analyze_composition(image)
        
        # Quality assessment
        quality_metrics = self._assess_image_quality(image)
        
        # Material inference from visual cues
        inferred_materials = self._infer_materials(image, detected_objects)
        
        # Brand/logo detection hints
        brand_hints = self._detect_brand_hints(image)
        
        # Aggregate all features
        return {
            "image_properties": image_properties,
            "captions": captions,
            "visual_features": visual_features,
            "color_analysis": color_analysis,
            "detected_objects": detected_objects,
            "texture_analysis": texture_analysis,
            "composition": composition,
            "quality_metrics": quality_metrics,
            "inferred_materials": inferred_materials,
            "brand_hints": brand_hints,
            
            # Legacy compatibility
            "caption": captions[0] if captions else "",
            "dominant_colors": color_analysis.get("dominant_colors", []),
            "object_tags": detected_objects.get("primary_objects", []),
            "image_size": image.size
        }
    
    def _extract_image_properties(self, image: Image) -> Dict[str, Any]:
        """Extract basic image properties"""
        width, height = image.size
        aspect_ratio = width / height
        
        # Determine orientation
        if aspect_ratio > 1.2:
            orientation = "landscape"
        elif aspect_ratio < 0.8:
            orientation = "portrait"
        else:
            orientation = "square"
        
        # Determine size category
        total_pixels = width * height
        if total_pixels < 100000:
            size_category = "small"
        elif total_pixels < 1000000:
            size_category = "medium"
        else:
            size_category = "large"
        
        return {
            "width": width,
            "height": height,
            "aspect_ratio": round(aspect_ratio, 2),
            "orientation": orientation,
            "size_category": size_category,
            "total_pixels": total_pixels,
            "format": image.format if image.format else "unknown",
            "mode": image.mode
        }
    
    def _generate_comprehensive_captions(self, image: Image) -> List[str]:
        """Generate multiple detailed captions"""
        captions = []
        
        # Lazy-load BLIP models if needed
        if self.blip_processor is None or self.blip_model is None:
            try:
                proc, model = get_blip_models()
                self.blip_processor = proc
                self.blip_model = model.to(self.device)
            except Exception as e:
                print(f"BLIP load error: {e}")
                return ["Product image"]
        
        try:
            # Generate multiple captions with different parameters
            for max_length in [30, 50, 75]:
                inputs = self.blip_processor(image, return_tensors="pt")
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Generate with different temperatures for variety
                for temperature in [0.7, 1.0]:
                    out = self.blip_model.generate(
                        **inputs, 
                        max_length=max_length,
                        temperature=temperature,
                        do_sample=True,
                        top_p=0.9
                    )
                    caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
                    if caption and caption not in captions:
                        captions.append(caption)
            
            # Also generate a deterministic caption
            inputs = self.blip_processor(image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            out = self.blip_model.generate(**inputs, max_length=50)
            caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
            if caption and caption not in captions:
                captions.append(caption)
                
        except Exception as e:
            print(f"Caption generation error: {e}")
            captions.append("Product image")
        
        return captions[:5]  # Return up to 5 unique captions
    
    def _comprehensive_color_analysis(self, image: Image) -> Dict[str, Any]:
        """Perform comprehensive color analysis"""
        # Resize for faster processing
        small_image = image.resize((150, 150))
        pixels = np.array(small_image).reshape(-1, 3)
        
        # Find dominant colors using KMeans clustering
        n_colors = min(5, len(np.unique(pixels, axis=0)))  # Up to 5 dominant colors
        if n_colors > 1:
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            dominant_rgb_values = kmeans.cluster_centers_.astype(int)
            
            # Get color percentages
            labels = kmeans.labels_
            color_percentages = []
            for i in range(n_colors):
                percentage = (labels == i).sum() / len(labels)
                color_percentages.append(round(percentage * 100, 1))
        else:
            dominant_rgb_values = [pixels.mean(axis=0).astype(int)]
            color_percentages = [100.0]
        
        # Map RGB to color names
        dominant_colors = []
        color_details = []
        
        for rgb, percentage in zip(dominant_rgb_values, color_percentages):
            color_name = self._get_closest_color_name(rgb)
            dominant_colors.append(color_name)
            
            # Get HSV values for additional analysis
            hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            
            color_details.append({
                "name": color_name,
                "rgb": rgb.tolist(),
                "hex": '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]),
                "percentage": percentage,
                "hsv": {
                    "hue": round(hsv[0] * 360),
                    "saturation": round(hsv[1] * 100),
                    "value": round(hsv[2] * 100)
                }
            })
        
        # Analyze overall color properties
        avg_rgb = pixels.mean(axis=0)
        avg_hsv = colorsys.rgb_to_hsv(avg_rgb[0]/255, avg_rgb[1]/255, avg_rgb[2]/255)
        
        # Determine color mood
        brightness = avg_hsv[2]
        saturation = avg_hsv[1]
        
        if brightness > 0.7:
            mood = "bright"
        elif brightness < 0.3:
            mood = "dark"
        else:
            mood = "neutral"
        
        if saturation > 0.7:
            vibrancy = "vibrant"
        elif saturation < 0.3:
            vibrancy = "muted"
        else:
            vibrancy = "moderate"
        
        # Check for monochrome
        is_monochrome = saturation < 0.1
        
        # Detect color scheme
        color_scheme = self._detect_color_scheme(dominant_rgb_values)
        
        return {
            "dominant_colors": dominant_colors,
            "color_details": color_details,
            "average_color": self._get_closest_color_name(avg_rgb),
            "mood": mood,
            "vibrancy": vibrancy,
            "is_monochrome": is_monochrome,
            "color_scheme": color_scheme,
            "unique_colors_count": len(np.unique(pixels, axis=0))
        }
    
    def _get_closest_color_name(self, rgb: np.ndarray) -> str:
        """Get the closest color name for an RGB value"""
        min_dist = float('inf')
        closest_color = 'unknown'
        
        for color_name, color_rgb in self.color_names.items():
            dist = np.linalg.norm(rgb - color_rgb)
            if dist < min_dist:
                min_dist = dist
                closest_color = color_name.replace('_', ' ')
        
        return closest_color
    
    def _detect_color_scheme(self, colors: np.ndarray) -> str:
        """Detect the color scheme type"""
        if len(colors) == 1:
            return "monochromatic"
        
        # Convert to HSV for analysis
        hsv_colors = []
        for rgb in colors:
            hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            hsv_colors.append(hsv)
        
        # Analyze hue differences
        hues = [h[0] * 360 for h in hsv_colors]
        hue_diffs = []
        for i in range(len(hues)):
            for j in range(i+1, len(hues)):
                diff = abs(hues[i] - hues[j])
                hue_diffs.append(min(diff, 360 - diff))
        
        avg_hue_diff = np.mean(hue_diffs) if hue_diffs else 0
        
        if avg_hue_diff < 30:
            return "analogous"
        elif 150 < avg_hue_diff < 210:
            return "complementary"
        elif 110 < avg_hue_diff < 130:
            return "triadic"
        else:
            return "mixed"
    
    def _detect_objects_comprehensive(self, image: Image) -> Dict[str, Any]:
        """Comprehensive object detection"""
        detected = {
            "primary_objects": [],
            "secondary_objects": [],
            "object_confidences": {},
            "object_categories": {},
            "total_objects_detected": 0
        }
        
        # Lazy-load CLIP models if needed
        if self.clip_processor is None or self.clip_model is None:
            try:
                proc, model = get_clip_models()
                self.clip_processor = proc
                self.clip_model = model.to(self.device)
            except Exception as e:
                print(f"CLIP load error: {e}")
                return detected
        
        try:
            # Process in batches for efficiency
            batch_size = 20
            all_scores = []
            
            for i in range(0, len(self.object_labels), batch_size):
                batch_labels = self.object_labels[i:i+batch_size]
                
                inputs = self.clip_processor(
                    text=batch_labels,
                    images=image,
                    return_tensors="pt",
                    padding=True
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                outputs = self.clip_model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1)
                
                # Store scores
                batch_scores = probs[0].detach().cpu().tolist()
                all_scores.extend(batch_scores)
            
            # Sort objects by confidence
            object_scores = list(zip(self.object_labels, all_scores))
            object_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Categorize objects by confidence
            for obj, score in object_scores:
                if score > 0.3:  # High confidence
                    detected["primary_objects"].append(obj)
                    detected["object_confidences"][obj] = round(score, 3)
                elif score > 0.15:  # Medium confidence
                    detected["secondary_objects"].append(obj)
                    detected["object_confidences"][obj] = round(score, 3)
                
                # Categorize by type
                if "electronic" in obj or "phone" in obj or "computer" in obj:
                    category = "electronics"
                elif "shirt" in obj or "dress" in obj or "pants" in obj:
                    category = "clothing"
                elif "bag" in obj or "wallet" in obj or "belt" in obj:
                    category = "accessories"
                elif "bottle" in obj or "cup" in obj or "plate" in obj:
                    category = "kitchenware"
                elif "mat" in obj or "ball" in obj or "weight" in obj:
                    category = "sports"
                else:
                    category = "general"
                
                if score > 0.15:
                    if category not in detected["object_categories"]:
                        detected["object_categories"][category] = []
                    detected["object_categories"][category].append(obj)
            
            detected["total_objects_detected"] = len(detected["primary_objects"]) + len(detected["secondary_objects"])
            
        except Exception as e:
            print(f"Object detection error: {e}")
        
        return detected
    
    def _analyze_texture_patterns(self, image: Image) -> Dict[str, Any]:
        """Analyze texture and patterns in the image"""
        # Convert to grayscale for texture analysis
        gray = image.convert('L')
        gray_array = np.array(gray)
        
        # Calculate texture metrics
        # Standard deviation indicates texture complexity
        texture_complexity = np.std(gray_array)
        
        # Edge detection for pattern analysis
        edges = np.gradient(gray_array)
        edge_density = np.mean(np.abs(edges))
        
        # Determine texture type
        if texture_complexity < 10:
            texture_type = "smooth"
        elif texture_complexity < 30:
            texture_type = "subtle"
        elif texture_complexity < 60:
            texture_type = "moderate"
        else:
            texture_type = "rough"
        
        # Pattern detection
        patterns = []
        if edge_density > 50:
            patterns.append("geometric")
        if texture_complexity > 40 and edge_density < 30:
            patterns.append("organic")
        
        # Check for specific patterns
        fft = np.fft.fft2(gray_array)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)
        
        # Look for regular patterns in frequency domain
        if np.max(magnitude[1:]) > np.mean(magnitude) * 10:
            patterns.append("repetitive")
        
        return {
            "texture_type": texture_type,
            "texture_complexity": round(float(texture_complexity), 2),
            "edge_density": round(float(edge_density), 2),
            "patterns": patterns,
            "surface_appearance": self._infer_surface_appearance(texture_complexity, edge_density)
        }
    
    def _infer_surface_appearance(self, complexity: float, edge_density: float) -> str:
        """Infer surface appearance from texture metrics"""
        if complexity < 10 and edge_density < 20:
            return "glossy"
        elif complexity < 20 and edge_density > 30:
            return "matte"
        elif complexity > 50:
            return "textured"
        elif edge_density > 60:
            return "patterned"
        else:
            return "standard"
    
    def _analyze_composition(self, image: Image) -> Dict[str, Any]:
        """Analyze image composition"""
        width, height = image.size
        
        # Convert to array for analysis
        img_array = np.array(image)
        
        # Find the main subject area (simplified)
        # Using brightness changes to detect subject
        gray = np.array(image.convert('L'))
        
        # Find center of mass
        y_coords, x_coords = np.ogrid[:height, :width]
        total_brightness = gray.sum()
        
        if total_brightness > 0:
            x_center = (gray * x_coords).sum() / total_brightness
            y_center = (gray * y_coords).sum() / total_brightness
            
            # Determine composition type
            x_ratio = x_center / width
            y_ratio = y_center / height
            
            if 0.4 < x_ratio < 0.6 and 0.4 < y_ratio < 0.6:
                composition_type = "centered"
            elif x_ratio < 0.33 or x_ratio > 0.67:
                composition_type = "rule_of_thirds"
            else:
                composition_type = "off_center"
        else:
            composition_type = "unknown"
            x_center = width / 2
            y_center = height / 2
        
        # Background analysis
        # Check corners for background consistency
        corners = [
            img_array[0:50, 0:50],
            img_array[0:50, -50:],
            img_array[-50:, 0:50],
            img_array[-50:, -50:]
        ]
        
        corner_colors = [np.mean(corner, axis=(0,1)) for corner in corners]
        background_variance = np.std(corner_colors)
        
        if background_variance < 20:
            background_type = "uniform"
        elif background_variance < 50:
            background_type = "simple"
        else:
            background_type = "complex"
        
        return {
            "composition_type": composition_type,
            "subject_position": {
                "x": round(float(x_center), 1),
                "y": round(float(y_center), 1),
                "x_ratio": round(float(x_center/width), 2),
                "y_ratio": round(float(y_center/height), 2)
            },
            "background_type": background_type,
            "background_variance": round(float(background_variance), 2),
            "has_clear_subject": background_variance > 30
        }
    
    def _assess_image_quality(self, image: Image) -> Dict[str, Any]:
        """Assess image quality metrics"""
        img_array = np.array(image)
        
        # Sharpness estimation using Laplacian
        gray = np.array(image.convert('L'))
        laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        
        # Simplified convolution for sharpness
        sharpness = np.std(gray) * 0.1  # Simplified metric
        
        # Brightness
        brightness = np.mean(img_array)
        
        # Contrast
        contrast = np.std(img_array)
        
        # Saturation (for color images)
        hsv = np.array(image.convert('HSV'))
        saturation = np.mean(hsv[:, :, 1])
        
        # Quality assessment
        quality_score = 0
        quality_issues = []
        
        if sharpness > 5:
            quality_score += 25
        else:
            quality_issues.append("low_sharpness")
        
        if 50 < brightness < 200:
            quality_score += 25
        else:
            quality_issues.append("brightness_issue")
        
        if contrast > 30:
            quality_score += 25
        else:
            quality_issues.append("low_contrast")
        
        if saturation > 30:
            quality_score += 25
        else:
            quality_issues.append("low_saturation")
        
        # Determine overall quality
        if quality_score >= 75:
            overall_quality = "high"
        elif quality_score >= 50:
            overall_quality = "medium"
        else:
            overall_quality = "low"
        
        return {
            "overall_quality": overall_quality,
            "quality_score": quality_score,
            "sharpness": round(float(sharpness), 2),
            "brightness": round(float(brightness), 2),
            "contrast": round(float(contrast), 2),
            "saturation": round(float(saturation), 2),
            "quality_issues": quality_issues,
            "is_professional": quality_score >= 75 and len(quality_issues) == 0
        }
    
    def _infer_materials(self, image: Image, detected_objects: Dict) -> List[str]:
        """Infer possible materials from visual cues"""
        inferred_materials = []
        
        # Get image properties for inference
        img_array = np.array(image)
        brightness = np.mean(img_array)
        
        # Check for metallic appearance (high brightness, low saturation)
        hsv = np.array(image.convert('HSV'))
        avg_saturation = np.mean(hsv[:, :, 1])
        
        if brightness > 180 and avg_saturation < 50:
            inferred_materials.append("metal")
            if brightness > 220:
                inferred_materials.append("stainless steel")
        
        # Check for plastic (moderate brightness, varied colors)
        if 100 < brightness < 200 and avg_saturation > 30:
            inferred_materials.append("plastic")
        
        # Check based on detected objects
        primary_objects = detected_objects.get("primary_objects", [])
        
        for obj in primary_objects:
            if "leather" in obj or "bag" in obj or "wallet" in obj:
                inferred_materials.append("leather")
            elif "fabric" in obj or "shirt" in obj or "clothing" in obj:
                inferred_materials.append("fabric")
            elif "glass" in obj or "bottle" in obj:
                inferred_materials.append("glass")
            elif "wood" in obj or "wooden" in obj:
                inferred_materials.append("wood")
            elif "ceramic" in obj or "mug" in obj or "plate" in obj:
                inferred_materials.append("ceramic")
        
        # Remove duplicates
        return list(set(inferred_materials))
    
    def _detect_brand_hints(self, image: Image) -> Dict[str, Any]:
        """Detect potential brand indicators"""
        # This is a simplified version - real brand detection would require OCR
        brand_hints = {
            "has_text": False,
            "has_logo": False,
            "text_regions": [],
            "potential_brand_colors": []
        }
        
        # Convert to grayscale for analysis
        gray = np.array(image.convert('L'))
        
        # Look for regions with high contrast (potential text/logos)
        edges = np.gradient(gray)
        edge_magnitude = np.sqrt(edges[0]**2 + edges[1]**2)
        
        # Find high contrast regions
        high_contrast_ratio = np.sum(edge_magnitude > 50) / edge_magnitude.size
        
        if high_contrast_ratio > 0.1:
            brand_hints["has_text"] = True
        
        if high_contrast_ratio > 0.05:
            brand_hints["has_logo"] = True
        
        # Check for distinctive brand colors (simplified)
        # Many brands use specific color combinations
        img_array = np.array(image)
        unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
        
        if unique_colors < 10:
            brand_hints["potential_brand_colors"] = ["monochromatic_brand"]
        elif unique_colors < 50:
            brand_hints["potential_brand_colors"] = ["limited_palette_brand"]
        
        return brand_hints
    
    def _extract_visual_features(self, image: Image) -> List[float]:
        """Extract CLIP visual features"""
        # Lazy-load CLIP models if needed
        if self.clip_processor is None or self.clip_model is None:
            try:
                proc, model = get_clip_models()
                self.clip_processor = proc
                self.clip_model = model.to(self.device)
            except Exception as e:
                print(f"CLIP load error: {e}")
                return []

        try:
            inputs = self.clip_processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            image_features = self.clip_model.get_image_features(**inputs)
            return image_features.detach().cpu().numpy().flatten().tolist()
        except Exception as e:
            print(f"Visual feature extraction error: {e}")
            return []