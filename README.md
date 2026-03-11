# Limit Order Book Simulator

This project implements an in-memory limit order book that processes buy and sell orders for a single instrument and matches them in real time using price-time priority. The engine reads orders from an input file and prints trade executions along with the final order book state.

Features

Core Requirements
- Support for LIMIT orders
- Support for MARKET orders (price = 0)
- Price-time priority matching
- Partial order fills
- Cancel resting orders
- Print final order book snapshot (top 5 bid/ask levels)

Bonus
- Real-time Best Bid Offer (BBO) updates
- Throughput benchmark for order processing

Order Format

ORDER_ID SIDE PRICE QUANTITY

Example:
O1 BUY 100.50 10
O2 SELL 101.00 5

Cancel command:
CANCEL ORDER_ID

Trade Output

TRADE BUY_ORDER SELL_ORDER PRICE QUANTITY

Example:
TRADE O1 O3 100.50 8

Data Structures

- defaultdict(deque) for storing orders at each price level
- deque to maintain FIFO order (time priority)
- order_map dictionary for fast order cancellation

This ensures price-time priority in matching.

Project Structure

limit-order-book
│
├── src
│   ├── order.py
│   ├── parser.py
│   ├── order_book.py
│   └── engine.py
│
├── tests
│   └── sample_input.txt
│
├── main.py
└── README.md

Run the Program

python main.py tests/sample_input.txt

Example Output

TRADE O1 O3 100.50 8
TRADE O1 O4 99.00 2
TRADE O2 O4 99.00 5

--- Book ---
ASK: 99.00 x 13

Processed in 0.000321 seconds

Design Notes

- Matching follows price-time priority
- Trades occur at the resting order's price
- System designed for clarity and correctness
