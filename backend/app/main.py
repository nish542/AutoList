from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Union
import json
from pathlib import Path
from pydantic import BaseModel
import io
import numpy as np
import traceback

from app.extractors.text_extractor import TextExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.category_detector import CategoryDetector
from app.generators.listing_generator import ListingGenerator
from app.utils.fusion_layer import MultimodalFusion
from app.utils.export_handler import ExportHandler

app = FastAPI(title="Amazon Listing Generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allow localhost for development and all origins for production
    # You can restrict this to specific frontend URLs if needed
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
text_extractor = TextExtractor()
image_extractor = ImageExtractor()
category_detector = CategoryDetector()
listing_generator = ListingGenerator()
fusion_layer = MultimodalFusion()
export_handler = ExportHandler()

class GenerateListingRequest(BaseModel):
    text_content: str
    detected_category: Optional[str] = None

@app.post("/generate")
async def generate_listing(
    request: Request,
    text_content: Optional[str] = Form(None),
    detected_category: Optional[str] = Form(None),
    images: Optional[Union[UploadFile, List[UploadFile]]] = File(None)
):
    """
    Main endpoint to generate product listing from social media post
    """
    try:
        # If the client sent JSON instead of multipart/form-data, accept that too
        if request.headers.get("content-type", "").startswith("application/json"):
            body = await request.json()
            text_content = body.get("text_content") or body.get("text")
            detected_category = body.get("detected_category") or body.get("category")
            imgs = body.get("images", [])
            # JSON image payloads should be base64 or urls — we currently don't support that in batch
            images_list = []
            # leave images_list empty; image extraction only runs for binary uploads
        else:
            images_list = images if isinstance(images, list) else ([images] if images else [])

        # Step 1: Extract text features
        if not text_content:
            raise HTTPException(status_code=422, detail="Missing 'text_content' field")
        text_features = text_extractor.extract_features(text_content)
        
        # Step 2: Extract image features if provided (only supports binary uploads)
        image_features = []
        for upload in images_list:
            img_bytes = await upload.read()
            img_features = image_extractor.extract_features(img_bytes)
            image_features.append(img_features)
        
        # Step 3: Detect product category
        if detected_category:
            category = detected_category
        else:
            category = category_detector.detect_category(
                text_features, 
                image_features
            )
        
        # Step 4: Fuse multimodal features
        combined_features = fusion_layer.fuse_features(
            text_features, 
            image_features, 
            category
        )
        
        # Step 5: Generate listing
        listing = listing_generator.generate(combined_features, category)
        
        response_content = {
            "success": True,
            "category": category,
            "listing": listing,
            "extracted_features": combined_features
        }

        # Sanitize numpy types (ndarray, numpy scalars) recursively so JSON encoding won't fail
        def sanitize(obj):
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [sanitize(v) for v in obj]
            if isinstance(obj, tuple):
                return tuple(sanitize(v) for v in obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.floating, np.floating.__class__)):
                try:
                    return float(obj)
                except Exception:
                    return obj.item() if hasattr(obj, 'item') else obj
            # numpy scalar
            if isinstance(obj, np.generic):
                return obj.item()
            return obj

        sanitized = sanitize(response_content)
        return JSONResponse(content=jsonable_encoder(sanitized))

    except Exception as e:
        # Return JSON error payload to avoid serialization issues in exception handlers
            # If this is an HTTPException (like validation 422), re-raise it
            if isinstance(e, HTTPException):
                raise

            tb = traceback.format_exc()
            err_content = {"success": False, "error": str(e), "traceback": tb}
            # Also print to stderr for server logs
            print(tb)
            return JSONResponse(status_code=500, content=jsonable_encoder(err_content))

@app.get("/categories")
async def get_categories():
    """
    Return all available product categories and their schemas
    """
    schema_path = Path(__file__).resolve().parent / "schemas" / "product_schema.json"
    with open(schema_path, "r") as f:
        schemas = json.load(f)
    return schemas


@app.get("/")
async def root():
    """Redirect root to the interactive docs."""
    return RedirectResponse(url="/docs")

@app.post("/export")
async def export_listing(payload: dict):
    """
    Export the generated listing in specified format.
    Accepts a JSON body { "listing": {...}, "format": "json" | "csv" }
    """
    # Support both direct listing in body or nested payload
    listing = payload.get('listing', payload)
    format = payload.get('format', 'json')
    if format == "csv":
        csv_content = export_handler.to_csv(listing)
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=listing.csv"
            }
        )
    else:
        return listing

@app.post("/validate")
async def validate_listing(payload: dict):
    """
    Validate listing against Amazon compliance rules.
    Accepts a JSON body { "listing": {...}, "auto_fix": true/false }
    """
    from app.generators.compliance_validator import ComplianceValidator
    validator = ComplianceValidator()
    # Support nested payload as well as raw listing
    listing = payload.get('listing', payload)
    auto_fix = payload.get('auto_fix', False)

    if auto_fix:
        return validator.auto_fix(listing)

    validation_result = validator.validate(listing)
    return validation_result

