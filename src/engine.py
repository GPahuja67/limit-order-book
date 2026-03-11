from src.order_book import OrderBook
from src.parser import parse_line
import time


def run_engine(file_path):

    start = time.time()

    book = OrderBook()

    with open(file_path) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            cmd, data = parse_line(line)

            if cmd == "ORDER":
                book.add_order(data)

            elif cmd == "CANCEL":
                book.cancel(data)

    book.print_book()

    end = time.time()

    duration = end - start

    print(f"\nProcessed in {duration:.6f} seconds")