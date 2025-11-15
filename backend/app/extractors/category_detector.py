import json
from pathlib import Path
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np

class CategoryDetector:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load product schemas
        schema_path = Path(__file__).resolve().parent.parent / "schemas" / "product_schema.json"
        with open(schema_path, "r") as f:
            self.schemas = json.load(f)
        
        # Pre-compute category embeddings
        self.category_embeddings = self._compute_category_embeddings()
    
    def _compute_category_embeddings(self) -> Dict[str, np.ndarray]:
        """
        Pre-compute embeddings for each category
        """
        embeddings = {}
        for category in self.schemas["categories"]:
            # Combine category name and keywords
            text = f"{category['category_name']} {' '.join(category['keywords'])}"
            embedding = self.sentence_model.encode([text])[0]
            embeddings[category["category_id"]] = embedding
        return embeddings
    
    def detect_category(
        self, 
        text_features: Dict[str, Any],
        image_features: List[Dict[str, Any]]
    ) -> str:
        """
        Detect product category from features
        """
        # Method 1: Keyword matching with incidental mention detection
        keyword_scores = self._keyword_matching(text_features)
        
        # Method 2: Semantic similarity
        semantic_scores = self._semantic_matching(text_features)
        
        # Method 3: Object detection from images (improved weight)
        if image_features:
            image_scores = self._image_object_matching(image_features)
        else:
            image_scores = {}
        
        # Combine scores with improved weighting
        # Image objects now have higher priority to prevent misclassification
        final_scores = {}
        for category_id in keyword_scores.keys():
            # Increased image weight to prevent text/semantic from overriding clear visual detection
            final_scores[category_id] = (
                keyword_scores.get(category_id, 0) * 0.25 +
                semantic_scores.get(category_id, 0) * 0.35 +
                image_scores.get(category_id, 0) * 0.4
            )
        
        # Penalize categories where matches are incidental (mentioned but not the main product)
        raw_text = text_features.get("raw_text", "").lower()
        first_half = raw_text[:len(raw_text)//2]  # Check first half of text
        
        for category in self.schemas["categories"]:
            cat_id = category["category_id"]
            if cat_id in final_scores:
                primary_keywords = category["keywords"][:2]  # First 2 keywords are primary
                
                # If primary keywords only appear late in text (not in first half), reduce score
                found_in_first_half = any(kw in first_half for kw in primary_keywords)
                if not found_in_first_half and final_scores[cat_id] > 0.1:
                    final_scores[cat_id] *= 0.5  # Penalize late/incidental mentions
        
        # Return category with highest score
        if final_scores:
            best_category = max(final_scores, key=final_scores.get)
            best_score = final_scores[best_category]
            
            # If best score is too low (< 0.05), it means weak detection overall
            if best_score > 0.05:
                return best_category
        
        return "unknown"
    
    def _keyword_matching(self, text_features: Dict) -> Dict[str, float]:
        """
        Match keywords from text with category keywords
        Improved to prioritize primary product keywords and avoid false positives from incidental mentions
        """
        scores = {}
        text_keywords = set(text_features.get("keywords", []))
        
        for category in self.schemas["categories"]:
            category_keywords = set(category["keywords"])
            
            # Check for overlapping keywords
            overlap = text_keywords & category_keywords
            
            if overlap:
                # Calculate base overlap score
                overlap_count = len(overlap)
                base_score = overlap_count / max(len(category_keywords), 1)
                
                # Check for primary product keywords (first 2-3 are usually most important)
                primary_keywords = set(list(category_keywords)[:3])
                primary_match_count = len(text_keywords & primary_keywords)
                
                # Boost score if primary keywords match
                if primary_match_count > 0:
                    base_score *= (1.0 + primary_match_count * 0.3)
                
                scores[category["category_id"]] = base_score
            else:
                scores[category["category_id"]] = 0.0
        
        return scores
    
    def _semantic_matching(self, text_features: Dict) -> Dict[str, float]:
        """
        Use semantic similarity for category detection
        """
        scores = {}
        
        if "embeddings" in text_features:
            text_embedding = np.array(text_features["embeddings"])
            
            for category_id, category_embedding in self.category_embeddings.items():
                # Cosine similarity
                similarity = np.dot(text_embedding, category_embedding) / (
                    np.linalg.norm(text_embedding) * np.linalg.norm(category_embedding)
                )
                scores[category_id] = float(similarity)
        
        return scores
    
    def _image_object_matching(self, image_features: List[Dict]) -> Dict[str, float]:
        """
        Match detected objects with categories - improved exact matching
        """
        scores = {}
        
        # Collect all detected objects with their confidences
        object_data = []
        for img_feat in image_features:
            primary_objects = img_feat.get("primary_objects", [])
            confidences = img_feat.get("object_confidences", {})
            
            for obj in primary_objects:
                confidence = confidences.get(obj, 0.5)
                object_data.append((obj, confidence))
        
        # Score each category based on exact keyword matches
        for category in self.schemas["categories"]:
            category_keywords = category["keywords"]
            category_score = 0
            matched_objects = []
            
            for obj, confidence in object_data:
                obj_lower = obj.lower()
                
                # Exact keyword matching (more precise)
                for keyword in category_keywords:
                    keyword_lower = keyword.lower()
                    
                    # Exact match or as a complete word
                    if obj_lower == keyword_lower or obj_lower in keyword_lower or keyword_lower in obj_lower:
                        # Boost score for high-confidence detections
                        match_score = confidence
                        category_score += match_score
                        matched_objects.append(obj)
                        break  # Don't double-count
            
            # Normalize by category keywords count (prevents categories with many keywords from winning)
            if matched_objects:
                scores[category["category_id"]] = category_score / len(category_keywords)
            else:
                scores[category["category_id"]] = 0.0
        
        return scores


