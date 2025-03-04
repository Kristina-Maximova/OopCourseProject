from unittest.mock import patch

from src.api_exchange_rate import get_usd_rate


@patch("requests.get")
def test_get_usd_rate(mock_get):
    mock_get.return_value.json.return_value = {'Valute': {
        'USD': {'ID': 'R01010', 'NumCode': '036', 'CharCode': 'AUD', 'Nominal': 1, 'Name': 'доллар', 'Value': 87.5133,
                'Previous': 87.8428}}}
    mock_get.return_value.status_code = 200
    result = get_usd_rate()
    assert result == 87.5133
    mock_get.assert_called_once()
