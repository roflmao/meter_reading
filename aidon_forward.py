#!/usr/bin/python

import serial, time, sys, argparse
from hass_influx import *
from aidon_obis import *

parser = argparse.ArgumentParser(description='Forward Aidon data to Home Assistant and InfluxDB')
parser.add_argument('serial_port')
parser.add_argument('--hass_host')
parser.add_argument('--hass_token')
args = parser.parse_args()

# Class used to forward data to Home Assistant
hi = hass_influx(
	hass_host=args.hass_host,
	hass_token=args.hass_token)

ser = serial.Serial(args.serial_port, 2400, timeout=0.05, parity=serial.PARITY_EVEN)

def aidon_callback(fields):
	ts = time.time()

	if 'p_act_in' in fields:
		hi.post("aidon", "power", "%.03f" % (fields['p_act_in']), hass_name="Effekt", hass_unit="W", ts=ts)

	if 'energy_act_in' in fields:
		hi.post("aidon", "energy", "%.02f" % fields['energy_act_in'], hass_name="Energi", hass_unit="kWh", ts=ts)

a = aidon(aidon_callback)
				
while(1):
	while ser.inWaiting():
		a.decode(ser.read(1))
	time.sleep(0.01)

