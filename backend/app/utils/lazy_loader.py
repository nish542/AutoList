import torch
from functools import lru_cache
from typing import Tuple, Any


def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    try:
        if torch.backends.mps.is_available():
            return torch.device("mps")
    except Exception:
        # Older torch builds may not expose mps backend
        pass
    return torch.device("cpu")


@lru_cache(maxsize=1)
def get_sentence_transformer(model_name: str = "all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)


@lru_cache(maxsize=1)
def get_blip_models(model_name: str = "Salesforce/blip-image-captioning-base") -> Tuple[Any, Any]:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    return processor, model


@lru_cache(maxsize=1)
def get_clip_models(model_name: str = "openai/clip-vit-base-patch32") -> Tuple[Any, Any]:
    from transformers import CLIPProcessor, CLIPModel
    processor = CLIPProcessor.from_pretrained(model_name)
    model = CLIPModel.from_pretrained(model_name)
    return processor, model


@lru_cache(maxsize=1)
def get_ner_pipeline(model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english"):
    from transformers import pipeline
    return pipeline("ner", model=model_name, aggregation_strategy="simple")


@lru_cache(maxsize=1)
def get_roberta_model_and_tokenizer(model_name: str = "roberta-base"):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model
