import json
import csv
import io
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd

# PDF generation imports
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.platypus import Image as RLImage
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

class ExportHandler:
    """
    Enhanced handler for exporting listings to various formats (JSON, CSV, PDF, Excel)
    """
    
    def __init__(self):
        # Amazon flat file column mappings (expanded)
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
            "other_image_url2",
            "other_image_url3",
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
            "other_attributes",
            # Additional metadata
            "generated_date",
            "model_version",
            "category",
            "optimization_score"
        ]
    
    def to_csv(self, listing: Dict[str, Any], include_metadata: bool = True) -> str:
        """
        Convert listing to comprehensive CSV format
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.csv_columns)
        writer.writeheader()
        
        row = self._map_to_csv_row(listing, include_metadata)
        writer.writerow(row)
        
        return output.getvalue()
    
    def to_csv_multiple(self, listings: List[Dict[str, Any]], include_metadata: bool = True) -> str:
        """
        Convert multiple listings to comprehensive CSV format
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.csv_columns)
        writer.writeheader()
        
        for listing in listings:
            row = self._map_to_csv_row(listing, include_metadata)
            writer.writerow(row)
        
        return output.getvalue()
    
    def to_detailed_csv(self, listings: List[Dict[str, Any]]) -> str:
        """
        Create detailed CSV with all fields dynamically captured
        """
        if not listings:
            return ""
        
        # Collect all possible fields from all listings
        all_fields = set()
        for listing in listings:
            all_fields.update(self._flatten_dict(listing).keys())
        
        # Sort fields for consistent ordering
        fieldnames = sorted(list(all_fields))
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for listing in listings:
            flattened = self._flatten_dict(listing)
            writer.writerow(flattened)
        
        return output.getvalue()
    
    def to_pdf(self, listing: Dict[str, Any], filename: Optional[str] = None) -> bytes:
        """
        Generate comprehensive PDF report for a single listing
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # Header with generation info
        elements.append(Paragraph("Product Listing Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Metadata table
        metadata = [
            ['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Category', listing.get('category', 'N/A')],
            ['Model', listing.get('model_version', 'N/A')]
        ]
        
        if 'optimization_score' in listing:
            metadata.append(['Optimization Score', f"{listing['optimization_score']}/100"])
        
        meta_table = Table(metadata, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Title section
        elements.append(Paragraph("Product Title", heading_style))
        elements.append(Paragraph(listing.get('title', 'No title provided'), body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Bullet points
        if 'bullets' in listing and listing['bullets']:
            elements.append(Paragraph("Key Features", heading_style))
            for i, bullet in enumerate(listing['bullets'], 1):
                bullet_text = f"<b>{i}.</b> {bullet}"
                elements.append(Paragraph(bullet_text, body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Description
        if 'description' in listing and listing['description']:
            elements.append(Paragraph("Product Description", heading_style))
            elements.append(Paragraph(listing['description'], body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Search terms
        if 'search_terms' in listing and listing['search_terms']:
            elements.append(Paragraph("Search Terms", heading_style))
            search_terms_text = ", ".join(listing['search_terms'])
            elements.append(Paragraph(search_terms_text, body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Attributes table
        if 'attributes' in listing and listing['attributes']:
            elements.append(Paragraph("Product Attributes", heading_style))
            attr_data = [['Attribute', 'Value']]
            for key, value in listing['attributes'].items():
                attr_data.append([key.replace('_', ' ').title(), str(value)])
            
            attr_table = Table(attr_data, colWidths=[2.5*inch, 3.5*inch])
            attr_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            elements.append(attr_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Compliance/Validation info
        if 'compliance' in listing or 'validation' in listing:
            elements.append(PageBreak())
            elements.append(Paragraph("Compliance & Validation", heading_style))
            
            validation = listing.get('validation', {})
            if validation:
                val_data = [['Check', 'Status', 'Details']]
                for check, result in validation.items():
                    status = '✓' if result.get('passed', True) else '✗'
                    details = result.get('message', 'OK')
                    val_data.append([check.replace('_', ' ').title(), status, details])
                
                val_table = Table(val_data, colWidths=[2*inch, 0.75*inch, 3.25*inch])
                val_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(val_table)
        
        # Additional data sections
        for key, value in listing.items():
            if key not in ['title', 'bullets', 'description', 'search_terms', 
                          'attributes', 'category', 'model_version', 
                          'optimization_score', 'compliance', 'validation']:
                if value and not isinstance(value, (dict, list)):
                    elements.append(Spacer(1, 0.1*inch))
                    elements.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", body_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def to_pdf_multiple(self, listings: List[Dict[str, Any]]) -> bytes:
        """
        Generate PDF report for multiple listings
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], 
                                    fontSize=24, alignment=TA_CENTER, spaceAfter=30)
        
        elements.append(Paragraph(f"Product Listings Report - {len(listings)} Items", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        for idx, listing in enumerate(listings, 1):
            if idx > 1:
                elements.append(PageBreak())
            
            elements.append(Paragraph(f"Listing {idx} of {len(listings)}", styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add each listing's content
            single_listing_pdf = self._add_listing_to_elements(listing, styles)
            elements.extend(single_listing_pdf)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def to_json(self, listing: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert listing to JSON format
        """
        if pretty:
            return json.dumps(listing, indent=2, ensure_ascii=False)
        return json.dumps(listing, ensure_ascii=False)
    
    def to_excel(self, listings: List[Dict[str, Any]]) -> bytes:
        """
        Convert listings to comprehensive Excel format with multiple sheets
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Main listings sheet
            main_rows = []
            for listing in listings:
                row = {
                    "Title": listing.get("title", ""),
                    "Category": listing.get("category", ""),
                    "Brand": listing.get("attributes", {}).get("brand", ""),
                    "Description": listing.get("description", "")[:500],  # Truncate for Excel
                    "Search Terms": ", ".join(listing.get("search_terms", [])),
                    "Generated Date": listing.get("generated_date", datetime.now().strftime('%Y-%m-%d'))
                }
                
                # Add bullets
                for i, bullet in enumerate(listing.get("bullets", [])[:5], 1):
                    row[f"Bullet {i}"] = bullet
                
                main_rows.append(row)
            
            df_main = pd.DataFrame(main_rows)
            df_main.to_excel(writer, sheet_name='Listings', index=False)
            
            # Attributes sheet
            attr_rows = []
            for idx, listing in enumerate(listings, 1):
                for key, value in listing.get("attributes", {}).items():
                    attr_rows.append({
                        "Listing #": idx,
                        "Title": listing.get("title", "")[:50],
                        "Attribute": key,
                        "Value": str(value)
                    })
            
            if attr_rows:
                df_attr = pd.DataFrame(attr_rows)
                df_attr.to_excel(writer, sheet_name='Attributes', index=False)
            
            # Metadata sheet
            meta_rows = []
            for idx, listing in enumerate(listings, 1):
                meta_rows.append({
                    "Listing #": idx,
                    "Title": listing.get("title", "")[:50],
                    "Category": listing.get("category", ""),
                    "Model Version": listing.get("model_version", ""),
                    "Optimization Score": listing.get("optimization_score", ""),
                    "Generated Date": listing.get("generated_date", "")
                })
            
            df_meta = pd.DataFrame(meta_rows)
            df_meta.to_excel(writer, sheet_name='Metadata', index=False)
        
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
        
        # Check for banned words
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
    
    def _map_to_csv_row(self, listing: Dict[str, Any], include_metadata: bool = True) -> Dict[str, str]:
        """
        Map listing data to comprehensive CSV row format
        """
        attributes = listing.get("attributes", {})
        bullets = listing.get("bullets", [])
        
        row = {
            "item_sku": listing.get("sku", f"SKU-{listing.get('category', 'ITEM')}-{datetime.now().strftime('%Y%m%d')}"),
            "product-id": listing.get("product_id", ""),
            "product-id-type": "ASIN",
            "item_name": listing.get("title", ""),
            "brand_name": attributes.get("brand", "Generic"),
            "manufacturer": attributes.get("manufacturer", attributes.get("brand", "Generic")),
            "product_description": listing.get("description", ""),
            "bullet_point1": bullets[0] if len(bullets) > 0 else "",
            "bullet_point2": bullets[1] if len(bullets) > 1 else "",
            "bullet_point3": bullets[2] if len(bullets) > 2 else "",
            "bullet_point4": bullets[3] if len(bullets) > 3 else "",
            "bullet_point5": bullets[4] if len(bullets) > 4 else "",
            "generic_keywords": ", ".join(listing.get("search_terms", [])),
            "main_image_url": listing.get("images", {}).get("main", ""),
            "other_image_url1": listing.get("images", {}).get("other_1", ""),
            "other_image_url2": listing.get("images", {}).get("other_2", ""),
            "other_image_url3": listing.get("images", {}).get("other_3", ""),
            "parent_child": listing.get("parent_child", "standalone"),
            "parent_sku": listing.get("parent_sku", ""),
            "relationship_type": listing.get("relationship_type", ""),
            "variation_theme": listing.get("variation_theme", ""),
            "size_name": attributes.get("size", ""),
            "color_name": attributes.get("color", ""),
            "material_type": attributes.get("material", ""),
            "product_tax_code": listing.get("tax_code", ""),
            "item_type": listing.get("category", ""),
            "target_audience": attributes.get("target_audience", ""),
            "subject_matter": attributes.get("subject_matter", ""),
            "other_attributes": json.dumps({k: v for k, v in attributes.items() 
                                          if k not in ['brand', 'size', 'color', 'material', 'target_audience']})
        }
        
        if include_metadata:
            row.update({
                "generated_date": listing.get("generated_date", datetime.now().strftime('%Y-%m-%d')),
                "model_version": listing.get("model_version", ""),
                "category": listing.get("category", ""),
                "optimization_score": listing.get("optimization_score", "")
            })
        
        return row
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, str]:
        """
        Flatten nested dictionary for CSV export
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to comma-separated strings
                items.append((new_key, ", ".join(str(x) for x in v)))
            else:
                items.append((new_key, str(v) if v is not None else ""))
        return dict(items)
    
    def _add_listing_to_elements(self, listing: Dict[str, Any], styles) -> List:
        """
        Helper to add a single listing's content to PDF elements
        """
        elements = []
        body_style = styles['BodyText']
        
        elements.append(Paragraph(f"<b>Title:</b> {listing.get('title', 'N/A')}", body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        if 'bullets' in listing:
            elements.append(Paragraph("<b>Features:</b>", body_style))
            for bullet in listing['bullets']:
                elements.append(Paragraph(f"• {bullet}", body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        if 'description' in listing:
            elements.append(Paragraph(f"<b>Description:</b> {listing['description']}", body_style))
        
        return elements