import json
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
import re
import random


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
        
        # Categories for bullet diversity
        self.bullet_categories = [
            "material_quality",
            "functionality",
            "design_aesthetics",
            "performance",
            "value_proposition",
            "use_case",
            "durability",
            "comfort_ergonomics",
            "technology_features",
            "safety_compliance",
            "environmental",
            "convenience"
        ]
    
    def generate(self, features: Dict[str, Any], category: str) -> Dict[str, Any]:
        """
        Generate Amazon listing with 3-5 unique bullet points
        """
        # Get category schema
        category_schema = self._get_category_schema(category)
        if not category_schema:
            category_schema = self._get_category_schema("unknown")
        
        # Extract and enrich attributes
        attributes = self._extract_comprehensive_attributes(features, category_schema)
        
        # Generate enriched title
        title = self._generate_enriched_title(attributes, features, category_schema)
        
        # Generate 3-5 UNIQUE bullet points
        bullets = self._generate_unique_bullets(attributes, features, category_schema)
        
        # Generate comprehensive description
        description = self._generate_comprehensive_description(features, attributes, category_schema)
        
        # Generate extensive search terms
        search_terms = self._generate_extensive_search_terms(features, attributes, category_schema)
        
        # Extract all possible features for backend attributes
        backend_attributes = self._extract_all_attributes(features, attributes)
        
        # Ensure compliance
        title = self._ensure_compliance(title, max_length=200)
        bullets = [self._ensure_compliance(b, max_length=256) for b in bullets]
        description = self._ensure_compliance(description, max_length=2000)
        
        return {
            "category": category_schema["category_name"],
            "title": title,
            "bullets": bullets,  # Will be 3-5 unique bullets
            "description": description,
            "search_terms": search_terms[:50],
            "attributes": backend_attributes,
            "feature_count": len(bullets),
            "extracted_features_summary": self._summarize_features(features)
        }
    
    def _generate_unique_bullets(self, attributes: Dict, features: Dict, schema: Dict) -> List[str]:
        """
        Generate 3-5 unique, non-repetitive bullet points
        Each bullet focuses on a different aspect to ensure diversity
        """
        bullets = []
        used_categories = set()
        used_keywords = set()
        
        # Determine how many bullets to generate (3-5)
        feature_richness = self._calculate_feature_richness(attributes, features)
        if feature_richness > 0.8:
            target_bullets = 5
        elif feature_richness > 0.6:
            target_bullets = 4
        else:
            target_bullets = 3
        
        # Priority order for bullet generation based on what's available
        bullet_generators = [
            ("material_quality", self._generate_material_quality_bullet),
            ("functionality", self._generate_functionality_bullet),
            ("design_aesthetics", self._generate_design_bullet),
            ("performance", self._generate_performance_bullet),
            ("value_proposition", self._generate_value_bullet_unique),
            ("use_case", self._generate_use_case_bullet),
            ("durability", self._generate_durability_bullet_unique),
            ("comfort_ergonomics", self._generate_comfort_bullet_unique),
            ("technology_features", self._generate_technology_bullet),
            ("safety_compliance", self._generate_safety_bullet_unique),
            ("environmental", self._generate_eco_bullet_unique),
            ("convenience", self._generate_convenience_bullet)
        ]
        
        # Shuffle to add variety across different products
        random.shuffle(bullet_generators)
        
        # Generate bullets, ensuring each is unique
        for category, generator in bullet_generators:
            if len(bullets) >= target_bullets:
                break
            
            if category not in used_categories:
                bullet = generator(attributes, features, schema, used_keywords)
                if bullet and self._is_unique_bullet(bullet, bullets, used_keywords):
                    bullets.append(bullet)
                    used_categories.add(category)
                    # Extract key terms from this bullet to avoid repetition
                    self._update_used_keywords(bullet, used_keywords)
        
        # If we don't have enough bullets, generate generic ones
        while len(bullets) < 3:
            generic_bullet = self._generate_generic_unique_bullet(
                attributes, schema, len(bullets), used_keywords
            )
            if generic_bullet and self._is_unique_bullet(generic_bullet, bullets, used_keywords):
                bullets.append(generic_bullet)
                self._update_used_keywords(generic_bullet, used_keywords)
            else:
                break  # Avoid infinite loop
        
        return bullets
    
    def _calculate_feature_richness(self, attributes: Dict, features: Dict) -> float:
        """
        Calculate how feature-rich the product is (0-1 scale)
        """
        score = 0.0
        max_score = 10.0
        
        # Check for various features
        if attributes.get("material") or attributes.get("materials"):
            score += 1
        if attributes.get("color") or attributes.get("colors"):
            score += 1
        if attributes.get("size") or attributes.get("dimensions") or attributes.get("capacity_ml"):
            score += 1
        if attributes.get("brand") and attributes["brand"] != "Premium Brand":
            score += 1
        if attributes.get("connectivity") or attributes.get("battery"):
            score += 1
        if attributes.get("semantic_target_audience"):
            score += 1
        if attributes.get("is_professional"):
            score += 1
        if attributes.get("quality_tier") == "high":
            score += 1
        if "image_descriptions" in attributes:
            score += 1
        if "keywords" in features.get("text_features", {}):
            score += 1
        
        return min(score / max_score, 1.0)
    
    def _is_unique_bullet(self, bullet: str, existing_bullets: List[str], used_keywords: Set[str]) -> bool:
        """
        Check if bullet is unique compared to existing ones
        """
        bullet_lower = bullet.lower()
        
        # Check for similarity with existing bullets
        for existing in existing_bullets:
            existing_lower = existing.lower()
            
            # Check for substantial overlap (more than 30% of words in common)
            bullet_words = set(bullet_lower.split())
            existing_words = set(existing_lower.split())
            
            common_words = bullet_words & existing_words
            # Ignore common words
            common_words -= {'the', 'a', 'an', 'and', 'or', 'for', 'with', 'to', 'in', 'on', 'at', 'by', 'of', 'is', 'are', 'this', 'that'}
            
            if len(common_words) > min(len(bullet_words), len(existing_words)) * 0.3:
                return False
            
            # Check if they start with the same phrase (first 3 words)
            bullet_start = ' '.join(bullet_lower.split()[:3])
            existing_start = ' '.join(existing_lower.split()[:3])
            if bullet_start == existing_start:
                return False
        
        return True
    
    def _update_used_keywords(self, bullet: str, used_keywords: Set[str]):
        """
        Extract and store key terms from bullet to avoid repetition
        """
        # Extract significant words (nouns, adjectives)
        significant_words = []
        words = bullet.lower().split()
        
        for word in words:
            # Skip common words and short words
            if len(word) > 4 and word not in {
                'the', 'and', 'for', 'with', 'that', 'this', 'from', 'your', 
                'ensures', 'provides', 'features', 'includes', 'offers', 'delivers'
            }:
                significant_words.append(word)
        
        # Add top 3 significant words to used keywords
        used_keywords.update(significant_words[:3])
    
    def _generate_material_quality_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on material and build quality
        """
        materials = attributes.get("materials", attributes.get("material", ""))
        texture = attributes.get("texture_type", "")
        surface = attributes.get("surface_appearance", "")
        
        if not materials and not texture:
            return None
        
        # Build bullet parts
        bullet_parts = []
        
        if materials:
            if isinstance(materials, list):
                material_str = materials[0]
            else:
                material_str = str(materials)
            
            # Choose unique phrasing based on material
            if "steel" in material_str.lower():
                bullet_parts.append(f"Rust-resistant {material_str} construction delivers professional-grade durability")
            elif "plastic" in material_str.lower():
                bullet_parts.append(f"Impact-resistant {material_str} withstands daily wear while maintaining lightweight portability")
            elif "fabric" in material_str.lower() or "cotton" in material_str.lower():
                bullet_parts.append(f"Premium {material_str} material offers exceptional comfort and breathability")
            elif "leather" in material_str.lower():
                bullet_parts.append(f"Genuine {material_str} craftsmanship ages beautifully with sophisticated appeal")
            elif "glass" in material_str.lower():
                bullet_parts.append(f"Crystal-clear {material_str} construction combines elegance with functionality")
            else:
                bullet_parts.append(f"High-quality {material_str} ensures long-lasting performance and reliability")
        
        if surface and surface not in str(used_keywords):
            if bullet_parts:
                bullet_parts[0] += f" with {surface} finish"
            else:
                bullet_parts.append(f"Features {surface} finish for enhanced visual appeal and easy maintenance")
        
        return " ".join(bullet_parts) if bullet_parts else None
    
    def _generate_functionality_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on core functionality
        """
        # Extract functional features
        capacity = attributes.get("capacity_ml", "")
        battery = attributes.get("battery", attributes.get("battery_life_hours", ""))
        connectivity = attributes.get("connectivity", "")
        special_features = attributes.get("semantic_special_features", [])
        
        if capacity:
            return f"Generous {capacity}ml capacity accommodates your daily needs while maintaining compact portability"
        elif battery:
            return f"Extended {battery} operation time reduces charging frequency for uninterrupted daily use"
        elif connectivity:
            if isinstance(connectivity, list):
                connectivity = connectivity[0]
            return f"Advanced {connectivity} technology enables seamless device integration and reliable performance"
        elif special_features:
            feature = special_features[0] if isinstance(special_features, list) else special_features
            return f"Innovative {feature} capability distinguishes this product from conventional alternatives"
        else:
            category = schema["category_name"].lower()
            return f"Engineered specifically for optimal {category} performance with user-centric design"
    
    def _generate_design_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on design and aesthetics
        """
        colors = attributes.get("colors", attributes.get("color", ""))
        mood = attributes.get("color_mood", "")
        composition = attributes.get("composition_type", "")
        patterns = attributes.get("patterns", [])
        
        bullet_parts = []
        
        if colors:
            if isinstance(colors, list) and len(colors) > 1:
                bullet_parts.append(f"Available in {len(colors)} sophisticated color options to complement your personal style")
            elif isinstance(colors, list) and colors:
                color = colors[0]
                bullet_parts.append(f"Elegant {color} finish adds contemporary sophistication to any environment")
            elif colors:
                bullet_parts.append(f"Classic {colors} colorway offers timeless appeal and versatile coordination")
        
        if patterns and isinstance(patterns, list) and patterns:
            pattern = patterns[0]
            if not bullet_parts:
                bullet_parts.append(f"Distinctive {pattern} pattern creates visual interest and unique character")
            else:
                bullet_parts[0] += f" featuring {pattern} detailing"
        
        if not bullet_parts:
            bullet_parts.append("Thoughtfully designed aesthetic balances modern style with practical functionality")
        
        return " ".join(bullet_parts)
    
    def _generate_performance_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on performance
        """
        quality_tier = attributes.get("quality_tier", "")
        is_professional = attributes.get("is_professional", False)
        speed = attributes.get("speed", "")
        performance_keywords = attributes.get("keywords_performance", [])
        
        if quality_tier == "high" or is_professional:
            return "Professional-grade components deliver consistent high-performance results exceeding industry standards"
        elif speed:
            if isinstance(speed, list):
                speed = speed[0]
            return f"Optimized {speed} processing speed accelerates task completion and enhances productivity"
        elif performance_keywords:
            keyword = performance_keywords[0] if isinstance(performance_keywords, list) else performance_keywords
            return f"Superior {keyword} performance ensures reliable operation under demanding conditions"
        else:
            return "Precision engineering maximizes efficiency while maintaining exceptional reliability standards"
    
    def _generate_value_bullet_unique(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on value proposition
        """
        price_range = attributes.get("inferred_price_range", "")
        quality_tier = attributes.get("quality_tier", "")
        warranty = attributes.get("warranty", "")
        
        if warranty and "warranty" not in str(used_keywords):
            return f"Protected by comprehensive {warranty} coverage demonstrating manufacturer confidence in quality"
        elif price_range == "budget" and quality_tier == "high":
            return "Exceptional value combines premium features typically found in higher-priced alternatives"
        elif price_range == "premium":
            return "Investment-grade quality justifies premium positioning through superior materials and craftsmanship"
        else:
            return "Smart value proposition balances quality construction with competitive pricing advantage"
    
    def _generate_use_case_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on use cases and versatility
        """
        audiences = attributes.get("semantic_target_audience", [])
        use_environment = attributes.get("inferred_use_environment", "")
        use_cases = attributes.get("use_cases", [])
        
        if audiences and isinstance(audiences, list) and audiences:
            audience_str = ", ".join(audiences[:2])
            return f"Ideal solution for {audience_str} users seeking professional-quality results"
        elif use_cases and isinstance(use_cases, list) and use_cases:
            case = use_cases[0]
            return f"Perfectly suited for {case} with specialized features enhancing user experience"
        elif use_environment:
            return f"Optimized for {use_environment} environments with adaptive functionality"
        else:
            return "Versatile design adapts seamlessly to multiple applications and user preferences"
    
    def _generate_durability_bullet_unique(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on durability
        """
        durability_keywords = attributes.get("keywords_durability", [])
        expected_durability = attributes.get("inferred_expected_durability", "")
        waterproof = "waterproof" in str(attributes).lower()
        shockproof = "shockproof" in str(attributes).lower()
        
        if waterproof and "waterproof" not in str(used_keywords):
            return "Waterproof construction protects against moisture damage in challenging environments"
        elif shockproof and "shockproof" not in str(used_keywords):
            return "Shock-absorbing design safeguards against accidental impacts and vibrations"
        elif durability_keywords:
            keyword = durability_keywords[0] if isinstance(durability_keywords, list) else durability_keywords
            return f"Built with {keyword} construction methods ensuring years of dependable service"
        elif expected_durability == "long-lasting":
            return "Engineered for extended lifespan using time-tested materials and construction techniques"
        else:
            return "Robust build quality withstands intensive use while maintaining optimal performance"
    
    def _generate_comfort_bullet_unique(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on comfort and ergonomics
        """
        comfort_keywords = attributes.get("keywords_comfort", [])
        ergonomic = "ergonomic" in str(attributes).lower()
        soft = "soft" in str(attributes).lower()
        lightweight = "lightweight" in str(attributes).lower()
        
        if ergonomic and "ergonomic" not in str(used_keywords):
            return "Ergonomically optimized design reduces fatigue during extended use periods"
        elif lightweight and "lightweight" not in str(used_keywords):
            weight = attributes.get("weight", "")
            if weight:
                return f"Ultra-lightweight {weight} construction minimizes strain without compromising durability"
            else:
                return "Lightweight engineering enhances portability without sacrificing structural integrity"
        elif soft and "soft" not in str(used_keywords):
            return "Soft-touch surfaces provide luxurious tactile experience and comfortable handling"
        elif comfort_keywords:
            keyword = comfort_keywords[0] if isinstance(comfort_keywords, list) else comfort_keywords
            return f"Enhanced {keyword} features prioritize user comfort throughout extended sessions"
        else:
            return None
    
    def _generate_technology_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on technology features
        """
        smart = any(word in str(attributes).lower() for word in ["smart", "ai", "intelligent"])
        wireless = "wireless" in str(attributes).lower() or "bluetooth" in str(attributes).lower()
        charging = any(word in str(attributes).lower() for word in ["charging", "rechargeable", "usb"])
        
        if smart and "smart" not in str(used_keywords):
            return "Intelligent technology adapts to usage patterns for personalized optimization"
        elif wireless and "wireless" not in str(used_keywords):
            return "Wireless connectivity eliminates cable constraints while maintaining stable connection"
        elif charging and "charging" not in str(used_keywords):
            return "Rapid charging technology minimizes downtime with efficient power management"
        else:
            return None
    
    def _generate_safety_bullet_unique(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on safety and compliance
        """
        safety_keywords = attributes.get("keywords_safety", [])
        certified = "certified" in str(attributes).lower()
        non_toxic = "non-toxic" in str(attributes).lower() or "bpa-free" in str(attributes).lower()
        food_safe = "food" in str(attributes).lower() and "safe" in str(attributes).lower()
        
        if certified and "certified" not in str(used_keywords):
            return "Independently certified to meet stringent safety and quality standards"
        elif non_toxic and "toxic" not in str(used_keywords):
            return "Non-toxic materials ensure safe use for all family members including children"
        elif food_safe and "food" not in str(used_keywords):
            return "Food-grade materials meet FDA requirements for safe contact with consumables"
        elif safety_keywords:
            keyword = safety_keywords[0] if isinstance(safety_keywords, list) else safety_keywords
            return f"Comprehensive {keyword} protocols ensure complete user protection and peace of mind"
        else:
            return None
    
    def _generate_eco_bullet_unique(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on environmental features
        """
        eco_keywords = attributes.get("keywords_eco", [])
        eco_friendly = any(word in str(attributes).lower() for word in ["eco", "sustainable", "recyclable", "green"])
        
        if eco_friendly and "eco" not in str(used_keywords):
            return "Environmentally responsible materials and manufacturing reduce ecological impact"
        elif eco_keywords:
            keyword = eco_keywords[0] if isinstance(eco_keywords, list) else eco_keywords
            return f"Features {keyword} components supporting sustainable lifestyle choices"
        else:
            return None
    
    def _generate_convenience_bullet(self, attributes: Dict, features: Dict, schema: Dict, used_keywords: Set[str]) -> str:
        """
        Generate bullet focusing on convenience and ease of use
        """
        convenience_keywords = attributes.get("keywords_convenience", [])
        dishwasher_safe = attributes.get("dishwasher_safe", False)
        portable = "portable" in str(attributes).lower() or "compact" in str(attributes).lower()
        
        if dishwasher_safe and "dishwasher" not in str(used_keywords):
            return "Dishwasher-safe design simplifies cleaning and maintenance routines"
        elif portable and "portable" not in str(used_keywords):
            return "Compact form factor enables convenient storage and effortless transportation"
        elif convenience_keywords:
            keyword = convenience_keywords[0] if isinstance(convenience_keywords, list) else convenience_keywords
            return f"Intuitive {keyword} operation eliminates learning curve for immediate productivity"
        else:
            return "User-friendly design streamlines operation for enhanced daily convenience"
    
    def _generate_generic_unique_bullet(self, attributes: Dict, schema: Dict, index: int, used_keywords: Set[str]) -> str:
        """
        Generate generic bullet that's still unique
        """
        category = schema["category_name"].lower()
        
        generic_templates = [
            f"Thoughtfully engineered {category} solution addresses common user challenges effectively",
            f"Innovative approach to {category} design sets new benchmark for quality",
            f"Meticulous attention to detail evident throughout entire product construction",
            f"Time-tested design principles ensure consistent satisfaction and reliability",
            f"Customer-focused engineering prioritizes real-world usability and longevity"
        ]
        
        if index < len(generic_templates):
            bullet = generic_templates[index]
            # Check it doesn't overlap with used keywords
            if not any(word in bullet.lower() for word in used_keywords):
                return bullet
        
        return None
    
    def _get_category_schema(self, category: str) -> Dict:
        """Get schema for specific category"""
        for cat in self.schemas["categories"]:
            if cat["category_id"] == category:
                return cat
        return None
    
    def _extract_comprehensive_attributes(self, features: Dict, schema: Dict) -> Dict[str, Any]:
        """Extract comprehensive attributes from all available features"""
        attributes = {}
        
        # Extract from text features
        text_features = features.get("text_features", features)
        if "pattern_features" in text_features:
            for attr, values in text_features["pattern_features"].items():
                if values:
                    if len(values) > 1:
                        attributes[attr] = values
                        attributes[f"{attr}_primary"] = values[0]
                    else:
                        attributes[attr] = values[0]
        
        # Extract semantic features
        if "semantic_features" in text_features:
            for key, value in text_features["semantic_features"].items():
                attributes[f"semantic_{key}"] = value
        
        # Extract inferred features
        if "inferred_features" in text_features:
            for key, value in text_features["inferred_features"].items():
                attributes[f"inferred_{key}"] = value
        
        # Extract categorized keywords
        if "categorized_keywords" in text_features:
            for category, keywords in text_features["categorized_keywords"].items():
                attributes[f"keywords_{category}"] = keywords
        
        # Extract from image features
        if "image_features" in features:
            for img_feat in features.get("image_features", []):
                if "color_analysis" in img_feat:
                    color_data = img_feat["color_analysis"]
                    attributes["colors"] = color_data.get("dominant_colors", [])
                    attributes["color_mood"] = color_data.get("mood", "")
                    attributes["color_vibrancy"] = color_data.get("vibrancy", "")
                
                if "detected_objects" in img_feat:
                    obj_data = img_feat["detected_objects"]
                    attributes["detected_objects"] = obj_data.get("primary_objects", [])
                
                if "texture_analysis" in img_feat:
                    texture_data = img_feat["texture_analysis"]
                    attributes["texture_type"] = texture_data.get("texture_type", "")
                    attributes["surface_appearance"] = texture_data.get("surface_appearance", "")
                    attributes["patterns"] = texture_data.get("patterns", [])
                
                if "quality_metrics" in img_feat:
                    quality = img_feat["quality_metrics"]
                    attributes["image_quality"] = quality.get("overall_quality", "")
                    attributes["is_professional"] = quality.get("is_professional", False)
                
                if "inferred_materials" in img_feat:
                    attributes["materials"] = img_feat["inferred_materials"]
                
                if "captions" in img_feat:
                    attributes["image_descriptions"] = img_feat["captions"]
        
        # Extract brand
        if "entities" in text_features:
            for entity in text_features["entities"]:
                if entity.get("entity") in ["ORG", "MISC"] or entity.get("potential_brand"):
                    attributes["brand"] = entity["word"]
                    break
        
        # Fill missing required fields
        for field, field_info in schema["required_fields"].items():
            if field not in attributes:
                if field_info["type"] == "text":
                    attributes[field] = "Premium"
                elif field_info["type"] == "numeric":
                    attributes[field] = field_info.get("min", 0)
                elif field_info["type"] == "boolean":
                    attributes[field] = False
        
        return attributes
    
    def _generate_enriched_title(self, attributes: Dict, features: Dict, schema: Dict) -> str:
        """Generate enriched product title"""
        title_parts = []
        
        # Brand
        brand = attributes.get("brand", "")
        if brand and brand != "Premium":
            title_parts.append(brand)
        
        # Category
        title_parts.append(schema["category_name"])
        
        # Key specs
        if "capacity_ml" in attributes:
            title_parts.append(f"{attributes['capacity_ml']}ml")
        
        if "colors" in attributes and attributes["colors"]:
            colors = attributes["colors"]
            if isinstance(colors, list) and colors:
                title_parts.append(colors[0].title())
        
        if "materials" in attributes and attributes["materials"]:
            materials = attributes["materials"]
            if isinstance(materials, list) and materials:
                title_parts.append(materials[0].title())
        
        # Special features
        if attributes.get("is_professional"):
            title_parts.append("Professional Grade")
        
        if "wireless" in str(attributes).lower():
            title_parts.append("Wireless")
        
        return " ".join(title_parts)
    
    def _generate_comprehensive_description(self, features: Dict, attributes: Dict, schema: Dict) -> str:
        """Generate comprehensive description"""
        category_name = schema["category_name"]
        brand = attributes.get("brand", "our")
        
        description = f"""
Introducing the {brand} {category_name} - a perfect blend of quality and innovation.

This premium product features exceptional build quality with carefully selected materials 
and thoughtful design. Every detail has been considered to deliver reliable performance 
and user satisfaction.

Key Features:
• Superior construction quality
• Optimized for daily use
• Professional-grade materials
• Versatile functionality
• Long-lasting durability

Whether for professional or personal use, this {category_name.lower()} delivers 
the quality and features you need. Experience the difference that attention to 
detail makes.
        """
        
        return description.strip()
    
    def _generate_extensive_search_terms(self, features: Dict, attributes: Dict, schema: Dict) -> List[str]:
        """Generate search terms"""
        search_terms = set()
        
        # Add category keywords
        search_terms.update(schema.get("keywords", []))
        
        # Add extracted keywords
        text_features = features.get("text_features", features)
        if "keywords" in text_features:
            search_terms.update(text_features["keywords"][:20])
        
        # Add colors
        if "colors" in attributes:
            colors = attributes["colors"]
            if isinstance(colors, list):
                search_terms.update(colors)
        
        # Add materials
        if "materials" in attributes:
            materials = attributes["materials"]
            if isinstance(materials, list):
                search_terms.update(materials)
        
        # Clean and return
        cleaned_terms = []
        for term in search_terms:
            if isinstance(term, str):
                cleaned = term.lower().strip()
                if cleaned and cleaned not in self.banned_words and len(cleaned) > 2:
                    cleaned_terms.append(cleaned)
        
        return cleaned_terms[:50]
    
    def _extract_all_attributes(self, features: Dict, attributes: Dict) -> Dict[str, Any]:
        """Extract all attributes for backend storage"""
        return attributes
    
    def _summarize_features(self, features: Dict) -> Dict[str, int]:
        """Summarize extracted features"""
        summary = {
            "total_keywords": 0,
            "total_entities": 0,
            "total_colors": 0,
            "total_materials": 0
        }
        
        text_features = features.get("text_features", features)
        
        if "keywords" in text_features:
            summary["total_keywords"] = len(text_features["keywords"])
        
        if "entities" in text_features:
            summary["total_entities"] = len(text_features["entities"])
        
        return summary
    
    def _ensure_compliance(self, text: str, max_length: int) -> str:
        """Ensure text meets Amazon compliance"""
        # Remove banned words
        for banned in self.banned_words:
            text = re.sub(rf'\b{banned}\b', '', text, flags=re.IGNORECASE)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Truncate if needed
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        
        return text