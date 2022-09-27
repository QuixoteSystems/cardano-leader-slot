# Cardano Leader Slot
Scheduled Block Checker for Cardano Stakepool Operators.

Lightweight and Portable Scheduled Blocks Checker for Next, Current and Previous Epochs.
No cardano-node required, data is taken from blockfrost.io and armada-alliance.com

Note: This is a reworking of old python script ScheduledBlocks.py 
available on https://github.com/papacarp/pooltool.io.git , Ouroboros TPraos version: https://github.com/asnakep/ScheduledBlocks and using Ouroboros Praos updated code from https://github.com/dostrelith678/cardano-leader-logs


## Prerequisites:
- Python 3.8
- pip (Python package installer)
- libsodium library

## Setup:
- clone this repository using git: ``` git clone https://github.com/QuixoteSystems/cardano-leader-slot.git ```
- execute inside the newly cloned directory: ```pip install -r pip_requirements.txt   ```  to install all needed python package requirements
- get a project id on blockfrost.io
- make sure you can access your vrf.skey file (you can copy in it a path of your choice) and remember to keep it as read only ``` chmod 400 vrf.skey ```

- Set Variables on lines 23, 27-30 of leaderslot.py:

### Set your own timezone -----------------------------------------###
local_tz = pytz.timezone('')

### Set These Variables ###
BlockFrostId = " "
PoolId = " "
PoolTicker = " "
VrfKeyFile = (' ')
### -------------------------------------------------------------- ###


## Usage:
``` python3 leaderslot.py ```

## Output: 
- a *console output* with all the slots assigned for next, current and previous Epochs
