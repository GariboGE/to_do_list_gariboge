import requests

CHEAPSHARK_API_URL = "https://www.cheapshark.com/api/1.0/deals"


def get_game_deals():
    """
    Fetch and filter game deals from the CheapShark API.

    This function makes an HTTP GET request to the CheapShark API to retrieve game deals
    from the specified store. It filters deals based on the criteria that the game's
    Metacritic score must be greater than 85 and the deal rating should be 9 or higher.
    The resulting list includes only the title, sale price, normal price, deal link,
    Metacritic score, and deal rating.

    Returns:
        list[dict]: A list of dictionaries containing filtered game deal information.
            Each dictionary includes the following keys:
            - 'title' (str): The title of the game.
            - 'salePrice' (str): The sale price of the game.
            - 'normalPrice' (str): The original price of the game.
            - 'dealID' (str): A URL linking to the game deal.
            - 'metacriticScore' (str): Metacritic score of the game.
            - 'dealRating' (str): Deal rating given by the users.
        
        Returns an empty list if the request fails or no deals meet the filtering criteria.
    """
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
