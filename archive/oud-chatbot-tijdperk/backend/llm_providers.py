"""
LLM Providers - Support voor verschillende AI providers
Ondersteunt OpenAI, Google Gemini, Anthropic Claude, etc.
"""

import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def create_openai_model(api_key: str, model: str = "gpt-4o", temperature: float = 0.7):
    """Create OpenAI ChatModel"""
    try:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=temperature
        )
    except ImportError:
        logger.error("langchain-openai not installed. Run: pip install langchain-openai")
        raise

def create_gemini_model(api_key: str, model: str = "gemini-2.5-pro", temperature: float = 0.7):
    """Create Google Gemini Model"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=temperature,
            convert_system_message_to_human=True  # Gemini specific setting
        )
    except ImportError:
        logger.error("langchain-google-genai not installed. Run: pip install langchain-google-genai")
        raise

def create_anthropic_model(api_key: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.7):
    """Create Anthropic Claude Model"""
    try:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            anthropic_api_key=api_key,
            model=model,
            temperature=temperature
        )
    except ImportError:
        logger.error("langchain-anthropic not installed. Run: pip install langchain-anthropic")
        raise

def create_chat_model(provider: str, api_key: str, model: str = None, temperature: float = 0.7):
    """
    Universal chat model creator
    
    Args:
        provider: 'openai', 'gemini', 'anthropic'
        api_key: API key for the provider
        model: Model name (uses defaults if not specified)
        temperature: Creativity/randomness (0.0 - 1.0)
    """
    
    provider = provider.lower()
    
    if provider == "openai":
        model = model or "gpt-4o"
        return create_openai_model(api_key, model, temperature)
    
    elif provider == "gemini":
        model = model or "gemini-2.5-pro"
        return create_gemini_model(api_key, model, temperature)
    
    elif provider == "anthropic":
        model = model or "claude-3-5-sonnet-20241022"
        return create_anthropic_model(api_key, model, temperature)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Choose from: openai, gemini, anthropic")

def get_available_models(provider: str, api_key: str) -> list:
    """Get available models for a provider"""
    
    if provider.lower() == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            models = client.models.list()
            return [model.id for model in models.data if model.id.startswith("gpt")]
        except Exception as e:
            logger.error(f"Error fetching OpenAI models: {e}")
            return ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    
    elif provider.lower() == "gemini":
        # Gemini models - based on API response
        return [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro-002", 
            "gemini-1.5-flash-002",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro"
        ]
    
    elif provider.lower() == "anthropic":
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022", 
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
    
    else:
        return []

def validate_api_key(provider: str, api_key: str) -> bool:
    """Validate API key for a provider"""
    if not api_key or len(api_key.strip()) < 10:
        return False
        
    try:
        # Quick test call
        model = create_chat_model(provider, api_key)
        # Simple test prompt
        test_response = model.invoke("Test")
        return True
    except Exception as e:
        logger.error(f"API key validation failed for {provider}: {e}")
        return False

# Provider configurations
PROVIDER_CONFIGS = {
    "openai": {
        "name": "OpenAI",
        "default_model": "gpt-4o",
        "api_key_env": "OPENAI_API_KEY",
        "description": "GPT-4o, GPT-4, ChatGPT models"
    },
    "gemini": {
        "name": "Google Gemini",
        "default_model": "gemini-2.5-pro", 
        "api_key_env": "GOOGLE_API_KEY",
        "description": "Google's latest Gemini 2.5 Pro model with advanced reasoning capabilities"
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "default_model": "claude-3-5-sonnet-20241022",
        "api_key_env": "ANTHROPIC_API_KEY", 
        "description": "Claude 3.5 Sonnet and other Claude models"
    }
}

def get_provider_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a provider"""
    return PROVIDER_CONFIGS.get(provider.lower(), {})