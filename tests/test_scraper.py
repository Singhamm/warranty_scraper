import pytest
from utils.scraper import scrape_warranty

def test_scraper_success():
    """Test with a known valid serial number (mock if needed)"""
    result = scrape_warranty("PF3A2XYZ")  # Replace with a test serial
    assert "product_name" in result
    assert "error" not in result

def test_scraper_failure():
    """Test error handling"""
    result = scrape_warranty("INVALID_SERIAL")
    assert "error" in result