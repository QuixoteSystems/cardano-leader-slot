#!/bin/env python3

import requests
import urllib.request
import math
import binascii
import json
from tzlocal import get_localzone
import hashlib
import re
import readchar
from ctypes import *
from os import system, path
from datetime import datetime, timezone
from sys import exit, platform
from decimal import *
import koios_python as kp

try:
    import pyfiglet
except:
    pass

### Set These Variables -------------------------------------------###

pool_ticker = "YOUR_POOL_TICKER"
vrf_key_file = ('YOUR_VRF_FILE_PATH')
pool_id_bech32 = "YOUR_POOL_ID:_pool1..."

### -------------------------------------------------------------- ###
 
class col:
    red = '\033[31m'
    green = '\033[92m'
    endcl = '\033[0m'

def ClearScreen():
    command ='clear'
    system(command)

### Get your machine timezone -----------------------------------------###
local_tz = get_localzone()

### ADA Unicode symbol and Lovelaces removal ###
ada = " \u20B3"
lovelaces = 1000000


### Get Next Epoch Nonce from Koios ###
try:
    # Current Epoch
    epoch_param = kp.get_tip()
    epoch = epoch_param[0]["epoch_no"]
    net_stake_param = kp.get_epoch_params(epoch)
    eta0 =  net_stake_param[0]["nonce"]

    # Next Epoch
    next_epoch_parameters = kp.get_pool_stake_snapshot(pool_id_bech32)
    next_epoch = next_epoch_parameters[2]["epoch_no"]
    next_eta0 = next_epoch_parameters[2]["nonce"]

    ErrorMsg = None

    if next_eta0 is None :
        msg = str(col.red + '(New Nonce Not Avaliable Yet)')

    if next_eta0 is not None :
        msg = str(col.green + '(Next Epoch Nonce Available)')

    if eta0 == next_eta0:
        msg = str(col.red + '(Next Epoch Not Nonce Yet)')

except OSError as ErrorMsg:
    msg = str(col.red + '(Failed to establish connection to nonce.armada-alliance.com)')


### User Prompt Menu to select what kind of Epochs you want to know
print()
print()

### Figlet Fancy Welcome Header
try:
    cardano = pyfiglet.figlet_format("  Cardano")
    leader_slot = pyfiglet.figlet_format("  Leader Slot")

    print(col.green + cardano)
    print(col.green + leader_slot)
except:
    pass

print(col.green + '  Welcome to Light Leader Slot Script for Cardano SPOs. ')
print()
print(col.green + '  Check Assigned Blocks in Next, Current and Previous Cardano Epochs.')
print(col.endcl)
#print(col.green + f'Current Epoch: ' + col.endcl +str(current_epoch))

print(col.endcl)
print(f'  Press (n) to Check Next Epoch {str(msg)}')
print(col.endcl)
print('  Press (c) to Check Current Epoch')
print(col.endcl)
print('  Press (p) to Check Previous Epoch')
print(col.endcl)

print(f'  (any key) to Exit')
print(col.endcl)

### Read Keyboard keys ###
key = readchar.readkey()

def print_epoch_menu():
    '''
    Print Menu to show Pool and Epoch data
    '''
    print()
    print('  Checking SlotLeader Schedules for Stakepool: ' + (col.green + pool_ticker + col.endcl))
    print()
    print('  Pool Id: ' + (col.green + pool_id_bech32 + col.endcl))
    print()
    print('  Epoch: ' + col.green + str(epoch) + col.endcl)
    print()
    print('  Nonce: ' + col.green + str(eta0) + col.endcl)
    print()
    print('  Network Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(n_stake) + col.endcl + ada + col.endcl)
    print()
    print('  Pool Active Stake in Epoch ' + str(epoch) + ": " + col.green + str(p_stake) + col.endcl + ada + col.endcl)
    print()


### NEXT EPOCH. Get data from Koios ###
if key == 'n':

    ClearScreen()

    epoch_parameters = kp.get_pool_stake_snapshot(pool_id_bech32)
    epoch = epoch_parameters[2]["epoch_no"]
    next_eta0 = epoch_parameters[2]["nonce"]
    current_epoch = epoch_parameters[1]["epoch_no"]
    # Old parameters from Armada
    #epoch_parameters = kp.get_tip()
    #epoch = epoch_parameters[0]["epoch_no"]
    #epoch = int(next_epoch)
    #current_epoch = epoch - 1

    eta0= next_eta0
    n_stake = epoch_parameters[2]["active_stake"]

    poolStakeParam = kp.get_pool_info(pool_id_bech32)
    p_stake = next_epoch_parameters[2]["pool_stake"]

    sigma = float(p_stake) / float(n_stake)

    print_epoch_menu()



### PREVIUOS EPOCH. Get data from Koios ###
if key == 'p':

    ClearScreen()
    print()
    epoch = input("  Enter Epoch Previous Number: " + col.green)
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

    print_epoch_menu()



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

    print_epoch_menu()


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
        exit(f' Unable to find libsodium, checked the following paths: {", ".join([daedalusLibsodiumPath, systemLibsodiumPath])}')
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

getcontext().prec = 9
getcontext().rounding = ROUND_HALF_UP

def mk_seed(slot, eta0):

    if eta0 == None:
        print(str(col.red + 'New Nonce Not Avaliable Yet. It can not check assigned blocks for Next Epoch'))
        exit()

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
        print("  Error.  Feed me bytes")
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
    '''
    Calculate and print the Epoch performance
    '''
    blocks_epoch = 21600

    n_stake = n_stake.replace(',','')
    p_stake = p_stake.replace(',','')

    n_stake = float(n_stake)
    p_stake = float(p_stake)

    n_stake = math.trunc(n_stake)
    p_stake = math.trunc(p_stake)

    epoch_luck = int(100 * slot_count) / (blocks_epoch * p_stake / n_stake)

    print()
    print(f'  Assigned Epoch Performance: ' + str(format(epoch_luck, ".2f")) + ' %' )
    print()

    if slot_count == 0:
        print()
        print("  No SlotLeader Schedules Found for Epoch: " +str(epoch))
        print()
        exit


def get_blocks(slot_count):
    '''
    Count and print Blocks Epoch output
    '''
    if slotLeader:
        timestamp = datetime.fromtimestamp(slot + 1591566291, tz=local_tz)
        slot_count+=1
        print("  Epoch: " + str(epoch) + " - Local Time: " + str(timestamp.strftime('%d-%m-%Y %H:%M:%S') + " - Slot: " + str(slot-firstSlotOfEpoch) + "  - Block: " + str(slot_count)))
    return slot_count


# Determine if our pool is a slot leader for this given slot
# @param slot The slot to check
# @param activeSlotsCoeff The activeSlotsCoeff value from protocol params
# @param sigma The controlled stake proportion for the pool
# @param eta0 The epoch nonce value
# @param pool_vrf_skey The vrf signing key for the pool

### For Epochs inside Praos Time ###
if float(epoch) >= 365:
    def is_slot_leader(slot, activeSlotsCoeff, sigma, eta0, pool_vrf_skey):
        '''
        Check and calculate if Pool is leader in a certain slot
        '''
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

    slot_count=0

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

        slot_count = get_blocks(slot_count)

    print()
    print("  Total Scheduled Blocks: " + str(slot_count))

    get_performance(n_stake, p_stake)


### For OLD Epochs inside TPraos Time (before Current Ouroboros Praos) ###
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
            print("Error.  Feed me bytes")
            exit()

    # Determine if our pool is a slot leader for this given slot
    # @param slot The slot to check
    # @param activeSlotCoeff The activeSlotsCoeff value from protocol params
    # @param sigma The controlled stake proportion for the pool
    # @param eta0 The epoch nonce value
    # @param pool_vrf_skey The vrf signing key for the pool

    def isSlotLeader(slot,activeSlotCoeff,sigma,eta0,pool_vrf_skey):
        '''
        Check and calculate if Pool is leader in a certain slot
        '''
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
    slot_count=0
    for slot in range(firstSlotOfEpoch,epochLength+firstSlotOfEpoch):
        slotLeader = isSlotLeader(slot, activeSlotCoeff, sigma, eta0, pool_vrf_skey)
        slot_count = get_blocks(slot_count)

    print()
    print("  Total Scheduled Blocks: " + str(slot_count))

    get_performance(n_stake, p_stake)

