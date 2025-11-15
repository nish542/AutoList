import re
from typing import Dict, List, Any
from app.utils.lazy_loader import get_sentence_transformer, get_ner_pipeline, get_roberta_model_and_tokenizer


class TextExtractor:
    def __init__(self):
        # Lazy-loaded models
        self.ner_model = None
        self.attribute_tokenizer = None
        self.attribute_model = None
        self.sentence_model = None

        # Regex patterns for common attributes
        self.patterns = {
            'price': r'\$[\d,]+\.?\d*|\d+\s*(?:dollars?|usd|\$)',
            'size': r'\b\d+(?:\.\d+)?\s*(?:ml|l|oz|gb|mb|inch|cm|mm)\b',
            'color': r'\b(?:red|blue|green|black|white|gray|silver|gold|pink|purple|yellow|orange)\b',
            'material': r'\b(?:cotton|polyester|leather|steel|plastic|glass|wood|aluminum)\b',
            'brand': r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b',
            'model_number': r'\b[A-Z0-9]{3,}-?[A-Z0-9]+\b'
        }
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """
        Extract features from social media text
        """
        # Clean text
        cleaned_text = self._clean_text(text)
        
        # Named Entity Recognition
        entities = self._extract_entities(cleaned_text)
        
        # Pattern-based extraction
        pattern_features = self._extract_patterns(cleaned_text)
        
        # Semantic features (lazy load sentence model)
        if self.sentence_model is None:
            try:
                self.sentence_model = get_sentence_transformer()
            except Exception:
                self.sentence_model = None

        embeddings = None
        if self.sentence_model is not None:
            embeddings = self.sentence_model.encode([cleaned_text])[0]
        else:
            embeddings = []
        
        # Keywords extraction
        keywords = self._extract_keywords(cleaned_text)
        
        return {
            "cleaned_text": cleaned_text,
            "entities": entities,
            "pattern_features": pattern_features,
            "keywords": keywords,
            "embeddings": embeddings.tolist(),
            "raw_text": text
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean social media text
        """
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        # Remove hashtags but keep the word
        text = re.sub(r'#(\w+)', r'\1', text)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove emojis
        text = re.sub(r'[^\w\s\.\,\!\?\-\$]', ' ', text)
        # Multiple spaces to single
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities using BERT NER (lazy-loaded)
        """
        if self.ner_model is None:
            try:
                self.ner_model = get_ner_pipeline()
            except Exception:
                self.ner_model = None

        if self.ner_model is None:
            return []

        entities = self.ner_model(text)
        return [
            {
                "entity": ent.get("entity_group") or ent.get("entity"),
                "word": ent.get("word"),
                "score": ent.get("score", 0)
            }
            for ent in entities
        ]
    
    def _extract_patterns(self, text: str) -> Dict[str, List[str]]:
        """
        Extract attributes using regex patterns
        """
        features = {}
        for feature_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                features[feature_name] = matches
        return features
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords using TF-IDF approach
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        # Simple keyword extraction
        words = text.lower().split()
        # Filter stop words (simplified)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return list(set(keywords))[:10]


