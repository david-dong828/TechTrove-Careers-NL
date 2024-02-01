# Name: Dong Han
# Mail: dongh@mun.ca

import pytest
from unittest.mock import patch, MagicMock
from api import index
from api import database_handle

@pytest.fixture
def mock_aip_companies():
    return {
        "verafin": "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin",
    }


@patch('api.index.readjson')
@patch('api.index.find_value_by_partial_key')
@patch('api.index.api.getCompniesCareerPage.ScraperFactory.get_scraper')
def test_get_jobs_success(mock_get_scraper, mock_find_value, mock_readjson, mock_aip_companies):
    # Setup mock responses
    mock_readjson.return_value = mock_aip_companies
    mock_find_value.return_value = "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin"
    mock_scraper_instance = MagicMock()
    mock_scraper_instance.scrape.return_value = {"jobs": "some job data"}
    mock_get_scraper.return_value = mock_scraper_instance

    # Call the function under test
    result = index.get_jobs("verafin")

    # Assertions
    mock_readjson.assert_called_once()
    mock_find_value.assert_called_once_with(mock_aip_companies, "verafin")
    mock_get_scraper.assert_called_once_with("verafin", "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin")
    mock_scraper_instance.scrape.assert_called_once()
    assert result == {"jobs": "some job data"}


@patch('api.index.readjson')
@patch('api.index.find_value_by_partial_key')
def test_get_jobs_no_company_found(mock_find_value, mock_readjson, mock_aip_companies):
    # Setup mock responses
    mock_readjson.return_value = mock_aip_companies
    mock_find_value.return_value = None

    # Call the function under test expecting no company found
    result = index.get_jobs("nonexistent company")

    # Assertions
    assert result == -1

def test_planetscale_connection():
    planetscale_params = database_handle.get_planetscale_params()
    db, cursor = database_handle.connectDB()
    sql = "select * from NL_TECH_JOBS limit 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result != None
