import pytest
from unittest.mock import patch, MagicMock
from services.api_service import get_game_deals, requests


@patch('services.api_service.requests.get')
def test_get_game_deals_success(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {
            'title': 'Game 1',
            'salePrice': '19.99',
            'normalPrice': '39.99',
            'dealID': '123',
            'metacriticScore': '90',
            'dealRating': '9.5'
        },
        {
            'title': 'Game 2',
            'salePrice': '15.99',
            'normalPrice': '29.99',
            'dealID': '456',
            'metacriticScore': '88',
            'dealRating': '9.0'
        }
    ]

    mock_get.return_value = mock_response

    deals = get_game_deals()

    assert len(deals) == 2
    assert deals[0]['title'] == 'Game 1'
    assert deals[1]['title'] == 'Game 2'


@patch('services.api_service.requests.get')
def test_get_game_deals_error(mock_get):
    mock_get.side_effect = requests.RequestException('API failure')

    deals = get_game_deals()

    assert deals == []