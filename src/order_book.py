from collections import defaultdict, deque

class OrderBook:

    def __init__(self):

        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)

        self.order_map = {}

    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None