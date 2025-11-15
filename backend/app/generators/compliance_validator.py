import re
from typing import Dict, List, Any

class ComplianceValidator:
    """
    Validates listings against Amazon's compliance rules and style guidelines
    """
    
    def __init__(self):
        # Amazon's banned/restricted words and phrases
        self.banned_words = [
            "best", "#1", "number one", "top rated", "award winning",
            "guaranteed", "warranty", "free shipping", "free delivery",
            "cheap", "cheapest", "bargain", "discount", "sale",
            "amazon's choice", "amazon", "prime", 
            "covid", "coronavirus", "pandemic",
            "cure", "treatment", "heal"
        ]
        
        # Promotional language to avoid
        self.promotional_phrases = [
            "limited time", "act now", "don't miss", "hurry",
            "exclusive", "special offer", "deal of the day",
            "money back", "risk free", "no risk"
        ]
        
        # Required title format rules
        self.title_rules = {
            "max_length": 200,
            "min_length": 20,
            "no_all_caps": True,
            "no_special_chars": ["!", "@", "#", "$", "%", "*", "~"],
            "proper_capitalization": True
        }
        
        # Bullet point rules
        self.bullet_rules = {
            "max_length": 256,
            "min_length": 10,
            "max_bullets": 5,
            "min_bullets": 3,
            "start_capital": True,
            "no_end_punctuation": True
        }
        
        # Description rules
        self.description_rules = {
            "max_length": 2000,
            "min_length": 50,
            "no_html": True,
            "no_links": True
        }
        
        # Search terms rules
        self.search_terms_rules = {
            "max_bytes": 249,
            "max_terms": 50,
            "no_duplicates": True,
            "no_brand_names": True,
            "no_banned_words": True
        }
    
    def validate(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation of the entire listing
        """
        results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": [],
            "compliance_score": 100
        }
        
        # Validate each component
        self._validate_title(listing.get("title", ""), results)
        self._validate_bullets(listing.get("bullets", []), results)
        self._validate_description(listing.get("description", ""), results)
        self._validate_search_terms(listing.get("search_terms", []), results)
        self._validate_attributes(listing.get("attributes", {}), results)
        
        # Check for banned content across all fields
        self._check_banned_content(listing, results)
        
        # Calculate compliance score
        results["compliance_score"] = self._calculate_compliance_score(results)
        results["is_valid"] = len(results["errors"]) == 0
        
        return results
    
    def auto_fix(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically fix common compliance issues
        """
        fixed_listing = listing.copy()
        
        # Fix title
        if "title" in fixed_listing:
            fixed_listing["title"] = self._fix_title(fixed_listing["title"])
        
        # Fix bullets
        if "bullets" in fixed_listing:
            fixed_listing["bullets"] = [
                self._fix_bullet(bullet) for bullet in fixed_listing["bullets"]
            ]
        
        # Fix description
        if "description" in fixed_listing:
            fixed_listing["description"] = self._fix_description(
                fixed_listing["description"]
            )
        
        # Fix search terms
        if "search_terms" in fixed_listing:
            fixed_listing["search_terms"] = self._fix_search_terms(
                fixed_listing["search_terms"]
            )
        
        return fixed_listing
    
    def _validate_title(self, title: str, results: Dict):
        """
        Validate title against Amazon rules
        """
        if not title:
            results["errors"].append("Title is missing")
            return
        
        # Length checks
        if len(title) > self.title_rules["max_length"]:
            results["errors"].append(
                f"Title exceeds {self.title_rules['max_length']} characters"
            )
        elif len(title) < self.title_rules["min_length"]:
            results["warnings"].append(
                f"Title is shorter than recommended {self.title_rules['min_length']} characters"
            )
        
        # Check for all caps
        if title.isupper():
            results["errors"].append("Title should not be in all capital letters")
        
        # Check for special characters
        for char in self.title_rules["no_special_chars"]:
            if char in title:
                results["errors"].append(f"Title contains prohibited character: {char}")
        
        # Check proper capitalization
        if not self._is_properly_capitalized(title):
            results["warnings"].append("Title should use proper title case capitalization")
    
    def _validate_bullets(self, bullets: List[str], results: Dict):
        """
        Validate bullet points
        """
        if not bullets:
            results["errors"].append("Bullet points are missing")
            return
        
        # Number of bullets
        if len(bullets) < self.bullet_rules["min_bullets"]:
            results["errors"].append(
                f"Minimum {self.bullet_rules['min_bullets']} bullet points required"
            )
        elif len(bullets) > self.bullet_rules["max_bullets"]:
            results["warnings"].append(
                f"Maximum {self.bullet_rules['max_bullets']} bullet points recommended"
            )
        
        # Validate each bullet
        for i, bullet in enumerate(bullets, 1):
            # Length check
            if len(bullet) > self.bullet_rules["max_length"]:
                results["errors"].append(
                    f"Bullet {i} exceeds {self.bullet_rules['max_length']} characters"
                )
            elif len(bullet) < self.bullet_rules["min_length"]:
                results["warnings"].append(
                    f"Bullet {i} is too short (min {self.bullet_rules['min_length']} chars)"
                )
            
            # Capitalization check
            if bullet and not bullet[0].isupper():
                results["warnings"].append(f"Bullet {i} should start with a capital letter")
            
            # End punctuation check
            if bullet and bullet[-1] in '.!?':
                results["warnings"].append(f"Bullet {i} should not end with punctuation")
    
    def _validate_description(self, description: str, results: Dict):
        """
        Validate product description
        """
        if not description:
            results["warnings"].append("Description is missing")
            return
        
        # Length checks
        if len(description) > self.description_rules["max_length"]:
            results["errors"].append(
                f"Description exceeds {self.description_rules['max_length']} characters"
            )
        elif len(description) < self.description_rules["min_length"]:
            results["warnings"].append(
                f"Description is shorter than recommended {self.description_rules['min_length']} characters"
            )
        
        # Check for HTML
        if re.search(r'<[^>]+>', description):
            results["errors"].append("Description contains HTML tags")
        
        # Check for URLs
        if re.search(r'https?://\S+', description):
            results["errors"].append("Description contains URLs")
    
    def _validate_search_terms(self, search_terms: List[str], results: Dict):
        """
        Validate search terms
        """
        if not search_terms:
            results["warnings"].append("Search terms are missing")
            return
        
        # Byte size check
        terms_string = " ".join(search_terms)
        byte_size = len(terms_string.encode('utf-8'))
        if byte_size > self.search_terms_rules["max_bytes"]:
            results["errors"].append(
                f"Search terms exceed {self.search_terms_rules['max_bytes']} bytes"
            )
        
        # Check for duplicates
        if len(search_terms) != len(set(search_terms)):
            results["warnings"].append("Search terms contain duplicates")
        
        # Too many terms
        if len(search_terms) > self.search_terms_rules["max_terms"]:
            results["warnings"].append(
                f"Too many search terms (max {self.search_terms_rules['max_terms']})"
            )
    
    def _validate_attributes(self, attributes: Dict[str, Any], results: Dict):
        """
        Validate product attributes
        """
        if not attributes:
            results["warnings"].append("Product attributes are missing")
            return
        
        # Check for required attributes
        required = ["brand", "color", "material"]
        for req in required:
            if req not in attributes or not attributes[req]:
                results["suggestions"].append(f"Consider adding '{req}' attribute")
    
    def _check_banned_content(self, listing: Dict[str, Any], results: Dict):
        """
        Check for banned words and phrases across all content
        """
        # Combine all text content
        all_text = " ".join([
            listing.get("title", ""),
            listing.get("description", ""),
            " ".join(listing.get("bullets", [])),
            " ".join(listing.get("search_terms", []))
        ]).lower()
        
        # Check banned words
        found_banned = []
        for word in self.banned_words:
            if word in all_text:
                found_banned.append(word)
        
        if found_banned:
            results["errors"].append(
                f"Contains banned words/phrases: {', '.join(found_banned)}"
            )
        
        # Check promotional phrases
        found_promotional = []
        for phrase in self.promotional_phrases:
            if phrase in all_text:
                found_promotional.append(phrase)
        
        if found_promotional:
            results["warnings"].append(
                f"Contains promotional language: {', '.join(found_promotional)}"
            )
    
    def _calculate_compliance_score(self, results: Dict) -> int:
        """
        Calculate overall compliance score
        """
        score = 100
        
        # Deduct for errors (10 points each)
        score -= len(results["errors"]) * 10
        
        # Deduct for warnings (3 points each)
        score -= len(results["warnings"]) * 3
        
        # Ensure score doesn't go below 0
        return max(0, score)
    
    def _is_properly_capitalized(self, text: str) -> bool:
        """
        Check if text uses proper title case
        """
        # Simple check: first letter of major words should be capitalized
        words = text.split()
        minor_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        
        for i, word in enumerate(words):
            if i == 0 or word.lower() not in minor_words:
                if not word[0].isupper():
                    return False
        return True
    
    def _fix_title(self, title: str) -> str:
        """
        Auto-fix common title issues
        """
        # Remove banned words
        for word in self.banned_words:
            title = re.sub(rf'\b{word}\b', '', title, flags=re.IGNORECASE)
        
        # Fix capitalization
        title = self._apply_title_case(title)
        
        # Remove special characters
        for char in self.title_rules["no_special_chars"]:
            title = title.replace(char, '')
        
        # Truncate if too long
        if len(title) > self.title_rules["max_length"]:
            title = title[:self.title_rules["max_length"]-3] + "..."
        
        # Clean up extra spaces
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _fix_bullet(self, bullet: str) -> str:
        """
        Auto-fix bullet point issues
        """
        # Remove banned words
        for word in self.banned_words:
            bullet = re.sub(rf'\b{word}\b', '', bullet, flags=re.IGNORECASE)
        
        # Ensure starts with capital
        if bullet:
            bullet = bullet[0].upper() + bullet[1:]
        
        # Remove end punctuation
        bullet = bullet.rstrip('.!?,;:')
        
        # Truncate if too long
        if len(bullet) > self.bullet_rules["max_length"]:
            bullet = bullet[:self.bullet_rules["max_length"]-3] + "..."
        
        # Clean up extra spaces
        bullet = re.sub(r'\s+', ' ', bullet).strip()
        
        return bullet
    
    def _fix_description(self, description: str) -> str:
        """
        Auto-fix description issues
        """
        # Remove HTML tags
        description = re.sub(r'<[^>]+>', '', description)
        
        # Remove URLs
        description = re.sub(r'https?://\S+', '', description)
        
        # Remove banned words
        for word in self.banned_words:
            description = re.sub(rf'\b{word}\b', '', description, flags=re.IGNORECASE)
        
        # Truncate if too long
        if len(description) > self.description_rules["max_length"]:
            description = description[:self.description_rules["max_length"]-3] + "..."
        
        # Clean up extra spaces
        description = re.sub(r'\s+', ' ', description).strip()
        
        return description
    
    def _fix_search_terms(self, search_terms: List[str]) -> List[str]:
        """
        Auto-fix search terms issues
        """
        # Remove duplicates
        search_terms = list(dict.fromkeys(search_terms))
        
        # Remove banned words
        cleaned_terms = []
        for term in search_terms:
            is_clean = True
            for banned in self.banned_words:
                if banned in term.lower():
                    is_clean = False
                    break
            if is_clean:
                cleaned_terms.append(term.lower())
        
        # Ensure byte limit
        while len(" ".join(cleaned_terms).encode('utf-8')) > self.search_terms_rules["max_bytes"]:
            cleaned_terms.pop()
        
        return cleaned_terms[:self.search_terms_rules["max_terms"]]
    
    def _apply_title_case(self, text: str) -> str:
        """
        Apply proper title case to text
        """
        minor_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        words = text.split()
        
        result = []
        for i, word in enumerate(words):
            if i == 0 or word.lower() not in minor_words:
                result.append(word.capitalize())
            else:
                result.append(word.lower())
        
        return " ".join(result)


