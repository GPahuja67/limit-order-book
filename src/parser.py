from src.order import Order
import time


def parse_line(line):

    parts = line.strip().split()

    if parts[0] == "CANCEL":
        return ("CANCEL", parts[1])

    order_id = parts[0]
    side = parts[1]
    price = float(parts[2])
    qty = int(parts[3])

    order = Order(order_id, side, price, qty, time.time())

    return ("ORDER", order)