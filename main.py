import sys
from src.engine import run_engine


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    run_engine(input_file)