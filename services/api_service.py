import requests

CHEAPSHARK_API_URL = "https://www.cheapshark.com/api/1.0/deals"

def get_game_deals():
    try:
        response = requests.get(CHEAPSHARK_API_URL, params={"storeID": "1", "upperPrice": "20"})
        response.raise_for_status()
        deals = response.json()

        filtered_deals = [
            {
                'title': deal.get('title', 'N/A'),
                'salePrice': deal.get('salePrice', 'N/A'),
                'normalPrice': deal.get('normalPrice', 'N/A'),
                'dealID': f"https://www.cheapshark.com/redirect.php?dealID={deal.get('dealID', '')}",
                'metacriticScore': deal.get('metacriticScore', 'N/A'),
                'dealRating': deal.get('dealRating', 'N/A'),
            }
            for deal in deals
            if int(deal.get('metacriticScore', 0)) > 85 and float(deal.get('dealRating', 0)) >= 9
        ]

        return filtered_deals

    except requests.RequestException as e:
        print(f"Error fetching deals: {e}")
        return []
