# HEX and Hedron Liquidity Pool Tracker

# How it works
Uses dexscreener's API to query (the biggest) pools for HEX and Hedron crypto as of March 2023 (pools are hardcoded, so may need updating from time to time). **It does not get numbers from ALL pools**, but a few signficiant ones.

https://api.dexscreener.com/latest/dex/pairs/ethereum/ and parsing JSON values from response['pair']['liquidity']['usd']

There's only 3 adjustments in code you may want to make
- Pools HEX_POOLS and HDRN_POOLS
- SLEEP_TIME
- ALERT_PERCENTAGE

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
