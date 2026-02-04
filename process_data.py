import os
from typing import Dict, List, Optional, Any


def process_records(records: List[Dict[str, Any]]) -> Optional[float]:
    """
    Process a list of records to find and calculate adjusted value.
    
    Searches for the first active record with a value greater than 10,
    then applies a 10% markup to that value.
    
    Args:
        records: List of record dictionaries containing 'status' and 'val' keys
        
    Returns:
        The adjusted value (original * 1.1) if a qualifying record is found,
        None otherwise
        
    Raises:
        ValueError: If API key is not configured in environment
    """
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise ValueError("STRIPE_API_KEY environment variable must be set")
    
    # WHY: Find first qualifying record to apply business logic
    # Records must be active with value > 10 to receive the adjustment
    qualifying_record = _find_qualifying_record(records)
    
    if qualifying_record is None:
        return None
    
    return _calculate_adjusted_value(qualifying_record)


def _find_qualifying_record(records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Find the first record that meets processing criteria.
    
    Args:
        records: List of record dictionaries
        
    Returns:
        First record with status='active' and val>10, or None if not found
    """
    for record in records:
        # WHY: Skip null/empty records to avoid processing invalid data
        if not record:
            continue
            
        # WHY: Only process active records per business requirements
        if record.get('status') != 'active':
            continue
            
        # WHY: 10 is the minimum threshold for adjustment eligibility
        if record.get('val', 0) > 10:
            print("found one")
            return record
    
    return None


def _calculate_adjusted_value(record: Dict[str, Any]) -> Optional[float]:
    """
    Calculate adjusted value with 10% markup.
    
    Args:
        record: Dictionary containing 'val' key
        
    Returns:
        Adjusted value (original * 1.1), or None if calculation fails
    """
    try:
        # WHY: Apply 10% markup as per pricing policy
        original_value = record['val']
        adjusted_value = original_value * 1.1
        return adjusted_value
    except (KeyError, TypeError, ValueError) as error:
        # WHY: Log specific errors for debugging but don't crash the process
        print(f"Error calculating adjusted value: {error}")
        return None