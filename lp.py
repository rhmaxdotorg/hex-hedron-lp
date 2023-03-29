#!/usr/bin/python3
#
# lp.py - checks dexscreener LP data for HEX and HDRN pools
#

import os
import sys
import time
import json
import requests

#
# pools
#
# UPDATED AS OF 03/27/23 -- doesn't contain every pool, just the larger ones
#
# Note: better if there was a way to get list of all pools for token or pair and just use that
#

#HEX_USDC_POOL_ONE = "0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5" # hex/usdc big pool
#HEX_USDC_POOL_TWO = "0xe05e653453f733786f2dabae0ffa1e96cfcc4b25"
#HEX_USDC_POOL_THR = "0xf6dcdce0ac3001b2f67f750bc64ea5beb37b5824"
#HEX_WETH_POOL_ONE = "0x9e0905249ceefffb9605e034b534544684a58be6" # hex/weth
#HEX_WETH_POOL_TWO = "0x82743c07bf3be4d55876f87bca6cce5f84429bd0" # hex/weth
#HEX_HDRN_POOL_ONE = "0x035a397725d3c9fc5ddd3e56066b7b64c749014e" # hex/hdrn
#HEX_DAI_POOL_ONE = "0x63f7d912eae3e7a2ec19afdad0d7c7533ae0781c" # hex/dai

HEX_POOLS = ('0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5',
             '0xe05e653453f733786f2dabae0ffa1e96cfcc4b25',
             '0xf6dcdce0ac3001b2f67f750bc64ea5beb37b5824',
             '0x9e0905249ceefffb9605e034b534544684a58be6',
             '0x82743c07bf3be4d55876f87bca6cce5f84429bd0',
             '0x035a397725d3c9fc5ddd3e56066b7b64c749014e',
             '0x63f7d912eae3e7a2ec19afdad0d7c7533ae0781c')

#HDRN_USDC_POOL_ONE = "0xe859041c9c6d70177f83de991b9d757e13cea26e" # hdrn/usdc
#HDRN_USDC_POOL_TWO = "0x841bb1966c1d1b80634111691471c667e4c2bfe4"
#HDRN_HEX_POOL_ONE = "0x035a397725d3c9fc5ddd3e56066b7b64c749014e" # hdrn/hex
#HDRN_HEX_POOL_TWO = "0x4a97b4da0d43e1d36952e239cfda8922e8643931"

HDRN_POOLS = ('0xe859041c9c6d70177f83de991b9d757e13cea26e',
              '0x841bb1966c1d1b80634111691471c667e4c2bfe4',
              '0x035a397725d3c9fc5ddd3e56066b7b64c749014e',
              '0x4a97b4da0d43e1d36952e239cfda8922e8643931')

#
# config - comment/uncomment/modify as needed
#

#SLEEP_TIME = 5 # 5 seconds
SLEEP_TIME = 60 # 1 minute
#SLEEP_TIME = 60 * 5 # 5 minutes
#SLEEP_TIME = 60 * 60 * 2 # 2 hours

ALERT_PERCENTAGE = 0.03 # alert if -/+ 0.03% change
#ALERT_PERCENTAGE = 5 # alert if -/+ 5% change
#ALERT_PERCENTAGE = 15 # alert if -/+ 15% change
#ALERT_PERCENTAGE = 25 # alert if -/+ 25% change

#
# get LP (usd value) from pools
#
def getTotalLP(pools):
    response = None
    lp = 0

    for pool in pools:
        DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/ethereum/" + pool

        try:
            response = json.loads(requests.get(DEX_URL).text)
        except Exception as error:
            print("%s\n" % error)
            return None

        pairLP = response['pair']['liquidity']['usd']

        #print(pairLP)

        lp += int(pairLP)

    return lp

#
# track lp functuations
#
def trackTotalLP(coin):
    if(coin == 'hex'):
        pools = HEX_POOLS
    else:
        pools = HDRN_POOLS

    try:
        while True:
            positive = False

            lp = getTotalLP(pools)

            #
            # not sure what the best cadence is here -- check config above
            # perhaps you want to check every 1-4 hours to catch swings
            # and on a minute-basis if you want to chart data or otherwise
            #
            time.sleep(SLEEP_TIME)

            lpNow = getTotalLP(pools)

            if(lpNow != lp):
                #change = (abs(lpNow - lp) / lp) * 100
                change = ((lpNow - lp) / lp) * 100
                if(change > 0):
                    positive = True

                if(abs(change) >= ALERT_PERCENTAGE):
                    alert = "{:.2f}%".format(ALERT_PERCENTAGE)
                    change = "{0:.2f}".format(change)

                    print("\n[!!!] LP CHANGED BY %s%% (alert set on >= %s) [!!!]\n" % (change, alert))
                else:
                    change = "{0:.2f}".format(change)

                if(positive):
                    change = "+" + change

                if("0.00" not in change):
                    print("%s%%" % change)
    except KeyboardInterrupt:
        return

#
# main function
#
def main():
    if(len(sys.argv) < 3):
        print("%s [get or track] [hex or hdrn]" % sys.argv[0])
        return

    arg = sys.argv[1]
    coin = sys.argv[2]

    if(arg == 'get'):
        if(coin == 'hex'):
            totalLP = getTotalLP(HEX_POOLS)

            if(totalLP != None):
                print("HEX: ${:,}".format(totalLP))

        elif(coin == 'hdrn'):
            totalLP = getTotalLP(HDRN_POOLS)

            if(totalLP != None):
                print("HDRN: ${:,}".format(totalLP))

        else:
            print("invalid coin")
            return

    elif(arg == 'track'):
        if(coin != 'hex' and coin != 'hdrn'):
            print("invalid coin")
            return

        trackTotalLP(coin)

    return

if(__name__ == '__main__'):
	main()
