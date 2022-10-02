#!/bin/env python3

import requests
import urllib.request
import math
import binascii
import json
import pytz
import hashlib
import re
import readchar
from ctypes import *
from os import system, path
from datetime import datetime, timezone
from sys import exit, platform
import koios_python as kp
try:
    import pyfiglet
except:
    pass

class col:
    red = '\033[31m'
    green = '\033[92m'
    endcl = '\033[0m'

def ClearScreen():
    command ='clear'
    system(command)

### Set your onw timezone -----------------------------------------###
local_tz = pytz.timezone('Europe/Berlin')

### Set These Variables ###
PoolTicker = "YOUT_POOL_TICKER"
VrfKeyFile = ('YOUR_VRF_FILE_PATH')
pool_id_bech32 = "YOUR_POOL_ID:_pool1..."

### -------------------------------------------------------------- ###


### ADA Unicode symbol and Lovelaces removal ###
ada = " \u20B3"
lovelaces = 1000000

### Get Epoch Info from Adamantium Site (Star Forge Pool [OTG]) ###
otg_headers ={'content-type': 'application/json'}

### Get Next Epoch Nonce from Adamantium Site (Star Forge Pool [OTG]) ###
try:
    next_epoch_parameters = requests.get("https://nonce.adamantium.online/next.json", headers=otg_headers)
    json_data = next_epoch_parameters.json()
    next_epoch = next_epoch_parameters.json().get("epoch")
    next_eta0 = next_epoch_parameters.json().get("nonce")

    ErrorMsg = "Query returned no rows"
    if ErrorMsg in next_eta0 :
        msg = str(col.red + f'(New Nonce Not Avaliable Yet)')
    if ErrorMsg not in next_eta0 :
        msg = str(col.green + f'(Next Epoch Nonce Available)')

except OSError as ErrorMsg:
    msg = str(col.red + f'(Failed to establish connection to nonce.adamantium.online)')


### User Prompt Menu to select what kind of Epochs you want to know
print()
print()

### Figlet Fancy Welcome Header
try:
    cardano = pyfiglet.figlet_format("Cardano")
    leader_slot = pyfiglet.figlet_format("Leader Slot")

    print(col.green + cardano)
    print(col.green + leader_slot)
except:
    pass

print(col.green + f'Welcome to Light Leader Slot Script for Cardano SPOs. ')
print()
print(col.green + f'Check Assigned Blocks in Next, Current and Previous Cardano Epochs.')
print(col.endcl)
#print(col.green + f'Current Epoch: ' + col.endcl +str(current_epoch))


print(col.endcl)
print(f'(n) to Check Next Epoch Schedules ' +str(msg))
print(col.endcl)
print(f'(c) to Check Current Epoch')
print(col.endcl)

## TODO
#print(f'(p) to Check Previous Epochs')
#print(col.endcl)

print(f'(any key) to Exit')
print(col.endcl)

### Read Keyboard keys ###
key = readchar.readkey()


### NEXT EPOCH. Get data from Koios & OTG Pool ###

if key == 'n':

    ClearScreen()

    epoch_parameters = kp.get_tip()
    epoch = epoch_parameters[0]["epoch_no"]
    epoch = int(next_epoch)
    current_epoch = epoch - 1

    netStakeParam = kp.get_epoch_params(current_epoch)
    #eta0 =  netStakeParam[0]["nonce"]
    eta0= next_eta0
    epoch_info = kp.get_epoch_info(current_epoch)
    nStake = epoch_info[0]["active_stake"]

    poolStakeParam = kp.get_pool_info(pool_id_bech32)
    pStake = poolStakeParam[0]["active_stake"]

    sigma = float(pStake) / float(nStake)

    print()
    print(f'Checking SlotLeader Schedules for Stakepool: ' + (col.green + PoolTicker + col.endcl))
    print()
    print(f'Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print(f'Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print(f'Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print(f'Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(nStake) + col.endcl + ada + col.endcl)
    print()
    print(f'Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(pStake) + col.endcl + ada + col.endcl)
    print()


if key == 'p':

    ClearScreen()
    print()
    Epoch = input("Enter Epoch Previous Number: " + col.green)
    print(col.endcl)


### CURRENT EPOCH. Get data from Koios ###

if key == 'c':

    ClearScreen()

    epochParam = kp.get_tip()
    epoch = epochParam[0]["epoch_no"]

    netStakeParam = kp.get_epoch_params(epoch)
    eta0 =  netStakeParam[0]["nonce"]

    epoch_info = kp.get_epoch_info(epoch)
    nStake = epoch_info[0]["active_stake"]

    poolStakeParam = kp.get_pool_info(pool_id_bech32)
    pStake = poolStakeParam[0]["active_stake"]

    sigma = float(pStake) / float(nStake)


    print()
    print(f'Checking SlotLeader Schedules for Stakepool: ' + (col.green + PoolTicker + col.endcl))
    print()
    print(f'Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print(f'Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print(f'Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print(f'Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(nStake) + col.endcl + ada + col.endcl)
    print()
    print(f'Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(pStake) + col.endcl + ada + col.endcl)
    print()


### ############### ###
if(key != 'p') and (key != 'c') and (key != 'n'):
    exit(0)


### Calculate Slots Leader ###

### Opening vrf.skey file ###
with open(VrfKeyFile) as f:
        skey = json.load(f)
        poolVrfSkey = skey['cborHex'][4:]

### Determine libsodium path based on platform ###
libsodium = None
if platform == "linux" or platform == "linux2":
    # Bindings are not avaliable so using ctypes to just force it in for now.
    libsodium = cdll.LoadLibrary("/usr/local/lib/libsodium.so")
elif platform == "darwin":
    # Try both Daedalus' bundled libsodium and a system-wide libsodium path.
    daedalusLibsodiumPath = path.join("/Applications", "Daedalus Mainnet.app", "Contents", "MacOS", "libsodium.23.dylib")
    systemLibsodiumPath = path.join("/usr", "local", "lib", "libsodium.23.dylib")

    if path.exists(daedalusLibsodiumPath):
        libsodium = cdll.LoadLibrary(daedalusLibsodiumPath)
    elif path.exists(systemLibsodiumPath):
        libsodium = cdll.LoadLibrary(systemLibsodiumPath)
    else:
        exit(f'Unable to find libsodium, checked the following paths: {", ".join([daedalusLibsodiumPath, systemLibsodiumPath])}')
libsodium.sodium_init()
################################################## ###

### Blockchain Genesis Parameters ###
GenesisParam = kp.get_genesis()

epochLength = int(GenesisParam[0]["epochlength"])
activeSlotCoeff = float(GenesisParam[0]["activeslotcoeff"])
slotLength = int(GenesisParam[0]["slotlength"])

### Epoch 211 First Slot ###
firstShelleySlot = kp.get_block_info("33a28456a44277cbfb3457082467e56f16554932eb2a9eb7ceca97740bd4f4db")
firstSlot = firstShelleySlot[0]["abs_slot"]



### calculate first slot of target epoch ###
firstSlotOfEpoch = (firstSlot) + (epoch - 211) * (epochLength)

from decimal import *
getcontext().prec = 9
getcontext().rounding = ROUND_HALF_UP

def mkSeed(slot, eta0):
    h = hashlib.blake2b(digest_size=32)
    h.update(slot.to_bytes(8, byteorder='big') + binascii.unhexlify(eta0))
    slotToSeedBytes = h.digest()

    return slotToSeedBytes


def vrfEvalCertified(seed, praosCanBeLeaderSignKeyVRF):
    if isinstance(seed, bytes) and isinstance(praosCanBeLeaderSignKeyVRF,
                                              bytes):
        proof = create_string_buffer(
            libsodium.crypto_vrf_ietfdraft03_proofbytes())
        libsodium.crypto_vrf_prove(proof, praosCanBeLeaderSignKeyVRF, seed,
                                   len(seed))
        proofHash = create_string_buffer(libsodium.crypto_vrf_outputbytes())
        libsodium.crypto_vrf_proof_to_hash(proofHash, proof)

        return proofHash.raw
    else:
        print("error.  Feed me bytes")
        exit()


def vrfLeaderValue(vrfCert):
    h = hashlib.blake2b(digest_size=32)
    h.update(str.encode("L"))
    h.update(vrfCert)
    vrfLeaderValueBytes = h.digest()

    return int.from_bytes(vrfLeaderValueBytes, byteorder="big", signed=False)


def isOverlaySlot(firstSlotOfEpoch, currentSlot, decentralizationParam):
    diff_slot = float(currentSlot - firstSlotOfEpoch)
    left = Decimal(diff_slot) * Decimal(decentralizationParam)
    right = Decimal(diff_slot + 1) * Decimal(decentralizationParam)
    if math.ceil(left) < math.ceil(right):
        return True
    return False


# Determine if our pool is a slot leader for this given slot
# @param slot The slot to check
# @param activeSlotsCoeff The activeSlotsCoeff value from protocol params
# @param sigma The controlled stake proportion for the pool
# @param eta0 The epoch nonce value
# @param poolVrfSkey The vrf signing key for the pool


def isSlotLeader(slot, activeSlotsCoeff, sigma, eta0, poolVrfSkey):
    seed = mkSeed(slot, eta0)
    praosCanBeLeaderSignKeyVRFb = binascii.unhexlify(poolVrfSkey)
    cert = vrfEvalCertified(seed, praosCanBeLeaderSignKeyVRFb)
    certLeaderVrf = vrfLeaderValue(cert)
    certNatMax = math.pow(2, 256)
    denominator = certNatMax - certLeaderVrf
    q = certNatMax / denominator
    c = math.log(1.0 - activeSlotsCoeff)
    sigmaOfF = math.exp(-sigma * c)

    return q <= sigmaOfF

slotcount=0

for slot in range(firstSlotOfEpoch,epochLength+firstSlotOfEpoch):

    slotLeader = isSlotLeader(slot, activeSlotCoeff, sigma, eta0, poolVrfSkey)

    seed = mkSeed(slot, eta0)
    praosCanBeLeaderSignKeyVRFb = binascii.unhexlify(poolVrfSkey)
    cert = vrfEvalCertified(seed,praosCanBeLeaderSignKeyVRFb)
    certLeaderVrf = vrfLeaderValue(cert)
    certNatMax = math.pow(2,256)
    denominator = certNatMax - certLeaderVrf
    q = certNatMax / denominator
    c = math.log(1.0 - activeSlotCoeff)
    sigmaOfF = math.exp(-sigma * c)

    if slotLeader:
        pass
        timestamp = datetime.fromtimestamp(slot + 1591566291, tz=local_tz)
        slotcount+=1

        print("Epoch: " + str(epoch) + " - Local Time: " + str(timestamp.strftime('%Y-%m-%d %H:%M:%S') + " - Slot: " + str(slot-firstSlotOfEpoch) + "  - Block: " + str(slotcount)))

print()
print("Total Scheduled Blocks: " + str(slotcount))


### Epoch Assigned Performance or Luck ###

blocksEpoch = 21600

nStake = nStake.replace(',','')
pStake = pStake.replace(',','')

nStake = float(nStake)
pStake = float(pStake)

nStake = math.trunc(nStake)
pStake = math.trunc(pStake)

EpochLuck = int(100 * slotcount) / (blocksEpoch * pStake / nStake)

print()
print(f'Assigned Epoch Performance: ' + str(format(EpochLuck, ".2f")) + ' %' )


if slotcount == 0:
    print()
    print("No SlotLeader Schedules Found for Epoch: " +str(epoch))
    exit
