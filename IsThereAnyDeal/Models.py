from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ITADGame:
    id: str
    slug: str
    title: str
    type: str
    assets: Dict

    @staticmethod
    def from_dict(obj: Any):
        id = str(obj.get("id"))
        slug = str(obj.get("slug"))
        title = str(obj.get("title"))
        type = str(obj.get("type"))
        assets = dict(obj.get("assets"))
        return ITADGame(id, slug, title, type, assets)

@dataclass
class ITADPriceInfo:
    amount: float = field(default=0.0)
    currency: str = field(default='EUR')

    @staticmethod
    def from_dict(obj: Any):
        if obj is None:
            return ITADPriceInfo()

        amount = obj.get("amount")
        currency = obj.get("currency")
        return ITADPriceInfo(amount, currency)

@dataclass
class ITADPrice:
    price: ITADPriceInfo = field(default_factory=ITADPriceInfo)
    regular: ITADPriceInfo = field(default_factory=ITADPriceInfo)
    cut: int = 0
    timestamp: str = ''
    expiry: str = ''

    @staticmethod
    def from_dict(obj: Any):
        if obj is None:
            return ITADPrice()

        price = ITADPriceInfo.from_dict(obj.get("price"))
        regular = ITADPriceInfo.from_dict(obj.get("regular"))
        cut = obj.get("cut")
        timestamp = str(obj.get("timestamp"))
        expiry = str(obj.get("expiry"))
        return ITADPrice(price, regular, cut, timestamp, expiry)

@dataclass
class ITADPriceOverview:
    id: str
    current: ITADPrice
    lowest: ITADPrice

    @staticmethod
    def from_dict(obj: Any):
        id = str(obj.get("id"))
        current = ITADPrice.from_dict(obj.get("current"))
        lowest = ITADPrice.from_dict(obj.get("lowest"))
        return ITADPriceOverview(id, current, lowest)
    
@dataclass
class ITADPricesOverview:
    prices: list[ITADPriceOverview]

    @staticmethod
    def from_dict(obj: Any):
        prices = [ITADPriceOverview.from_dict(y) for y in obj.get("prices")]
        return ITADPricesOverview(prices)