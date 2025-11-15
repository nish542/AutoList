from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

# Request Models
class GenerateListingRequest(BaseModel):
    """
    Request model for generating a listing
    """
    text_content: str = Field(..., min_length=10, max_length=2000)
    detected_category: Optional[str] = None
    auto_fix_compliance: bool = True
    
    @validator('text_content')
    def validate_text_content(cls, v):
        if not v.strip():
            raise ValueError('Text content cannot be empty')
        return v

class ExportRequest(BaseModel):
    """
    Request model for exporting a listing
    """
    listing: Dict[str, Any]
    format: str = Field(default="json", regex="^(json|csv|excel)$")
    include_validation: bool = False

class ValidationRequest(BaseModel):
    """
    Request model for validating a listing
    """
    listing: Dict[str, Any]
    auto_fix: bool = False

# Response Models
class AttributeInfo(BaseModel):
    """
    Information about a product attribute
    """
    name: str
    value: Any
    type: str
    confidence: float = Field(ge=0.0, le=1.0)
    source: str  # "text", "image", "default"

class ListingResponse(BaseModel):
    """
    Response model for a generated listing
    """
    success: bool
    category: str
    title: str
    bullets: List[str]
    description: str
    search_terms: List[str]
    attributes: Dict[str, Any]
    extracted_features: Optional[Dict[str, Any]] = None
    confidence_scores: Optional[Dict[str, float]] = None
    processing_time_ms: Optional[int] = None

class ValidationResponse(BaseModel):
    """
    Response model for listing validation
    """
    is_valid: bool
    compliance_score: int = Field(ge=0, le=100)
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    fixed_listing: Optional[Dict[str, Any]] = None

class CategorySchema(BaseModel):
    """
    Schema for a product category
    """
    category_id: str
    category_name: str
    keywords: List[str]
    required_fields: Dict[str, Dict[str, Any]]
    optional_fields: Dict[str, Dict[str, Any]]
    listing_rules: Dict[str, Any]

class CategoriesResponse(BaseModel):
    """
    Response model for categories endpoint
    """
    categories: List[CategorySchema]
    total_categories: int

class ExportResponse(BaseModel):
    """
    Response model for export endpoint
    """
    success: bool
    format: str
    file_size_bytes: Optional[int] = None
    download_url: Optional[str] = None
    content: Optional[str] = None  # For JSON format

class ErrorResponse(BaseModel):
    """
    Standard error response
    """
    error: str
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthCheckResponse(BaseModel):
    """
    Health check response
    """
    status: str
    version: str
    models_loaded: bool
    available_categories: int

# Feature Models
class TextFeatures(BaseModel):
    """
    Extracted text features
    """
    cleaned_text: str
    entities: List[Dict[str, Any]]
    pattern_features: Dict[str, List[str]]
    keywords: List[str]
    embeddings: List[float]
    raw_text: str

class ImageFeatures(BaseModel):
    """
    Extracted image features
    """
    caption: str
    visual_features: List[float]
    dominant_colors: List[str]
    object_tags: List[str]
    image_size: tuple

class CombinedFeatures(BaseModel):
    """
    Combined multimodal features
    """
    category: str
    text_features: TextFeatures
    image_features: List[ImageFeatures]
    merged_attributes: Dict[str, Any]
    all_keywords: List[str]
    confidence_scores: Dict[str, float]

# Batch Processing Models
class BatchListingRequest(BaseModel):
    """
    Request for batch listing generation
    """
    posts: List[GenerateListingRequest]
    parallel_processing: bool = True
    max_workers: int = Field(default=4, ge=1, le=10)

class BatchListingResponse(BaseModel):
    """
    Response for batch listing generation
    """
    success: bool
    total_processed: int
    successful: int
    failed: int
    listings: List[ListingResponse]
    errors: List[Dict[str, str]]
    processing_time_seconds: float

# Analytics Models
class ListingAnalytics(BaseModel):
    """
    Analytics data for a listing
    """
    listing_id: str
    category: str
    compliance_score: int
    keyword_density: float
    readability_score: float
    completeness_score: float
    optimization_suggestions: List[str]

# Configuration Models
class ModelConfig(BaseModel):
    """
    Configuration for AI models
    """
    text_model: str = "bert-base-uncased"
    image_model: str = "Salesforce/blip-image-captioning-base"
    category_model: str = "all-MiniLM-L6-v2"
    use_gpu: bool = False
    batch_size: int = 8
    max_sequence_length: int = 512

class ProcessingConfig(BaseModel):
    """
    Configuration for processing pipeline
    """
    enable_ocr: bool = True
    enable_translation: bool = False
    target_language: str = "en"
    confidence_threshold: float = 0.7
    max_processing_time: int = 60  # seconds

# WebSocket Models (for real-time processing)
class WebSocketMessage(BaseModel):
    """
    WebSocket message format
    """
    type: str  # "progress", "result", "error"
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ProgressUpdate(BaseModel):
    """
    Progress update for long-running operations
    """
    stage: str
    percentage: int = Field(ge=0, le=100)
    message: str
    estimated_time_remaining: Optional[int] = None  # seconds


