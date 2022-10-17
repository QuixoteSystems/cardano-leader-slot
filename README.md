# Cardano Leader Slot
Scheduled Block Checker for Cardano Stakepool Operators. 

![cardano-leader-slot](https://user-images.githubusercontent.com/82296005/195933862-96568b7d-4378-42a5-90a7-47195051889a.png)


Lightweight Scheduled Blocks Checker for Next, Current and Previous Epochs.
No cardano-node required for current and previous, just your VRF Key file. Will need cardano-cli connected to a node for next. All data is taken from [Koios API](https://www.koios.rest/) & the blockchain with cardano-cli.

Note: This is a reworking of old python script ScheduledBlocks.py 
available on https://github.com/papacarp/pooltool.io.git , Ouroboros TPraos version: https://github.com/asnakep/ScheduledBlocks and using Ouroboros Praos updated code from https://github.com/dostrelith678/cardano-leader-logs

Next nonce with cardano-cli credited to SNAKE pool https://github.com/asnakep/getNewEpochNonce, https://github.com/asnakep/YaLL


## Prerequisites:
- Python 3.8 or higher version
- pip (Python package installer)
- libsodium library

## Setup:

- Clone this repository using git: ``` git clone https://github.com/QuixoteSystems/cardano-leader-slot.git ```
- Execute inside the newly cloned directory: ```pip install -r pip_requirements.txt ```  to install all needed python package requirements
- Make sure you can access your vrf.skey file (you can copy in it a path of your choice) and remember to keep it as read only ``` chmod 400 vrf.skey ```

- Create a .env file and set variables in .env:

~~~
### Set your own timezone -----------------------------------------###
local_tz = "Europe/Berlin"

### Set These Variables ###
pool_ticker = "YOUT_POOL_TICKER"
vrf_key_file = ('YOUR_VRF_FILE_PATH')
pool_id_bech32 = "YOUR_POOL_ID:_pool1..."

### -------------------------------------------------------------- ###
~~~


## Usage:

``` python3 leaderslot.py ```


## Output: 
- a *console output* with all the slots assigned for next, current and previous Epochs
