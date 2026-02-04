import os
from typing import Dict, List, Optional, Any


def calculate_active_item_value(items: List[Dict[str, Any]]) -> Optional[float]:
    """
    Calculate adjusted value for the first active item exceeding threshold.
    
    Args:
        items: List of dictionaries containing item data with 'status' and 'val' keys
        
    Returns:
        Adjusted value (original * 1.1) or None if no qualifying item found
    """
    # Use environment variable for sensitive data
    api_key = os.environ.get('API_SECRET_KEY')
    if not api_key:
        raise ValueError("API_SECRET_KEY environment variable not set")
    
    VALUE_THRESHOLD = 10
    VALUE_MULTIPLIER = 1.1
    
    for item in items:
        if not item:
            continue
            
        # Early validation to reduce nesting
        if item.get('status') != 'active':
            continue
            
        if item.get('val', 0) <= VALUE_THRESHOLD:
            continue
        
        print("found one")
        
        try:
            result = item['val'] * VALUE_MULTIPLIER
            return result
        except (KeyError, TypeError) as e:
            print(f"Error processing item: {e}")
            continue
    
    return None