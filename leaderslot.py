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
pool_ticker = "YOUT_POOL_TICKER"
vrf_key_file = ('YOUR_VRF_FILE_PATH')
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
print(f'(p) to Check Previous Epochs')
print(col.endcl)

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
    n_stake = epoch_info[0]["active_stake"]

    poolStakeParam = kp.get_pool_info(pool_id_bech32)
    p_stake = poolStakeParam[0]["active_stake"]

    sigma = float(p_stake) / float(n_stake)

    print()
    print(f'Checking SlotLeader Schedules for Stakepool: ' + (col.green + pool_ticker + col.endcl))
    print()
    print(f'Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print(f'Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print(f'Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print(f'Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(n_stake) + col.endcl + ada + col.endcl)
    print()
    print(f'Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(p_stake) + col.endcl + ada + col.endcl)
    print()

### CURRENT PREVIUOS. Get data from Koios ###

if key == 'p':

    ClearScreen()
    print()
    epoch = input("Enter Epoch Previous Number: " + col.green)
    print(col.endcl)

    epoch_param = kp.get_epoch_info(epoch)
    epoch = epoch_param[0]["epoch_no"]

    net_stake_param = kp.get_epoch_params(epoch)
    eta0 =  net_stake_param[0]["nonce"]

    epoch_info = kp.get_epoch_info(epoch)
    n_stake = epoch_info[0]["active_stake"]

    pool_stake_param = kp.get_pool_info(pool_id_bech32)
    p_stake = pool_stake_param[0]["active_stake"]

    sigma = float(p_stake) / float(n_stake)


    print()
    print(f'Checking SlotLeader Schedules for Stakepool: ' + (col.green + pool_ticker + col.endcl))
    print()
    print(f'Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print(f'Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print(f'Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print(f'Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(n_stake) + col.endcl + ada + col.endcl)
    print()
    print(f'Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(p_stake) + col.endcl + ada + col.endcl)
    print()


### CURRENT EPOCH. Get data from Koios ###

if key == 'c':

    ClearScreen()

    epoch_param = kp.get_tip()
    epoch = epoch_param[0]["epoch_no"]

    net_stake_param = kp.get_epoch_params(epoch)
    eta0 =  net_stake_param[0]["nonce"]

    epoch_info = kp.get_epoch_info(epoch)
    n_stake = epoch_info[0]["active_stake"]

    pool_stake_param = kp.get_pool_info(pool_id_bech32)
    p_stake = pool_stake_param[0]["active_stake"]

    sigma = float(p_stake) / float(n_stake)


    print()
    print(f'Checking SlotLeader Schedules for Stakepool: ' + (col.green + pool_ticker + col.endcl))
    print()
    print(f'Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print(f'Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print(f'Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print(f'Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(n_stake) + col.endcl + ada + col.endcl)
    print()
    print(f'Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(p_stake) + col.endcl + ada + col.endcl)
    print()


### ############### ###
if(key != 'p') and (key != 'c') and (key != 'n'):
    exit(0)

######################################
####### Calculate Slots Leader ######
#####################################

### Opening vrf.skey file ###
with open(vrf_key_file) as f:
        skey = json.load(f)
        pool_vrf_skey = skey['cborHex'][4:]

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



### Calculate first slot of target Epoch ###
firstSlotOfEpoch = (firstSlot) + (epoch - 211) * (epochLength)

from decimal import *
getcontext().prec = 9
getcontext().rounding = ROUND_HALF_UP

def mk_seed(slot, eta0):
    h = hashlib.blake2b(digest_size=32)
    h.update(slot.to_bytes(8, byteorder='big') + binascii.unhexlify(eta0))
    slotToSeedBytes = h.digest()

    return slotToSeedBytes


def vrf_eval_certified(seed, praosCanBeLeaderSignKeyVRF):
    if isinstance(seed, bytes) and isinstance(praosCanBeLeaderSignKeyVRF, bytes):
        proof = create_string_buffer(libsodium.crypto_vrf_ietfdraft03_proofbytes())
        libsodium.crypto_vrf_prove(proof, praosCanBeLeaderSignKeyVRF, seed, len(seed))
        proof_hash = create_string_buffer(libsodium.crypto_vrf_outputbytes())
        libsodium.crypto_vrf_proof_to_hash(proof_hash, proof)

        return proof_hash.raw
    else:
        print("Error.  Feed me bytes")
        exit()


def vrf_leader_value(vrfCert):
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


### Epoch Assigned Performance or Luck ###
def get_performance(n_stake, p_stake):
    blocksEpoch = 21600

    n_stake = n_stake.replace(',','')
    p_stake = p_stake.replace(',','')

    n_stake = float(n_stake)
    p_stake = float(p_stake)

    n_stake = math.trunc(n_stake)
    p_stake = math.trunc(p_stake)

    epoch_luck = int(100 * slotcount) / (blocksEpoch * p_stake / n_stake)

    print()
    print(f'Assigned Epoch Performance: ' + str(format(epoch_luck, ".2f")) + ' %' )


    if slotcount == 0:
        print()
        print("No SlotLeader Schedules Found for Epoch: " +str(epoch))
        exit

# Determine if our pool is a slot leader for this given slot
# @param slot The slot to check
# @param activeSlotsCoeff The activeSlotsCoeff value from protocol params
# @param sigma The controlled stake proportion for the pool
# @param eta0 The epoch nonce value
# @param pool_vrf_skey The vrf signing key for the pool

### For Epochs inside Praos Time ###
if float(epoch) >= 364:
    def is_slot_leader(slot, activeSlotsCoeff, sigma, eta0, pool_vrf_skey):
        seed = mk_seed(slot, eta0)
        praosCanBeLeaderSignKeyVRFb = binascii.unhexlify(pool_vrf_skey)
        cert = vrf_eval_certified(seed, praosCanBeLeaderSignKeyVRFb)
        certLeaderVrf = vrf_leader_value(cert)
        certNatMax = math.pow(2, 256)
        denominator = certNatMax - certLeaderVrf
        q = certNatMax / denominator
        c = math.log(1.0 - activeSlotsCoeff)
        sigmaOfF = math.exp(-sigma * c)

        return q <= sigmaOfF

    slotcount=0

    for slot in range(firstSlotOfEpoch,epochLength+firstSlotOfEpoch):

        slotLeader = is_slot_leader(slot, activeSlotCoeff, sigma, eta0, pool_vrf_skey)

        seed = mk_seed(slot, eta0)
        praosCanBeLeaderSignKeyVRFb = binascii.unhexlify(pool_vrf_skey)
        cert = vrf_eval_certified(seed,praosCanBeLeaderSignKeyVRFb)
        certLeaderVrf = vrf_leader_value(cert)
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

    get_performance(n_stake, p_stake)


### For old Epochs inside TPraos Time (before Current Ouroboros Praos) ###
else:
    def mkSeed(slot, eta0):
        h = hashlib.blake2b(digest_size=32)
        h.update(bytearray([0,0,0,0,0,0,0,1])) #neutral nonce
        seedLbytes=h.digest()
        h = hashlib.blake2b(digest_size=32)
        h.update(slot.to_bytes(8,byteorder='big') + binascii.unhexlify(eta0))
        slotToSeedBytes = h.digest()
        seed = [x ^ slotToSeedBytes[i] for i,x in enumerate(seedLbytes)]
        return bytes(seed)

    def vrfEvalCertified(seed, tpraosCanBeLeaderSignKeyVRF):
        if isinstance(seed, bytes) and isinstance(tpraosCanBeLeaderSignKeyVRF, bytes):
            proof = create_string_buffer(libsodium.crypto_vrf_ietfdraft03_proofbytes())
            libsodium.crypto_vrf_prove(proof, tpraosCanBeLeaderSignKeyVRF,seed, len(seed))
            proofHash = create_string_buffer(libsodium.crypto_vrf_outputbytes())
            libsodium.crypto_vrf_proof_to_hash(proofHash,proof)
            return proofHash.raw
        else:
            print("error.  Feed me bytes")
            exit()

    # Determine if our pool is a slot leader for this given slot
    # @param slot The slot to check
    # @param activeSlotCoeff The activeSlotsCoeff value from protocol params
    # @param sigma The controlled stake proportion for the pool
    # @param eta0 The epoch nonce value
    # @param pool_vrf_skey The vrf signing key for the pool

    def isSlotLeader(slot,activeSlotCoeff,sigma,eta0,pool_vrf_skey):
        seed = mkSeed(slot, eta0)
        tpraosCanBeLeaderSignKeyVRFb = binascii.unhexlify(pool_vrf_skey)
        cert=vrfEvalCertified(seed,tpraosCanBeLeaderSignKeyVRFb)
        certNat  = int.from_bytes(cert, byteorder="big", signed=False)
        certNatMax = math.pow(2,512)
        denominator = certNatMax - certNat
        q = certNatMax / denominator
        c = math.log(1.0 - activeSlotCoeff)
        sigmaOfF = math.exp(-sigma * c)
        return q <= sigmaOfF
    slotcount=0
    for slot in range(firstSlotOfEpoch,epochLength+firstSlotOfEpoch):
        slotLeader = isSlotLeader(slot, activeSlotCoeff, sigma, eta0, pool_vrf_skey)
        if slotLeader:
            pass
            timestamp = datetime.fromtimestamp(slot + 1591566291, tz=local_tz)
            slotcount+=1
            print("Epoch: " + str(epoch) + " - Local Time: " + str(timestamp.strftime('%Y-%m-%d %H:%M:%S') + " - Slot: " + str(slot-firstSlotOfEpoch) + "  - Block: " + str(slotcount)))
    print()
    print("Total Scheduled Blocks: " + str(slotcount))

    get_performance(n_stake, p_stake)

