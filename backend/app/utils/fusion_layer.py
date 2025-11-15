from typing import Dict, List, Any
import numpy as np

class MultimodalFusion:
    """
    Fuses features from text and image extractors to create a unified feature set
    """
    
    def __init__(self):
        self.feature_weights = {
            "text": 0.6,
            "image": 0.4
        }
    
    def fuse_features(
        self, 
        text_features: Dict[str, Any], 
        image_features: List[Dict[str, Any]],
        category: str
    ) -> Dict[str, Any]:
        """
        Combine text and image features intelligently
        """
        combined_features = {
            "category": category,
            "text_features": text_features,
            "image_features": image_features,
            "merged_attributes": {}
        }
        
        # Extract text-based attributes
        text_attributes = self._extract_text_attributes(text_features)
        
        # Extract image-based attributes
        image_attributes = self._extract_image_attributes(image_features)
        
        # Merge attributes with priority
        merged = self._merge_attributes(text_attributes, image_attributes)
        combined_features["merged_attributes"] = merged
        
        # Extract keywords for search terms
        combined_features["all_keywords"] = self._combine_keywords(
            text_features, image_features
        )
        
        # Confidence scores
        combined_features["confidence_scores"] = self._calculate_confidence(
            text_features, image_features
        )
        
        return combined_features
    
    def _extract_text_attributes(self, text_features: Dict) -> Dict[str, Any]:
        """
        Extract structured attributes from text features
        """
        attributes = {}
        
        # From pattern features
        if "pattern_features" in text_features:
            for key, values in text_features["pattern_features"].items():
                if values:
                    attributes[key] = values[0]
        
        # From entities
        if "entities" in text_features:
            for entity in text_features["entities"]:
                if entity["entity"] == "ORG" and entity["score"] > 0.8:
                    if "brand" not in attributes:
                        attributes["brand"] = entity["word"]
                elif entity["entity"] == "LOC":
                    if "origin" not in attributes:
                        attributes["origin"] = entity["word"]
        
        # From keywords
        if "keywords" in text_features:
            attributes["text_keywords"] = text_features["keywords"]
        
        return attributes
    
    def _extract_image_attributes(self, image_features: List[Dict]) -> Dict[str, Any]:
        """
        Extract structured attributes from image features
        """
        attributes = {}
        
        if not image_features:
            return attributes
        
        # Aggregate from all images
        all_colors = []
        all_objects = []
        all_captions = []
        
        for img_feat in image_features:
            if "dominant_colors" in img_feat:
                all_colors.extend(img_feat["dominant_colors"])
            if "object_tags" in img_feat:
                all_objects.extend(img_feat["object_tags"])
            if "caption" in img_feat:
                all_captions.append(img_feat["caption"])
        
        # Most common color
        if all_colors:
            from collections import Counter
            color_counts = Counter(all_colors)
            attributes["color"] = color_counts.most_common(1)[0][0]
        
        # Primary objects
        if all_objects:
            attributes["detected_objects"] = list(set(all_objects))
        
        # Combined caption insights
        if all_captions:
            attributes["image_descriptions"] = all_captions
        
        return attributes
    
    def _merge_attributes(
        self, 
        text_attrs: Dict[str, Any], 
        image_attrs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge attributes with intelligent priority
        """
        merged = {}
        
        # Start with text attributes (usually more specific)
        merged.update(text_attrs)
        
        # Add image attributes if not already present
        for key, value in image_attrs.items():
            if key not in merged:
                merged[key] = value
            elif key == "color" and "color" not in text_attrs:
                # Image color detection is reliable
                merged[key] = value
        
        # Special handling for certain attributes
        if "detected_objects" in image_attrs and "text_keywords" in text_attrs:
            # Combine both for richer context
            all_context = list(set(
                image_attrs.get("detected_objects", []) + 
                text_attrs.get("text_keywords", [])
            ))
            merged["context_keywords"] = all_context[:15]
        
        return merged
    
    def _combine_keywords(
        self, 
        text_features: Dict, 
        image_features: List[Dict]
    ) -> List[str]:
        """
        Combine keywords from all sources
        """
        keywords = set()
        
        # From text
        if "keywords" in text_features:
            keywords.update(text_features["keywords"])
        
        # From images
        for img_feat in image_features:
            if "object_tags" in img_feat:
                keywords.update(img_feat["object_tags"])
            if "caption" in img_feat:
                # Extract keywords from caption
                caption_words = img_feat["caption"].lower().split()
                important_words = [
                    w for w in caption_words 
                    if len(w) > 3 and w not in ['with', 'this', 'that', 'from']
                ]
                keywords.update(important_words[:5])
        
        return list(keywords)[:20]
    
    def _calculate_confidence(
        self, 
        text_features: Dict, 
        image_features: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate confidence scores for different aspects
        """
        confidence = {}
        
        # Text confidence based on entity scores
        if "entities" in text_features and text_features["entities"]:
            avg_entity_score = np.mean([e["score"] for e in text_features["entities"]])
            confidence["text_extraction"] = float(avg_entity_score)
        else:
            confidence["text_extraction"] = 0.5
        
        # Image confidence based on presence of features
        if image_features:
            img_score = 0
            for img_feat in image_features:
                if "caption" in img_feat:
                    img_score += 0.3
                if "dominant_colors" in img_feat:
                    img_score += 0.3
                if "object_tags" in img_feat:
                    img_score += 0.4
            confidence["image_extraction"] = min(img_score / len(image_features), 1.0)
        else:
            confidence["image_extraction"] = 0.0
        
        # Overall confidence
        confidence["overall"] = (
            confidence["text_extraction"] * self.feature_weights["text"] +
            confidence["image_extraction"] * self.feature_weights["image"]
        )
        
        return confidence


