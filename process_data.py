import logging
from typing import List, Optional, TypedDict

# Configure logging
logger = logging.getLogger(__name__)

# Named constants
MINIMUM_VALUE_THRESHOLD = 10
MARKUP_PERCENTAGE = 0.1


class ItemDict(TypedDict):
    """Type definition for item structure."""
    status: str
    val: float


def find_first_active_item_with_markup(data: List[ItemDict]) -> Optional[float]:
    """
    Find the first active item above threshold and return its value with markup.
    
    Searches through the data for the first item that meets all criteria:
    - Item exists (not None/empty)
    - Status is 'active'
    - Value exceeds MINIMUM_VALUE_THRESHOLD
    
    Args:
        data: List of dictionaries containing item information with 'status' and 'val' keys
        
    Returns:
        Float value with markup applied if matching item found, None otherwise
        
    Raises:
        ValueError: If item value cannot be converted to float or markup calculation fails
    """
    for item in data:
        if item and _is_active_item_above_threshold(item):
            return _apply_markup_to_value(item)
    
    logger.info("No active items above threshold found")
    return None


def _is_active_item_above_threshold(item: ItemDict) -> bool:
    """
    Determine if an item meets processing criteria.
    
    Args:
        item: Dictionary containing 'status' and 'val' keys
        
    Returns:
        True if item is active and value exceeds threshold, False otherwise
    """
    return (
        item.get('status') == 'active' 
        and item.get('val', 0) > MINIMUM_VALUE_THRESHOLD
    )


def _apply_markup_to_value(item: ItemDict) -> float:
    """
    Apply markup percentage to item value.
    
    Args:
        item: Dictionary containing 'val' key with numeric value
        
    Returns:
        Value with markup applied
        
    Raises:
        ValueError: If value cannot be converted to float or is missing
    """
    try:
        value = float(item['val'])
        result = value * (1 + MARKUP_PERCENTAGE)
        logger.debug(f"Applied {MARKUP_PERCENTAGE*100}% markup: {value} -> {result}")
        return result
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"Failed to calculate markup for item {item}: {e}")
        raise ValueError(f"Invalid item value for markup calculation: {e}") from e


# Unit tests
import unittest


class TestItemProcessing(unittest.TestCase):
    """Unit tests for item processing functions."""
    
    def test_find_active_item_with_valid_data(self):
        """Test finding active item with value above threshold."""
        data = [
            {'status': 'active', 'val': 20},
            {'status': 'active', 'val': 30}
        ]
        result = find_first_active_item_with_markup(data)
        self.assertAlmostEqual(result, 22.0)
    
    def test_find_active_item_skips_inactive(self):
        """Test that inactive items are skipped."""
        data = [
            {'status': 'inactive', 'val': 20},
            {'status': 'active', 'val': 15}
        ]
        result = find_first_active_item_with_markup(data)
        self.assertAlmostEqual(result, 16.5)
    
    def test_find_active_item_skips_below_threshold(self):
        """Test that items below threshold are skipped."""
        data = [
            {'status': 'active', 'val': 5},
            {'status': 'active', 'val': 20}
        ]
        result = find_first_active_item_with_markup(data)
        self.assertAlmostEqual(result, 22.0)
    
    def test_find_active_item_returns_none_when_no_match(self):
        """Test None is returned when no items match criteria."""
        data = [
            {'status': 'inactive', 'val': 20},
            {'status': 'active', 'val': 5}
        ]
        result = find_first_active_item_with_markup(data)
        self.assertIsNone(result)
    
    def test_find_active_item_with_empty_list(self):
        """Test empty list returns None."""
        result = find_first_active_item_with_markup([])
        self.assertIsNone(result)
    
    def test_is_active_item_above_threshold_true(self):
        """Test item criteria check returns True for valid item."""
        item = {'status': 'active', 'val': 15}
        self.assertTrue(_is_active_item_above_threshold(item))
    
    def test_is_active_item_above_threshold_false_inactive(self):
        """Test item criteria check returns False for inactive item."""
        item = {'status': 'inactive', 'val': 15}
        self.assertFalse(_is_active_item_above_threshold(item))
    
    def test_is_active_item_above_threshold_false_low_value(self):
        """Test item criteria check returns False for low value."""
        item = {'status': 'active', 'val': 5}
        self.assertFalse(_is_active_item_above_threshold(item))
    
    def test_apply_markup_to_value_success(self):
        """Test markup calculation with valid value."""
        item = {'val': 100}
        result = _apply_markup_to_value(item)
        self.assertAlmostEqual(result, 110.0)
    
    def test_apply_markup_to_value_raises_on_missing_key(self):
        """Test markup calculation raises ValueError on missing key."""
        item = {}
        with self.assertRaises(ValueError):
            _apply_markup_to_value(item)
    
    def test_apply_markup_to_value_raises_on_invalid_type(self):
        """Test markup calculation raises ValueError on invalid type."""
        item = {'val': 'invalid'}
        with self.assertRaises(ValueError):
            _apply_markup_to_value(item)
    
    def test_apply_markup_with_string_number(self):
        """Test markup calculation handles string numbers."""
        item = {'val': '50'}
        result = _apply_markup_to_value(item)
        self.assertAlmostEqual(result, 55.0)


if __name__ == '__main__':
    unittest.main()