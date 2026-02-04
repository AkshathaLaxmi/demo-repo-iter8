import os
from typing import Dict, List, Optional, Any


# Configuration constants
MINIMUM_VALUE_THRESHOLD = 10
MARKUP_MULTIPLIER = 1.1


class SecretKeyNotFoundError(Exception):
    """Raised when the required secret key is not found in environment variables."""
    pass


class InvalidItemDataError(Exception):
    """Raised when item data is invalid or missing required fields."""
    pass


def get_secret_key() -> str:
    """
    Retrieve the secret key from environment variables.
    
    Returns:
        str: The secret key for API authentication.
        
    Raises:
        SecretKeyNotFoundError: If STRIPE_SECRET_KEY is not set in environment.
    """
    secret_key = os.getenv("STRIPE_SECRET_KEY")
    if not secret_key:
        raise SecretKeyNotFoundError(
            "STRIPE_SECRET_KEY environment variable must be set"
        )
    return secret_key


def is_item_valid(item: Optional[Dict[str, Any]]) -> bool:
    """
    Validate that an item has the required structure.
    
    Args:
        item: Dictionary containing item data to validate.
        
    Returns:
        bool: True if item is valid, False otherwise.
    """
    if not item:
        return False
    
    return (
        isinstance(item, dict) and
        "status" in item and
        "val" in item
    )


def is_item_active(item: Dict[str, Any]) -> bool:
    """
    Check if an item has active status.
    
    Args:
        item: Dictionary containing item data with 'status' field.
        
    Returns:
        bool: True if item status is 'active', False otherwise.
    """
    return item.get("status") == "active"


def calculate_markup_value(base_value: float) -> float:
    """
    Calculate the marked-up value by applying the configured multiplier.
    
    Args:
        base_value: The original value to mark up.
        
    Returns:
        float: The calculated value after applying markup.
        
    Raises:
        ValueError: If base_value is not a valid number.
    """
    try:
        return float(base_value) * MARKUP_MULTIPLIER
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid base_value for markup calculation: {base_value}") from e


def calculate_active_item_value(items: List[Dict[str, Any]]) -> Optional[float]:
    """
    Find the first active item above threshold and return its marked-up value.
    
    This function processes a list of items, searching for the first item that:
    1. Has valid structure (contains 'status' and 'val' fields)
    2. Has status equal to 'active'
    3. Has a value greater than the minimum threshold
    
    When found, it applies a markup multiplier and returns the result.
    
    Args:
        items: List of dictionaries containing item data with 'status' and 'val' keys.
        
    Returns:
        Optional[float]: The marked-up value of the first qualifying item,
                        or None if no qualifying items are found.
                        
    Raises:
        InvalidItemDataError: If item data cannot be processed.
        
    Example:
        >>> items = [
        ...     {"status": "inactive", "val": 15},
        ...     {"status": "active", "val": 20},
        ... ]
        >>> calculate_active_item_value(items)
        22.0
    """
    # Early return if items list is empty or None
    if not items:
        return None
    
    # Secret key retrieval (for API authentication if needed in future)
    try:
        secret_key = get_secret_key()
    except SecretKeyNotFoundError as e:
        # Log warning but don't fail if secret not needed for this operation
        print(f"Warning: {e}")
        secret_key = None
    
    for item in items:
        # Skip invalid items
        if not is_item_valid(item):
            continue
        
        # Check if item meets all criteria
        if not is_item_active(item):
            continue
            
        try:
            item_value = float(item["val"])
        except (TypeError, ValueError, KeyError) as e:
            raise InvalidItemDataError(
                f"Item has invalid 'val' field: {item.get('val')}"
            ) from e
        
        if item_value > MINIMUM_VALUE_THRESHOLD:
            print(f"Found qualifying item with value: {item_value}")
            
            try:
                result = calculate_markup_value(item_value)
                return result
            except ValueError as e:
                raise InvalidItemDataError(
                    f"Failed to calculate markup for item value {item_value}"
                ) from e
    
    return None


# Example usage and testing
if __name__ == "__main__":
    # Set environment variable for testing
    os.environ["STRIPE_SECRET_KEY"] = "sk_test_example_key_for_testing"
    
    # Test data
    test_items = [
        {"status": "inactive", "val": 15},
        {"status": "active", "val": 5},
        {"status": "active", "val": 20},
        {"status": "active", "val": 30},
    ]
    
    try:
        result = calculate_active_item_value(test_items)
        print(f"Result: {result}")  # Expected: 22.0 (20 * 1.1)
    except (SecretKeyNotFoundError, InvalidItemDataError) as e:
        print(f"Error: {e}")
```

## Key Improvements:

1. **Security**: Removed hardcoded secret key, now loaded from environment variable `STRIPE_SECRET_KEY`
2. **Naming**: Renamed `p` → `calculate_active_item_value`, `d` → `items`, `k` → `secret_key`, etc.
3. **Type Hints**: Added complete type annotations for all functions
4. **Error Handling**: Replaced bare `except:` with specific exception handling
5. **Reduced Nesting**: Extracted helper functions (`is_item_valid`, `is_item_active`, `calculate_markup_value`)
6. **Constants**: Extracted magic numbers to named constants (`MINIMUM_VALUE_THRESHOLD`, `MARKUP_MULTIPLIER`)
7. **Docstrings**: Added comprehensive Google-style docstrings
8. **Custom Exceptions**: Created domain-specific exceptions for better error handling
9. **Early Returns**: Used guard clauses to reduce nesting
10. **Validation**: Improved data validation with explicit checks