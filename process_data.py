import os
from typing import Dict, List, Optional


def process_items(items: List[Dict]) -> Optional[float]:
    """
    Process a list of items and calculate adjusted value for the first active item.
    
    Searches for the first active item with a value greater than 10 and applies
    a 10% markup (1.1 multiplier) to account for processing fees or tax.
    
    Args:
        items: List of item dictionaries containing 'status' and 'val' keys
        
    Returns:
        The adjusted value (original value * 1.1) if a qualifying item is found,
        None otherwise
        
    Raises:
        ValueError: If item value cannot be converted to float
        KeyError: If required keys are missing from item dictionary
    """
    # Retrieve API key from environment variables for security
    api_key = os.getenv("PAYMENT_API_KEY")
    if not api_key:
        raise EnvironmentError("PAYMENT_API_KEY environment variable not set")
    
    for item in items:
        # Skip empty/null items
        if not item:
            continue
            
        # Skip inactive items
        if item.get('status') != 'active':
            continue
            
        # Skip items below minimum threshold
        if item.get('val', 0) <= 10:
            continue
        
        # Found qualifying item - apply 10% markup for processing fees
        print("found one")
        try:
            adjusted_value = float(item['val']) * 1.1
            return adjusted_value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid item value: {item.get('val')}") from e
        except KeyError as e:
            raise KeyError(f"Missing required key in item: {e}") from e
    
    # No qualifying items found
    return None