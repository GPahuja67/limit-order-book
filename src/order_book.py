def match(self, order):

    while order.qty > 0:

        if order.side == "BUY":
            best_price = self.best_ask()

            if best_price is None:
                break

            if order.price != 0 and best_price > order.price:
                break

            queue = self.asks[best_price]

        else:
            best_price = self.best_bid()

            if best_price is None:
                break

            if order.price != 0 and best_price < order.price:
                break

            queue = self.bids[best_price]

        top = queue[0]

        trade_qty = min(order.qty, top.qty)

        print(f"TRADE {order.id} {top.id} {best_price} {trade_qty}")

        order.qty -= trade_qty
        top.qty -= trade_qty

        if top.qty == 0:
            queue.popleft()
            del self.order_map[top.id]