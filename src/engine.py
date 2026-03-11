from src.order_book import OrderBook
from src.parser import parse_line


def run_engine(file_path):

    book = OrderBook()

    with open(file_path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            cmd, data = parse_line(line)

            if cmd == "ORDER":
                book.add_order(data)

            elif cmd == "CANCEL":
                book.cancel(data)

    # after processing all orders
    book.print_book()