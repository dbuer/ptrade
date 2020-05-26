# ptrade
This is a python wrapper for the Etrade API. It handles authentication and provides an interface for making requests.

## Getting started
To use this library, you must have API consumer keys, which require an Etrade account. Visit their [getting started page](https://developer.etrade.com/getting-started) to learn more.

### Setup [temp]
0. Acquire consumer keys from Etrade.
1. Clone this repo.
2. Run `pip install -e .` in the cloned directory to install this package.

### Example
0. Read the example code given in [examples/starter.py](https://github.com/dbuer/ptrade/blob/master/examples/starter.py).
1. Provide program with consumer keys (example uses a .env file).
2. Run the example program in a terminal: `python3 starter.py`.
3. Login to your Etrade account when prompted by your browser.
4. Read and accept the terms and agreements.
5. Copy the verification code given to you by Etrade, and paste it into the console where you ran the program.
6. The program prints the output of a few common api requests, use as desired.
