import json
import csv
import io
from typing import Dict, Any, List
import pandas as pd

class ExportHandler:
    """
    Handles exporting listings to various formats (JSON, CSV, etc.)
    """
    
    def __init__(self):
        # Amazon flat file column mappings
        self.csv_columns = [
            "item_sku",
            "product-id",
            "product-id-type",
            "item_name",
            "brand_name",
            "manufacturer",
            "product_description",
            "bullet_point1",
            "bullet_point2",
            "bullet_point3",
            "bullet_point4",
            "bullet_point5",
            "generic_keywords",
            "main_image_url",
            "other_image_url1",
            "parent_child",
            "parent_sku",
            "relationship_type",
            "variation_theme",
            "size_name",
            "color_name",
            "material_type",
            "product_tax_code",
            "item_type",
            "target_audience",
            "subject_matter",
            "other_attributes"
        ]
    
    def to_csv(self, listing: Dict[str, Any]) -> str:
        """
        Convert listing to CSV format compatible with Amazon flat file
        """
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.csv_columns)
        writer.writeheader()
        
        # Map listing data to CSV row
        row = self._map_to_csv_row(listing)
        writer.writerow(row)
        
        return output.getvalue()
    
    def to_csv_multiple(self, listings: List[Dict[str, Any]]) -> str:
        """
        Convert multiple listings to CSV format
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.csv_columns)
        writer.writeheader()
        
        for listing in listings:
            row = self._map_to_csv_row(listing)
            writer.writerow(row)
        
        return output.getvalue()
    
    def to_json(self, listing: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert listing to JSON format
        """
        if pretty:
            return json.dumps(listing, indent=2, ensure_ascii=False)
        return json.dumps(listing, ensure_ascii=False)
    
    def to_amazon_json(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert to Amazon SP-API compatible JSON structure
        """
        amazon_json = {
            "productType": listing.get("category", "PRODUCT"),
            "requirements": "LISTING",
            "attributes": {
                "title": [
                    {
                        "value": listing.get("title", ""),
                        "language_tag": "en_US"
                    }
                ],
                "bullet_points": [
                    {
                        "value": bullets,
                        "language_tag": "en_US"
                    } for bullets in listing.get("bullets", [])
                ],
                "description": [
                    {
                        "value": listing.get("description", ""),
                        "language_tag": "en_US"
                    }
                ],
                "generic_keywords": [
                    {
                        "value": keywords,
                        "language_tag": "en_US"
                    } for keywords in listing.get("search_terms", [])
                ]
            }
        }
        
        # Add dynamic attributes
        if "attributes" in listing:
            for key, value in listing["attributes"].items():
                # Map common attributes to Amazon format
                amazon_key = self._map_attribute_key(key)
                if amazon_key:
                    amazon_json["attributes"][amazon_key] = [
                        {
                            "value": str(value),
                            "language_tag": "en_US"
                        }
                    ]
        
        return amazon_json
    
    def to_excel(self, listings: List[Dict[str, Any]]) -> bytes:
        """
        Convert listings to Excel format
        """
        # Flatten listings for DataFrame
        rows = []
        for listing in listings:
            row = {
                "Title": listing.get("title", ""),
                "Category": listing.get("category", ""),
                "Brand": listing.get("attributes", {}).get("brand", ""),
                "Description": listing.get("description", ""),
                "Search Terms": ", ".join(listing.get("search_terms", []))
            }
            
            # Add bullets
            for i, bullet in enumerate(listing.get("bullets", [])[:5], 1):
                row[f"Bullet {i}"] = bullet
            
            # Add key attributes
            for key, value in listing.get("attributes", {}).items():
                if key not in ["brand"]:
                    row[key.replace("_", " ").title()] = value
            
            rows.append(row)
        
        # Create DataFrame and convert to Excel
        df = pd.DataFrame(rows)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Listings', index=False)
        
        return output.getvalue()
    
    def validate_export(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate listing before export
        """
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ["title", "bullets", "description", "category"]
        for field in required_fields:
            if field not in listing or not listing[field]:
                errors.append(f"Missing required field: {field}")
        
        # Check field lengths
        if "title" in listing and len(listing["title"]) > 200:
            errors.append(f"Title exceeds 200 characters: {len(listing['title'])}")
        
        if "bullets" in listing:
            for i, bullet in enumerate(listing["bullets"]):
                if len(bullet) > 256:
                    errors.append(f"Bullet {i+1} exceeds 256 characters: {len(bullet)}")
        
        # Check for banned words (warnings)
        banned_words = ["best", "#1", "guaranteed", "free shipping"]
        text_to_check = listing.get("title", "") + " " + listing.get("description", "")
        for word in banned_words:
            if word.lower() in text_to_check.lower():
                warnings.append(f"Contains potentially banned word: {word}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _map_to_csv_row(self, listing: Dict[str, Any]) -> Dict[str, str]:
        """
        Map listing data to CSV row format
        """
        attributes = listing.get("attributes", {})
        bullets = listing.get("bullets", [])
        
        row = {
            "item_sku": f"SKU-{listing.get('category', 'ITEM')}-001",
            "product-id": "",
            "product-id-type": "ASIN",
            "item_name": listing.get("title", ""),
            "brand_name": attributes.get("brand", "Generic"),
            "manufacturer": attributes.get("brand", "Generic"),
            "product_description": listing.get("description", ""),
            "bullet_point1": bullets[0] if len(bullets) > 0 else "",
            "bullet_point2": bullets[1] if len(bullets) > 1 else "",
            "bullet_point3": bullets[2] if len(bullets) > 2 else "",
            "bullet_point4": bullets[3] if len(bullets) > 3 else "",
            "bullet_point5": bullets[4] if len(bullets) > 4 else "",
            "generic_keywords": ", ".join(listing.get("search_terms", [])),
            "main_image_url": "",
            "other_image_url1": "",
            "parent_child": "standalone",
            "parent_sku": "",
            "relationship_type": "",
            "variation_theme": "",
            "size_name": attributes.get("size", ""),
            "color_name": attributes.get("color", ""),
            "material_type": attributes.get("material", ""),
            "product_tax_code": "",
            "item_type": listing.get("category", ""),
            "target_audience": attributes.get("target_audience", ""),
            "subject_matter": "",
            "other_attributes": json.dumps(attributes)
        }
        
        return row
    
    def _map_attribute_key(self, key: str) -> str:
        """
        Map internal attribute keys to Amazon attribute names
        """
        mapping = {
            "brand": "brand_name",
            "color": "color_name",
            "size": "size_name",
            "material": "material_type",
            "weight_grams": "item_weight",
            "dimensions_cm": "item_dimensions",
            "capacity_ml": "capacity",
            "battery_life_hours": "battery_life"
        }
        
        return mapping.get(key, key)


