"""
Contains all the variables related to the PM sensor based on its datasheet
"""
    
mean10sec= b'\x81\x31\x4E'
mean1min = b'\x81\x32\x4D'
mean5min = b'\x81\x33\x4C'
temp_hum= b'\x81\x14\x6B'
power_on = b'\x81\x15\x6A'
find_power_state = b'\x81\x16\x6A'
sen_state = b'\x81\x16\x69'
vers = b'\x81\x17\x68'

status_table = {
    0: 'N/A',
    1: 'Sleep State',
    2: 'Degraded State',
    3: 'Not Ready',
    4: 'Heat Error',
    5: 'T/RH Error',
    6: 'Fan Error',
    7: 'Memory Error',
    8: 'Laser Error'}