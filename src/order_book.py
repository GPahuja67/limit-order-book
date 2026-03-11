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


    # ---------------- BBO ----------------
    def print_bbo(self):

        bid = self.best_bid()
        ask = self.best_ask()

        bid_str = bid if bid is not None else "None"
        ask_str = ask if ask is not None else "None"

        print(f"BBO: BID {bid_str} | ASK {ask_str}")


    # ---------------- MATCHING ----------------
    def match(self, order):

        while order.qty > 0:

            if order.side == "BUY":

                best_price = self.best_ask()

                if best_price is None:
                    break

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

            trade_price = top.price

            print(f"TRADE {buy_id} {sell_id} {trade_price} {trade_qty}")

            order.qty -= trade_qty
            top.qty -= trade_qty

            if top.qty == 0:

                queue.popleft()
                del self.order_map[top.id]

            if not queue:

                if order.side == "BUY":
                    del self.asks[best_price]
                else:
                    del self.bids[best_price]


    # ---------------- ADD ORDER ----------------
    def add_order(self, order):

        self.match(order)

        if order.qty == 0:
            return

        book = self.bids if order.side == "BUY" else self.asks

        book[order.price].append(order)

        self.order_map[order.id] = order

        self.print_bbo()


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

        self.print_bbo()


    # ---------------- FINAL BOOK ----------------
    def print_book(self):

        print("\n--- Book ---")

        ask_prices = sorted(self.asks.keys())[:5]

        for p in ask_prices:

            qty = sum(o.qty for o in self.asks[p])

            print(f"ASK: {p} x {qty}")

        bid_prices = sorted(self.bids.keys(), reverse=True)[:5]

        for p in bid_prices:

            qty = sum(o.qty for o in self.bids[p])

            print(f"BID: {p} x {qty}")