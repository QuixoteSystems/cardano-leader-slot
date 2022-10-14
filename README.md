# Cardano Leader Slot
Scheduled Block Checker for Cardano Stakepool Operators. 

*Warning: At the moment this script are working for the Current and Next epochs.*

![cardano](https://user-images.githubusercontent.com/82296005/193456430-4aad96b9-5306-49d7-afe6-30f2320f15b0.jpg)


Lightweight and Portable Scheduled Blocks Checker for Next, Current and Previous Epochs.
No cardano-node required, data is taken from [Koios API](https://www.koios.rest/) and [adamantium.online](https://adamantium.online/)

Note: This is a reworking of old python script ScheduledBlocks.py 
available on https://github.com/papacarp/pooltool.io.git , Ouroboros TPraos version: https://github.com/asnakep/ScheduledBlocks and using Ouroboros Praos updated code from https://github.com/dostrelith678/cardano-leader-logs


## Prerequisites:
- Python 3.8 or higher version
- pip (Python package installer)
- libsodium library

## Setup:

- Clone this repository using git: ``` git clone https://github.com/QuixoteSystems/cardano-leader-slot.git ```
- Execute inside the newly cloned directory: ```pip install -r pip_requirements.txt ```  to install all needed python package requirements
- Make sure you can access your vrf.skey file (you can copy in it a path of your choice) and remember to keep it as read only ``` chmod 400 vrf.skey ```

- Set Variables on lines 27-35 of leaderslot.py:

~~~
### Set your onw timezone -----------------------------------------###
local_tz = pytz.timezone('Europe/Berlin')

### Set These Variables ###
PoolTicker = "YOUR_POOL_TICKER"
VrfKeyFile = ('YOUR_VRF_FILE_PATH')
pool_id_bech32 = "YOUR_POOL_ID:_pool1..."

### -------------------------------------------------------------- ###
~~~


## Usage:

``` python3 leaderslot.py ```


## Output: 
- a *console output* with all the slots assigned for next, current and previous Epochs
