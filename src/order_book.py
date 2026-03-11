from collections import defaultdict, deque


class OrderBook:

    def __init__(self):

        # price -> queue of orders
        self.bids = defaultdict(deque)   # BUY side
        self.asks = defaultdict(deque)   # SELL side

        # order_id -> order
        self.order_map = {}

    # best buy price
    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    # best sell price
    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None


    # ---------------- MATCHING ENGINE ----------------
    def match(self, order):

        while order.qty > 0:

            if order.side == "BUY":

                best_price = self.best_ask()

                if best_price is None:
                    break

                # price check for LIMIT order
                if order.price != 0 and best_price > order.price:
                    break

                queue = self.asks[best_price]

                buy_id = order.id
                sell_id = queue[0].id

            else:

                best_price = self.best_bid()

                if best_price is None:
                    break

                if order.price != 0 and best_price < order.price:
                    break

                queue = self.bids[best_price]

                buy_id = queue[0].id
                sell_id = order.id

            top = queue[0]

            trade_qty = min(order.qty, top.qty)

            print(f"TRADE {buy_id} {sell_id} {best_price} {trade_qty}")

            order.qty -= trade_qty
            top.qty -= trade_qty

            # remove filled order
            if top.qty == 0:
                queue.popleft()
                del self.order_map[top.id]

            # remove empty price level
            if not queue:
                if order.side == "BUY":
                    del self.asks[best_price]
                else:
                    del self.bids[best_price]


    # ---------------- ADD ORDER ----------------
    def add_order(self, order):

        # attempt match first
        self.match(order)

        # if fully executed
        if order.qty == 0:
            return

        book = self.bids if order.side == "BUY" else self.asks

        book[order.price].append(order)

        self.order_map[order.id] = order


    # ---------------- CANCEL ORDER ----------------
    def cancel(self, order_id):

        if order_id not in self.order_map:
            return

        order = self.order_map[order_id]

        book = self.bids if order.side == "BUY" else self.asks

        queue = book[order.price]

        for o in list(queue):
            if o.id == order_id:
                queue.remove(o)
                break

        if not queue:
            del book[order.price]

        del self.order_map[order_id]


    # ---------------- PRINT FINAL BOOK ----------------
    def print_book(self):

        print("\n--- Book ---")

        # asks (lowest first)
        ask_prices = sorted(self.asks.keys())[:5]

        for p in ask_prices:
            qty = sum(o.qty for o in self.asks[p])
            print(f"ASK: {p} x {qty}")

        # bids (highest first)
        bid_prices = sorted(self.bids.keys(), reverse=True)[:5]

        for p in bid_prices:
            qty = sum(o.qty for o in self.bids[p])
            print(f"BID: {p} x {qty}")