#!/usr/bin/python3

import datetime as dt
import logging

from gpsdclient import GPSDClient


def get_gpsd_position():
	"""Get latitude and longitude from GPSD."""
	logging.info("Trying to figure out position using GPS")
	try:
		with GPSDClient(
			host='localhost',
			port=2947,
			timeout=15,
		) as client:
			for result in client.json_stream(filter=["TPV"]):
				if result["class"] == "TPV":
					logging.info("GPS 3D fix acquired")
					utc = result.get("time", dt.datetime.now(dt.timezone.utc))
					lat = result.get("lat", 0)
					lon = result.get("lon", 0)
					alt = result.get("alt", 0)
					if lat != 0 and lon != 0 and alt != 0:
						logging.info(
							"%s | GPS Position: %s, %s, %s", utc, lat, lon, alt
						)
					print(utc, lat, lon, alt)
				else:
					logging.info("GPS Position not available yet")
	except Exception as e:
		logging.error("Error getting GPS data: %s", e)


def get_gpsd_sat():
	"""Get satellite used from GPSD."""
	logging.info("Trying to figure out satellite used using GPS")
	try:
		with GPSDClient(
			host='localhost',
			port=2947,
			timeout=15,
		) as client:
			for result in client.json_stream(filter=["SKY"]):
				if result["class"] == "SKY":
					logging.info("GPS satellite acquired")
					uSat = result.get("uSat", 0)
					nSat = result.get("nSat", 0)
					print(uSat, nSat)
				else:
					logging.info("GPS satellite not available yet")
	except Exception as e:
		logging.error("Error getting GPS data: %s", e)


if __name__ == "__main__":
	get_gpsd_position()
	get_gpsd_sat()