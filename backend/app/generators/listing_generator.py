import json
from pathlib import Path
from typing import Dict, Any, List
import re

class ListingGenerator:
    def __init__(self):
        schema_path = Path(__file__).resolve().parent.parent / "schemas" / "product_schema.json"
        with open(schema_path, "r") as f:
            self.schemas = json.load(f)
        
        # Amazon compliance rules
        self.banned_words = [
            "best", "#1", "number one", "top", "free shipping", 
            "guarantee", "warranty", "sale", "discount", "cheap"
        ]
    
    def generate(self, features: Dict[str, Any], category: str) -> Dict[str, Any]:
        """
        Generate Amazon listing from extracted features
        """
        # Get category schema
        category_schema = self._get_category_schema(category)
        if not category_schema:
            raise ValueError(f"Unknown category: {category}")
        
        # Extract attributes
        attributes = self._extract_attributes(features, category_schema)
        
        # Generate listing components
        title = self._generate_title(attributes, category_schema)
        bullets = self._generate_bullets(attributes, category_schema)
        description = self._generate_description(features, attributes, category_schema)
        search_terms = self._generate_search_terms(features, category_schema)
        
        # Ensure compliance
        title = self._ensure_compliance(title, max_length=200)
        bullets = [self._ensure_compliance(b, max_length=256) for b in bullets]
        description = self._ensure_compliance(description, max_length=2000)
        
        return {
            "category": category_schema["category_name"],
            "title": title,
            "bullets": bullets,
            "description": description,
            "search_terms": search_terms,
            "attributes": attributes
        }
    
    def _get_category_schema(self, category: str) -> Dict:
        """
        Get schema for specific category
        """
        for cat in self.schemas["categories"]:
            if cat["category_id"] == category:
                return cat
        return None
    
    def _extract_attributes(self, features: Dict, schema: Dict) -> Dict[str, Any]:
        """
        Extract attributes from features based on schema
        """
        attributes = {}
        
        # Extract from text features
        if "pattern_features" in features:
            for attr, values in features["pattern_features"].items():
                if values:
                    attributes[attr] = values[0]
        
        # Extract from image features
        if "image_features" in features:
            for img_feat in features.get("image_features", []):
                if "dominant_colors" in img_feat:
                    attributes["color"] = img_feat["dominant_colors"][0]
        
        # Extract brand from entities
        if "entities" in features:
            for entity in features["entities"]:
                if entity["entity"] == "ORG" and "brand" not in attributes:
                    attributes["brand"] = entity["word"]
        
        # Fill missing required fields with defaults
        for field, field_info in schema["required_fields"].items():
            if field not in attributes:
                if field_info["type"] == "text":
                    attributes[field] = "Not specified"
                elif field_info["type"] == "numeric":
                    attributes[field] = field_info.get("min", 0)
                elif field_info["type"] == "boolean":
                    attributes[field] = False
        
        return attributes
    
    def _generate_title(self, attributes: Dict, schema: Dict) -> str:
        """
        Generate product title
        """
        title_format = schema["listing_rules"]["title_format"]
        
        # Replace placeholders
        title = title_format
        title = title.replace("[Brand]", attributes.get("brand", "Generic"))
        title = title.replace("[Color]", attributes.get("color", ""))
        title = title.replace("[Material]", attributes.get("material", ""))
        
        # Handle numeric fields
        for key, value in attributes.items():
            placeholder = f"[{key.replace('_', ' ').title()}]"
            if placeholder in title:
                title = title.replace(placeholder, str(value))
        
        # Clean up empty placeholders
        title = re.sub(r'\[.*?\]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _generate_bullets(self, attributes: Dict, schema: Dict) -> List[str]:
        """
        Generate bullet points
        """
        bullets = []
        priorities = schema["listing_rules"]["bullet_priorities"]
        
        for priority in priorities:
            bullet = ""
            
            if priority == "capacity" and "capacity_ml" in attributes:
                bullet = f"Large {attributes['capacity_ml']}ml capacity perfect for all-day hydration"
            elif priority == "material" and "material" in attributes:
                bullet = f"Durable {attributes['material']} construction ensures long-lasting use"
            elif priority == "battery_life" and "battery_life_hours" in attributes:
                bullet = f"Extended {attributes['battery_life_hours']}-hour battery life for uninterrupted use"
            elif priority == "connectivity" and "connectivity" in attributes:
                bullet = f"Advanced {attributes['connectivity']} technology for stable wireless connection"
            elif priority == "dimensions" and any(k in attributes for k in ["length_cm", "width_cm"]):
                bullet = f"Optimal size for portability and functionality"
            
            if bullet:
                bullets.append(bullet)
        
        # Ensure we have at least 5 bullets
        while len(bullets) < 5:
            bullets.append(f"Premium quality {schema['category_name'].lower()} designed for everyday use")
        
        return bullets[:5]
    
    def _generate_description(self, features: Dict, attributes: Dict, schema: Dict) -> str:
        """
        Generate product description
        """
        category_name = schema["category_name"]
        brand = attributes.get("brand", "our")
        
        description = f"""
        Introducing the {brand} {category_name} - a perfect blend of functionality and style.
        
        This premium {category_name.lower()} features exceptional build quality and thoughtful design 
        that meets your daily needs. Crafted with attention to detail, it offers reliable performance 
        and durability you can count on.
        
        Whether you're a professional or casual user, this {category_name.lower()} delivers the quality 
        and features you're looking for. Its versatile design makes it suitable for various occasions 
        and uses.
        
        Key Features:
        - High-quality construction
        - User-friendly design
        - Versatile functionality
        - Long-lasting durability
        - Modern aesthetics
        
        Experience the difference with this carefully designed {category_name.lower()} that combines 
        practicality with style.
        """
        
        return description.strip()
    
    def _generate_search_terms(self, features: Dict, schema: Dict) -> List[str]:
        """
        Generate search terms
        """
        search_terms = []
        
        # Add category keywords
        search_terms.extend(schema["keywords"])
        
        # Add extracted keywords
        if "keywords" in features:
            search_terms.extend(features["keywords"][:5])
        
        # Add attribute values
        for key, value in features.get("pattern_features", {}).items():
            if isinstance(value, list):
                search_terms.extend(value[:2])
        
        # Remove duplicates and limit to 10
        search_terms = list(set(search_terms))[:10]
        
        return search_terms
    
    def _ensure_compliance(self, text: str, max_length: int) -> str:
        """
        Ensure text meets Amazon compliance rules
        """
        # Remove banned words
        for banned in self.banned_words:
            text = re.sub(rf'\b{banned}\b', '', text, flags=re.IGNORECASE)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Truncate if needed
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        
        # Proper capitalization
        text = '. '.join(s.capitalize() for s in text.split('. '))
        
        return text


