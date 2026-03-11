class Order:
    def __init__(self, order_id, side, price, quantity, timestamp):
        self.id = order_id
        self.side = side
        self.price = float(price)
        self.qty = int(quantity)
        self.timestamp = timestamp