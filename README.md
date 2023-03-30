# Cardano Leader Slot
Scheduled Block Checker for Cardano Stakepool Operators. 

![leader-slot](https://user-images.githubusercontent.com/82296005/196404189-f0b41e84-2996-4772-ab0e-d1ab80935a5c.png)


Lightweight and Portable Scheduled Blocks Checker for Next, Current and Previous Epochs.
No cardano-cli required, just your VRF Key file. All data is taken from [Koios API](https://www.koios.rest/) and [Armada Alliance](https://armada-alliance.com/)

Note: This is a reworking of old python script ScheduledBlocks.py 
available on https://github.com/papacarp/pooltool.io.git , Ouroboros TPraos version: https://github.com/asnakep/ScheduledBlocks and using Ouroboros Praos updated code from https://github.com/dostrelith678/cardano-leader-logs


## Prerequisites:
- Python 3.8 or higher version
- pip (Python package installer)
- libsodium library
- Koios-Python Library

### Installing libsodium library
First of all you need libsodium library installed, If not follow these steps:


```shell 

git clone https://github.com/input-output-hk/libsodium.git

cd libsodium

git checkout 1.0.16-519-g66f017f1

./autogen.sh

./configure

make

sudo make install

```

## Update:

- Go to your Git folder where is this repository cloned and run:
```
git pull
```

- Make sure that you have the last version of Koios Python [https://github.com/cardano-community/koios-python] running:
```
pip install koios-python -U
```

## Setup:

- Clone this repository using git: 
``` git clone https://github.com/QuixoteSystems/cardano-leader-slot.git ```

- Execute inside the newly cloned directory: 
```pip install -r pip_requirements.txt ```  to install all needed python package requirements

- Make sure you can access your vrf.skey file (you can copy in it a path of your choice) and remember to keep it as read only ``` chmod 400 vrf.skey ```

- Set Pool Variables on lines 35-39 of leaderslot.py:

~~~

### Set These Variables -------------------------------------------###

pool_ticker = "YOUT_POOL_TICKER"
vrf_key_file = ('YOUR_VRF_FILE_PATH')
pool_id_bech32 = "YOUR_POOL_ID:_pool1..."

### -------------------------------------------------------------- ###
~~~


## Usage:

``` python3 leaderslot.py ```


## Output: 
- a *console output* with all the slots assigned for next, current and previous Epochs

Output Example of a Previous Epoch:

![360](https://user-images.githubusercontent.com/82296005/196671094-733b586b-b3f8-4487-89ac-1745d41495a6.png)

