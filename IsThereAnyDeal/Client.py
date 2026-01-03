import logging
from typing import Optional
import requests
import urllib.parse

from IsThereAnyDeal.Models import *

CFG_ISTHEREANYDEAL = 'IsThereAnyDeal'
CFG_BASEURL = 'BaseUrl'
CFG_APIKEY = 'ApiKey'

# ============================================================================
# IS THERE ANY DEAL
# ============================================================================
class IsThereAnyDeal:
    def __init__(self) -> None:
        self.m_log = logging.getLogger("SDB - IsThereAnyDeal")
        self.m_has_valid_config = False

# CONFIG FILE ----------------------------------------------------------------
    def load_config( self, _json: dict ):
        if CFG_ISTHEREANYDEAL not in _json:
            self.m_log.error(f"No {CFG_ISTHEREANYDEAL} section found in config file")
            return
        
        config = _json[CFG_ISTHEREANYDEAL]
        if CFG_APIKEY in config:
            self.m_apiKey = config[CFG_APIKEY]
        
        if CFG_BASEURL in config:
            self.m_baseUrl = config[CFG_BASEURL]

        self.m_has_valid_config = True

    def save_config( self, _json_data: dict ):
        if not self.m_has_valid_config:
            return

        _json_data[ CFG_ISTHEREANYDEAL ] = {
            CFG_APIKEY: self.m_apiKey,
            CFG_BASEURL: self.m_baseUrl,
        }

# FUNCTIONS ----------------------------------------------------------------
    def find_games_deals( self, _name: str ):
        # Search game
        games = self.search_games(_name)

        if len(games) == 0:
            self.m_log.info(f"No result found for {_name}")
            return FindResult(total_games=len(games))

        # Get first game's prices
        first_game = games[0]
        overview = self.fetch_game_prices_overview(first_game.id)
        
        if len(overview.prices) == 0:
            self.m_log.info(f"Game {first_game.title} has no prices")
            return FindResult(total_games=len(games), game=first_game)
        
        first_game_price = overview.prices[0]
        return FindResult(
            total_games=len(games),
            game=first_game,
            prices=PricesResult(
                current=first_game_price.current.price.amount,
                regular=first_game_price.current.regular.amount,
                lowest=first_game_price.lowest.price.amount,
                cut=first_game_price.current.cut,
                expiry=first_game_price.current.expiry,
                currency=first_game_price.current.price.currency,
            )
        )
    
    def search_games( self, _title: str ):
        self.m_log.info(f"Searching for {_title}")

        params = {"key": self.m_apiKey, "title": _title}
        results = requests.get(f"{self.m_baseUrl}/games/search/v1", params=params)

        if results.status_code >= 400:
            raise Exception(f"Error when searching games : {results.status_code} {results.reason}")
        
        return [ITADGame.from_dict(r) for r in results.json()]


    def fetch_game_prices_overview( self, _id ):
        self.m_log.info(f"Fetching prices overview for {_id}")

        params = {"key": self.m_apiKey, "country": "FR"}
        data = [_id]
        results = requests.post(f"{self.m_baseUrl}/games/overview/v2", params=params, json=data)

        return ITADPricesOverview.from_dict(results.json())

    @staticmethod
    def get_game_url( _slug: str ):
        return f"https://isthereanydeal.com/game/{_slug}"
    
    @staticmethod
    def get_search_url( _search: str ):
        encoded = urllib.parse.quote_plus(_search)
        return f"https://isthereanydeal.com/search/?q={encoded}"
    
@dataclass
class PricesResult:
    current: float
    regular: float
    lowest: float
    cut: int
    expiry: Optional[datetime]
    currency: str

@dataclass
class FindResult:
    total_games: int
    game: Optional[ITADGame] = None
    prices: Optional[PricesResult] = None
