"""Cache management for WHODIS."""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from .config import CACHE_DIR


class Cache:
    """Simple file-based cache system."""

    @staticmethod
    def get_cache_path(number: str, source: str) -> Path:
        """Get cache file path for a number and source."""
        # Hash the number for filename
        hash_name = hashlib.md5(number.encode()).hexdigest()
        return CACHE_DIR / f"{hash_name}_{source}.json"

    @staticmethod
    def get(number: str, source: str, max_age_days: int = 7) -> dict or None:
        """Get cached result for a number and source."""
        cache_path = Cache.get_cache_path(number, source)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if cache is still valid
            timestamp = datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
            if datetime.now() - timestamp > timedelta(days=max_age_days):
                return None
            
            return data.get("data")
        except (json.JSONDecodeError, IOError):
            return None

    @staticmethod
    def set(number: str, source: str, data: dict) -> None:
        """Cache result for a number and source."""
        cache_path = Cache.get_cache_path(number, source)
        
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "number": number,
            "source": source,
            "data": data
        }
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not write cache: {e}")

    @staticmethod
    def clear(number: str = None) -> None:
        """Clear cache for a specific number or all cache."""
        if number:
            hash_name = hashlib.md5(number.encode()).hexdigest()
            for cache_file in CACHE_DIR.glob(f"{hash_name}_*.json"):
                try:
                    cache_file.unlink()
                except IOError:
                    pass
        else:
            # Clear all cache
            for cache_file in CACHE_DIR.glob("*.json"):
                try:
                    cache_file.unlink()
                except IOError:
                    pass

    @staticmethod
    def get_all_for_number(number: str) -> dict:
        """Get all cached data for a number."""
        hash_name = hashlib.md5(number.encode()).hexdigest()
        results = {}
        
        for cache_file in CACHE_DIR.glob(f"{hash_name}_*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    source = data.get("source", "unknown")
                    results[source] = data.get("data")
            except (json.JSONDecodeError, IOError):
                continue
        
        return results
