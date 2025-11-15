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
        # Method 1: Keyword matching
        keyword_scores = self._keyword_matching(text_features)
        
        # Method 2: Semantic similarity
        semantic_scores = self._semantic_matching(text_features)
        
        # Method 3: Object detection from images
        if image_features:
            image_scores = self._image_object_matching(image_features)
        else:
            image_scores = {}
        
        # Combine scores
        final_scores = {}
        for category_id in keyword_scores.keys():
            final_scores[category_id] = (
                keyword_scores.get(category_id, 0) * 0.3 +
                semantic_scores.get(category_id, 0) * 0.5 +
                image_scores.get(category_id, 0) * 0.2
            )
        
        # Return category with highest score
        if final_scores:
            return max(final_scores, key=final_scores.get)
        return "unknown"
    
    def _keyword_matching(self, text_features: Dict) -> Dict[str, float]:
        """
        Match keywords from text with category keywords
        """
        scores = {}
        text_keywords = set(text_features.get("keywords", []))
        
        for category in self.schemas["categories"]:
            category_keywords = set(category["keywords"])
            overlap = len(text_keywords & category_keywords)
            scores[category["category_id"]] = overlap / max(len(category_keywords), 1)
        
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
        Match detected objects with categories
        """
        scores = {}
        
        # Collect all detected objects
        all_objects = []
        for img_feat in image_features:
            all_objects.extend(img_feat.get("object_tags", []))
        
        for category in self.schemas["categories"]:
            category_keywords = category["keywords"]
            score = 0
            for obj in all_objects:
                if any(keyword in obj.lower() for keyword in category_keywords):
                    score += 1
            scores[category["category_id"]] = score / max(len(all_objects), 1)
        
        return scores


