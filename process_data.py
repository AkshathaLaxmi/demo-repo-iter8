import os
from typing import Dict, List, Optional, Any, Union


class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass


def calculate_active_item_value(
    data_items: List[Dict[str, Any]]
) -> Optional[float]:
    """
    Process a list of data items and calculate an adjusted value for the first
    active item that meets the threshold criteria.

    This function iterates through a list of data items, finds the first item
    that is marked as 'active' and has a value greater than 10, then applies
    a 10% adjustment to that value.

    Args:
        data_items: A list of dictionaries containing item data. Each dictionary
                   should have 'status' (str) and 'val' (numeric) keys.

    Returns:
        Optional[float]: The adjusted value (original value * 1.1) if a matching
                        item is found, None otherwise.

    Raises:
        DataProcessingError: If there's an error processing the item value.

    Example:
        >>> items = [
        ...     {'status': 'active', 'val': 15},
        ...     {'status': 'inactive', 'val': 20}
        ... ]
        >>> calculate_active_item_value(items)
        16.5
    """
    # Retrieve API key from environment variables instead of hardcoding
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise ValueError(
            "STRIPE_API_KEY environment variable is not set. "
            "Please configure it before running this function."
        )

    # Validate input
    if not isinstance(data_items, list):
        raise TypeError(f"Expected list for data_items, got {type(data_items).__name__}")

    # Process items with reduced nesting
    for item in data_items:
        # Skip empty/None items
        if not item:
            continue

        # Validate item structure
        if not isinstance(item, dict):
            continue

        # Check if item meets criteria
        if item.get('status') != 'active':
            continue

        try:
            item_value = float(item.get('val', 0))
        except (ValueError, TypeError) as e:
            raise DataProcessingError(
                f"Invalid value type for item: {item}. Error: {str(e)}"
            ) from e

        if item_value <= 10:
            continue

        # Calculate and return adjusted value
        try:
            adjusted_value = item_value * 1.1
            return adjusted_value
        except (TypeError, ArithmeticError) as e:
            raise DataProcessingError(
                f"Failed to calculate adjusted value for item_value={item_value}. "
                f"Error: {str(e)}"
            ) from e

    # No matching item found
    return None