#!/usr/bin/python3

import datetime as dt
import logging

from gpsdclient import GPSDClient

logging.basicConfig(
	format="%(asctime)s %(levelname)s: %(message)s",
	datefmt="%Y-%m-%dT%H:%M:%S",
	level=logging.INFO,
)


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
					logging.info("GPS fix acquired")
					utc = result.get("time", dt.datetime.now(dt.timezone.utc))
					lat = float(result.get("lat", 0))
					lon = float(result.get("lon", 0))
					alt = float(result.get("alt", 0))
					if lat != 0 and lon != 0 and alt != 0:
						logging.info(
							"%s | GPS Position: %s, %s, %s", utc, lat, lon, alt
						)
					print(utc, lat, lon, alt)
				else:
					logging.info("GPS Position unavailable")
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
					logging.info("GPS Satellite acquired")
					uSat = int(result.get("uSat", 0))
					nSat = int(result.get("nSat", 0))
					print(uSat, nSat)
				else:
					logging.info("GPS Satellite unavailable")
	except Exception as e:
		logging.error("Error getting GPS data: %s", e)


if __name__ == "__main__":
	get_gpsd_position()
	get_gpsd_sat()
