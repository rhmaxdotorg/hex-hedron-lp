# HEX and Hedron Liquidity Pool Tracker

# How it works
Uses dexscreener's API to query (the biggest) pools for HEX and Hedron crypto as of March 2023 (pools are hardcoded, so may need updating from time to time). **It does not get numbers from ALL pools**, but a few signficiant ones.

Basically just queries https://api.dexscreener.com/latest/dex/pairs/ethereum/ and parses JSON values from response['pair']['liquidity']['usd'] and formats numbers so changes and total values are easy to understand.

There's only 3 adjustments in code you may want to make
- Pools for HEX_POOLS and HDRN_POOLS (optional, add/remove as fits your scenario)
- SLEEP_TIME
- ALERT_PERCENTAGE

# Dependencies
**Windows**

Install Python 3 from https://www.python.org/downloads/windows/ and bring up a command line terminal to use Python and run the script.

**Linux**

Python 3 should come installed by default, if not, do `apt install python3 python3-pip -y` on Debian/Ubuntu Linux distributions.

**Mac**

Python 2 may be installed by default, but to install Python 3 you can follow the instructions [here](https://docs.python-guide.org/starting/install3/osx/) and `brew install python`.

# How to use it

**Command Line Interface** (code can be repurposed for a web portal as well)
```
$ ./lp.py
./lp.py [get or track] [hex or hdrn]
```

**Get Total Hedron liquidity**
```
$ ./lp.py get hdrn
HDRN: $4,210,140
```

**Get both HEX and HDRN liquidity**
```
$ ./lp.py get all
HEX: $13,121,310
HDRN: $3,188,492
```

**Track HEX liquidity changes**
```
$ ./lp.py track hex
-0.42%
-0.27%

[!!!] LP CHANGED BY -8.96% (alert set on >= 5.00%) [!!!]

-8.96%
-0.84%
+0.59%
+0.65%
+0.07%
+0.60%
+0.39%
+0.07%
+0.81%
-1.56%
...
```

Of course this is just testing console alerts (this could also be email alerts, written to a file that is monitored, etc) with 0.03%, but you can adjust it to alert on 15% moves over 4hr time periods, whatever you think is useful for tracking LP.
