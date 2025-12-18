#!/usr/bin/python3

"""RasPiAPRS: Send APRS position and telemetry from Raspberry Pi to APRS-IS."""

import asyncio
import datetime as dt
import json
import logging
import os
import random
import subprocess
import sys
import time
from urllib.request import urlopen

import aprslib
import dotenv
import humanize
import telegram
from aprslib.exceptions import ConnectionError as APRSConnectionError
from dotenv import set_key
from gpsdclient import GPSDClient

# Default paths for system files
CPUINFO_FILE = "/proc/cpuinfo"
LOADAVG_FILE = "/proc/loadavg"
MEMINFO_FILE = "/proc/meminfo"
UPTIME_FILE = "/proc/uptime"
VERSION_FILE = "/proc/version"
THERMAL_FILE = "/sys/class/thermal/thermal_zone0/temp"
OS_RELEASE_FILE = "/etc/os-release"
PISTAR_RELEASE_FILE = "/etc/pistar-release"
WPSD_RELEASE_FILE = "/etc/WPSD-release"
MMDVMHOST_FILE = "/etc/mmdvmhost"
MMDVMLOGPATH = "/var/log/pi-star"
MMDVMLOGPREFIX = "MMDVM"
DMRGATEWAYLOGPREFIX = "DMRGateway"


# Set up logging
def configure_logging():
	logging.basicConfig(
		level=logging.INFO,
		datefmt="%Y-%m-%dT%H:%M:%S",
		format="%(asctime)s - %(levelname)s - %(message)s",
	)


# Configuration class to handle settings
class Config(object):
	"""Class to handle configuration settings."""

	def __init__(self):
		dotenv.load_dotenv(".env")

		call = os.getenv("APRS_CALL", "N0CALL")
		ssid = os.getenv("APRS_SSID", "0")
		self.call = f"{call}-{ssid}"
		self.sleep = int(os.getenv("SLEEP", 600))
		self.symbol_table = os.getenv("APRS_SYMBOL_TABLE", "/")
		self.symbol = os.getenv("APRS_SYMBOL", "n")

		lat = os.getenv("APRS_LATITUDE", "0.0")
		lon = os.getenv("APRS_LONGITUDE", "0.0")
		alt = os.getenv("APRS_ALTITUDE", "0.0")

		if os.getenv("GPSD_ENABLE"):
			self.latitude, self.longitude, self.altitude = get_gpsd_position()
		else:
			if lat == "0.0" and lon == "0.0":
				self.latitude, self.longitude = get_coordinates()
				self.altitude = alt
			else:
				self.latitude, self.longitude, self.altitude = lat, lon, alt
		self.server = os.getenv("APRSIS_SERVER", "rotate.aprs2.net")
		self.port = int(os.getenv("APRSIS_PORT", 14580))
		self.filter = os.getenv("APRSIS_FILTER", "m/50")

		passcode = os.getenv("APRS_PASSCODE")
		if passcode:
			self.passcode = passcode
		else:
			logging.warning("Generating passcode")
			self.passcode = aprslib.passcode(call)

	def __repr__(self):
		return ("<Config> call: {0.call}, passcode: {0.passcode} - {0.latitude}/{0.longitude}/{0.altitude}").format(self)

	@property
	def call(self):
		return self._call

	@call.setter
	def call(self, val):
		self._call = str(val)

	@property
	def sleep(self):
		return self._sleep

	@sleep.setter
	def sleep(self, val):
		try:
			self._sleep = int(val)
		except ValueError:
			logging.warning("Sleep value error, using 600")
			self._sleep = 600

	@property
	def latitude(self):
		return self._latitude

	@latitude.setter
	def latitude(self, val):
		self._latitude = val

	@property
	def longitude(self):
		return self._longitude

	@longitude.setter
	def longitude(self, val):
		self._longitude = val

	@property
	def altitude(self):
		return self._altitude

	@altitude.setter
	def altitude(self, val):
		self._altitude = val

	@property
	def symbol(self):
		return self._symbol

	@symbol.setter
	def symbol(self, val):
		self._symbol = str(val)

	@property
	def symbol_table(self):
		return self._symbol_table

	@symbol_table.setter
	def symbol_table(self, val):
		self._symbol_table = str(val)

	@property
	def server(self):
		return self._server

	@server.setter
	def server(self, val):
		self._server = str(val)

	@property
	def port(self):
		return self._port

	@port.setter
	def port(self, val):
		try:
			self._port = int(val)
		except ValueError:
			logging.warning("Port value error, using 14580")
			self._port = 14580

	@property
	def passcode(self):
		return self._passcode

	@passcode.setter
	def passcode(self, val):
		self._passcode = str(val)


class Sequence(object):
	"""Class to manage APRS sequence numbers."""
	_count = 0

	def __init__(self):
		self.sequence_file = os.path.join("/tmp", "raspiaprs.seq")
		try:
			with open(self.sequence_file) as fds:
				self._count = int(fds.readline())
		except (IOError, ValueError):
			self._count = 0

	def flush(self):
		try:
			with open(self.sequence_file, "w") as fds:
				fds.write("{0:d}".format(self._count))
		except IOError:
			pass

	def __iter__(self):
		return self

	def next(self):
		return self.__next__()

	def __next__(self):
		self._count = (1 + self._count) % 999
		self.flush()
		return self._count


def get_gpsd_position():
	"""Get position from GPSD."""
	if os.getenv("GPSD_ENABLE"):
		logging.info("Trying to figure out position using GPS")
		try:
			with GPSDClient(os.getenv("GPSD_HOST", "localhost"), int(os.getenv("GPSD_PORT", 2947)), 15) as client:
				for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
					if result["class"] == "TPV":
						logging.info("GPS fix acquired")
						utc = result.get("time", dt.datetime.now(dt.timezone.utc))
						lat = result.get("lat", 0)
						lon = result.get("lon", 0)
						alt = result.get("alt", 0)
						# acc = result.get("sep", 0)
						if lat != 0 and lon != 0 and alt != 0:
							logging.info("%s | GPS Position: %s, %s, %s", utc, lat, lon, alt)
							set_key(".env", "APRS_LATITUDE", lat, quote_mode="never")
							set_key(".env", "APRS_LONGITUDE", lon, quote_mode="never")
							set_key(".env", "APRS_ALTITUDE", alt, quote_mode="never")
							Config.latitude = lat
							Config.longitude = lon
							Config.altitude = alt
							return lat, lon, alt
					else:
						logging.info("GPS Position unavailable")
						return (0, 0, 0)
		except Exception as e:
			logging.error("Error getting GPS data: %s", e)
			return (0, 0, 0)


def get_gpsd_sat():
	"""Get satellite from GPSD."""
	if os.getenv("GPSD_ENABLE"):
		logging.info("Trying to figure out satellite using GPS")
		try:
			with GPSDClient(os.getenv("GPSD_HOST", "localhost"), int(os.getenv("GPSD_PORT", 2947)), 15) as client:
				for result in client.dict_stream(convert_datetime=True, filter=["SKY"]):
					if result["class"] == "SKY":
						logging.info("GPS Satellite acquired")
						uSat = result.get("uSat", 0)
						nSat = result.get("nSat", 0)
						return uSat, nSat
					else:
						logging.info("GPS Satellite unavailable")
						return (0, 0)
		except Exception as e:
			logging.error("Error getting GPS data: %s", e)
			return (0, 0)


def get_coordinates():
	"""Get approximate latitude and longitude using IP address lookup."""
	logging.info("Trying to figure out the coordinate using your IP address")
	url = "http://ip-api.com/json/"
	try:
		with urlopen(url) as response:
			_data = response.read()
			data = json.loads(_data.decode())
	except Exception as err:
		logging.error("Failed to fetch coordinates from %s: %s", url, err)
		return (0, 0)
	else:
		try:
			logging.info("IP-Position: %f, %f", data["lat"], data["lon"])
			return data["lat"], data["lon"]
		except (KeyError, TypeError) as err:
			logging.error("Unexpected response format: %s", err)
			return (0, 0)


def get_cpuload():
	"""Get CPU load as a percentage of total capacity."""
	try:
		with open(LOADAVG_FILE) as lfd:
			loadstr = lfd.readline()
		load5 = float(loadstr.split()[1])
		corecount = os.cpu_count()
		return int((load5 / corecount) * 1000)
	except Exception as e:
		logging.error("Unexpected error: %s", e)
		return 0


def get_memused():
	"""Get used memory in MB."""
	try:
		with open(MEMINFO_FILE) as pfd:
			for line in pfd:
				if line.startswith("MemTotal"):
					parts = line.split()
					if len(parts) > 1:
						totalmem = int(parts[1])
				if line.startswith("MemFree"):
					parts = line.split()
					if len(parts) > 1:
						freemem = int(parts[1])
				if line.startswith("Buffers"):
					parts = line.split()
					if len(parts) > 1:
						buffmem = int(parts[1])
				if line.startswith("Cached"):
					parts = line.split()
					if len(parts) > 1:
						cachemem = int(parts[1])
		return int((totalmem - freemem - buffmem - cachemem) / 100)
	except Exception as e:
		logging.error("Unexpected error: %s", e)
		return 0


def get_diskused():
	"""Get used disk space in GB."""
	try:
		diskused = subprocess.check_output(["df --block-size=1 /", "|", "tail -1", "|", "awk {'print $3'}"], text=True).strip()
		return int(diskused / 1024 / 1024 / 1024) * 10
	except Exception as e:
		logging.error("Unexpected error: %s", e)
		return 0


def get_temp():
	"""Get CPU temperature in degC."""
	try:
		with open(THERMAL_FILE) as tfd:
			temperature = int(tfd.readline().strip())
		return int(temperature / 100)
	except Exception as e:
		logging.error("Unexpected error: %s", e)
		return 0


def get_osinfo():
	"""Get operating system information."""
	osname = ""
	try:
		with open(OS_RELEASE_FILE) as osr:
			for line in osr:
				if "ID_LIKE" in line:
					id_like = line.split("=", 1)[1].strip().title()
				if "DEBIAN_VERSION_FULL" in line:
					debian_version_full = line.split("=", 1)[1].strip()
				if "VERSION_CODENAME" in line:
					version_codename = line.split("=", 1)[1].strip()
			osname = f"{id_like} {debian_version_full} ({version_codename})"
	except (IOError, OSError):
		logging.warning("OS release file not found: %s", OS_RELEASE_FILE)
	kernelver = ""
	try:
		with open(VERSION_FILE) as ver:
			for line in ver:
				parts = line.split()
				if len(parts) >= 3:
					kernelver = f"[{parts[0]} {parts[2]} ({parts[4].removeprefix('(').split('-')[0]})]"
	except (IOError, IndexError):
		logging.warning("Version file not found or unexpected format: %s", VERSION_FILE)
	return f" {osname} {kernelver}"


def get_dmrmaster():
	"""Get connected DMR master from DMRGateway log files."""
	with open(MMDVMHOST_FILE, "r") as mmh:
		if "Enable=1" in mmh.read():
			log_dmrgw_previous = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log")
			log_dmrgw_now = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log")

			dmr_master: str = ""
			log_master_string = "Logged into the master successfully"
			log_ref_string = "XLX, Linking"
			# log_master_dc_string = "Closing DMR Network"
			master_line: list[str] = []
			# master_dc_line: list[str] = []
			ref_line: list[str] = []
			dmrmaster: list[str] = []
			dmrmasters: list[str] = []
			try:
				master_line = subprocess.check_output(["grep", log_master_string, log_dmrgw_now], text=True).splitlines()
				# master_dc_line = subprocess.check_output(["grep", log_master_dc_string, log_dmrgw_now], text=True).splitlines()
				ref_line = subprocess.check_output(["grep", log_ref_string, log_dmrgw_now], text=True).splitlines()
				ref_line = ref_line[-1:] if ref_line else []
			except subprocess.CalledProcessError:
				try:
					master_line = subprocess.check_output(["grep", log_master_string, log_dmrgw_previous], text=True).splitlines()
					# master_dc_line = subprocess.check_output(["grep", log_master_dc_string, log_dmrgw_previous], text=True).splitlines()
					ref_line = subprocess.check_output(["grep", log_ref_string, log_dmrgw_previous], text=True).splitlines()
					ref_line = ref_line[-1:] if ref_line else []
				except subprocess.CalledProcessError:
					pass
			master_line_count = len(master_line)
			# master_dc_line_count = len(master_dc_line)
			ref_line_count = len(ref_line)
			for mascount in range(master_line_count):
				master = master_line[mascount].split()[3].split(",")[0].replace("_", " ")
				if master == "XLX":
					for refcount in range(ref_line_count):
						master = f"{ref_line[refcount].split()[7]} {ref_line[refcount].split()[8]}"
				dmrmaster.append(master)
				# for dccount in range(master_dc_line_count):
				# 	 master_dc = master_dc_line[dccount].split()[3].split(",")[0]
				# 	 if master_dc == "XLX":
				# 		 xlxdcid = dmrmaster.index(re.search(r"^XLX.+", dmrmaster[dccount])[0])
				# 		 dmrmaster.pop(xlxdcid)
				# 	 dmrmaster.remove(master_dc)
			dmrmasters = list(dict.fromkeys(dmrmaster))
			if len(dmrmasters) > 0:
				dmr_master = f" connected via [{', '.join(dmrmasters)}]"
	return dmr_master


def get_uptime():
	"""Get system uptime in a human-readable format."""
	with open(UPTIME_FILE) as upf:
		uptime_seconds = float(upf.readline().split()[0])
		uptime = dt.timedelta(seconds=uptime_seconds)
	return f"up={humanize.precisedelta(uptime, minimum_unit='seconds', format='%0.0f')}"


def get_mmdvminfo():
	"""Get MMDVM configured frequency and color code."""
	rx_freq, tx_freq, color_code, dmr_enabled = 0, 0, 0, False
	with open(MMDVMHOST_FILE, "r") as mmh:
		for line in mmh:
			if line.startswith("RXFrequency="):
				rx_freq = int(line.strip().split("=")[1])
			elif line.startswith("TXFrequency="):
				tx_freq = int(line.strip().split("=")[1])
			elif line.startswith("ColorCode="):
				color_code = int(line.strip().split("=")[1])
			elif "[DMR]" in line:
				dmr_enabled = "Enable=1" in next(mmh, "")
	rx = round(rx_freq / 1000000, 6)
	tx = round(tx_freq / 1000000, 6)
	shift = ""
	if tx > rx:
		shift = f" ({round(rx - tx, 6)}MHz)"
	elif tx < rx:
		shift = f" (+{round(rx - tx, 6)}MHz)"
	cc = f" CC{color_code}" if dmr_enabled else ""
	return (str(tx) + "MHz" + shift + cc) + get_dmrmaster() + ","


async def logs_to_telegram(tg_message: str, lat: float=0, lon: float=0):
	"""Send log message to Telegram channel."""
	if os.getenv("TELEGRAM_ENABLE"):
		tgbot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
		async with tgbot:
			try:
				botmsg = await tgbot.send_message(
					chat_id=os.getenv("TELEGRAM_CHAT_ID"),
					message_thread_id=int(os.getenv("TELEGRAM_TOPIC_ID")),
					text=tg_message,
					parse_mode="HTML",
					link_preview_options={
						"is_disabled": True,
						"prefer_small_media": True,
						"show_above_text": True,
					},
				)
				logging.info("Sent message to Telegram: %s/%s/%s", botmsg.chat_id, botmsg.message_thread_id, botmsg.message_id)
				if lat != 0 and lon != 0:
					botloc = await tgbot.send_location(
						chat_id=os.getenv("TELEGRAM_CHAT_ID"),
						message_thread_id=int(os.getenv("TELEGRAM_TOPIC_ID")),
						latitude=lat,
						longitude=lon
					)
					logging.info("Sent location to Telegram: %s/%s/%s", botloc.chat_id, botloc.message_thread_id, botloc.message_id)
			except Exception as e:
				logging.error("Failed to send message to Telegram: %s", e)


async def send_position(ais, cfg, seq):
	"""Send APRS position packet to APRS-IS."""

	# Build a simple APRS uncompressed position packet string instead of relying on aprslib.packets
	def _lat_to_aprs(lat):
		ns = "N" if lat >= 0 else "S"
		lat = abs(lat)
		deg = int(lat)
		minutes = (lat - deg) * 60
		return f"{deg:02d}{minutes:05.2f}{ns}"

	def _lon_to_aprs(lon):
		ew = "E" if lon >= 0 else "W"
		lon = abs(lon)
		deg = int(lon)
		minutes = (lon - deg) * 60
		return f"{deg:03d}{minutes:05.2f}{ew}"

	def _alt_to_aprs(alt):
		alt /= 0.3048  # to feet
		alt = min(999999, alt)
		alt = max(-99999, alt)
		return "/A={0:06.0f}".format(alt)

	if os.getenv("GPSD_ENABLE"):
		cur_lat, cur_lon, cur_alt = get_gpsd_position()
		if cur_lat == 0 and cur_lon == 0 and cur_alt == 0:
			cur_lat = os.getenv("APRS_LATITUDE", cfg.latitude)
			cur_lon = os.getenv("APRS_LONGITUDE", cfg.longitude)
			cur_alt = os.getenv("APRS_ALTITUDE", cfg.altitude)
	else:
		cur_lat = os.getenv("APRS_LATITUDE", cfg.latitude)
		cur_lon = os.getenv("APRS_LONGITUDE", cfg.longitude)
		cur_alt = os.getenv("APRS_ALTITUDE", cfg.altitude)
	mmdvminfo = get_mmdvminfo()
	osinfo = get_osinfo()
	comment = f"{mmdvminfo}{osinfo} https://github.com/HafiziRuslan/RasPiAPRS"
	timestamp = dt.datetime.now(dt.timezone.utc).strftime("%d%H%Mz")
	latstr = _lat_to_aprs(float(cur_lat))
	lonstr = _lon_to_aprs(float(cur_lon))
	altstr = _alt_to_aprs(float(cur_alt))
	payload = f"/{timestamp}{latstr}{cfg.symbol_table}{lonstr}{cfg.symbol}{altstr}{comment}"
	packet = f"{cfg.call}>APP642:{payload}"
	await logs_to_telegram(f"<u>{cfg.call} Position-{seq}</u>\n\n<b>Time</b>: {timestamp}\n<b>Pos</b>:\n\t<b>Latitude</b>: {cur_lat}\n\t<b>Longitude</b>: {cur_lon}\n\t<b>Altitude</b>: {cur_alt}m\n<b>Comment</b>: {comment}", cur_lat, cur_lon)
	logging.info(packet)
	try:
		ais.sendall(packet)
	except APRSConnectionError as err:
		logging.warning(err)


def send_header(ais, cfg):
	"""Send APRS header information to APRS-IS."""
	try:
		if os.getenv("GPSD_ENABLE"):
			ais.sendall("{0}>APP642::{0:9s}:PARM.CPUTemp,CPULoad,RAMUsed,DiskUsed,GPSUsed".format(cfg.call))
			ais.sendall("{0}>APP642::{0:9s}:UNIT.degC,pcnt,MB,GB,sats".format(cfg.call))
			ais.sendall("{0}>APP642::{0:9s}:EQNS.0,0.1,0,0,0.1,0,0,0.1,0,0,0.1,0,0,1,0".format(cfg.call))
		else:
			ais.sendall("{0}>APP642::{0:9s}:PARM.CPUTemp,CPULoad,RAMUsed,DiskUsed".format(cfg.call))
			ais.sendall("{0}>APP642::{0:9s}:UNIT.degC,pcnt,MB,GB".format(cfg.call))
			ais.sendall("{0}>APP642::{0:9s}:EQNS.0,0.1,0,0,0.1,0,0,0.1,0,0,0.1,0".format(cfg.call))
	except APRSConnectionError as err:
		logging.warning(err)


def ais_connect(cfg):
	"""Establish connection to APRS-IS with retries."""
	logging.info("Connecting to APRS-IS server %s:%d as %s", cfg.server, cfg.port, cfg.call)
	ais = aprslib.IS(cfg.call, passwd=cfg.passcode, host=cfg.server, port=cfg.port)
	for _ in range(5):
		try:
			ais.connect()
		except APRSConnectionError as err:
			logging.warning(err)
			time.sleep(20)
		else:
			ais.set_filter(cfg.filter)
			return ais
	logging.error("Connection error, exiting")
	sys.exit(getattr(os, "EX_NOHOST", 1))


async def main():
	"""Main function to run the APRS reporting loop."""
	cfg = Config()
	ais = ais_connect(cfg)
	for seq in Sequence():
		if seq % 2 == 1:
			await send_position(ais, cfg, seq)
		if seq % 6 == 1:
			send_header(ais, cfg)
		temp = get_temp()
		cpuload = get_cpuload()
		memused = get_memused()
		diskused = get_diskused()
		if os.getenv("GPSD_ENABLE"):
			uSat, nSat = get_gpsd_sat()
			telemetry = "{}>APP642:T#{:03d},{:d},{:d},{:d},{:d},{:d}".format(cfg.call, seq, temp, cpuload, memused, diskused, uSat)
			ais.sendall(telemetry)
			await logs_to_telegram(f"<u>{cfg.call} Telemetry-{seq}</u>\n\n<b>CPU Temp</b>: {temp / 10:.1f}°C\n<b>CPU Load</b>: {cpuload / 10:.1f}%\n<b>RAM Used</b>: {memused / 10:.1f}MB\n<b>Disk Used</b>: {diskused / 10:.1f}GB\n<b>GPS Used</b>: {uSat}/{nSat}")
			logging.info(telemetry)
			uptime = get_uptime()
			sats = f"sats={uSat}/{nSat}"
			nowz = f"time={dt.datetime.now(dt.timezone.utc).strftime('%d%H%Mz')}"
			status = "{0}>APP642:>{1}, {2}, {3}".format(cfg.call, nowz, uptime, sats)
			ais.sendall(status)
			await logs_to_telegram(f"<u>{cfg.call} Status-{seq}</u>\n\n{nowz}, {uptime}, {sats}")
			logging.info(status)
		else:
			telemetry = "{}>APP642:T#{:03d},{:d},{:d},{:d},{:d}".format(cfg.call, seq, temp, cpuload, memused, diskused)
			ais.sendall(telemetry)
			await logs_to_telegram(f"<u>{cfg.call} Telemetry-{seq}</u>\n\n<b>CPU Temp</b>: {temp / 10:.1f}°C\n<b>CPU Load</b>: {cpuload / 10:.1f}%\n<b>RAM Used</b>: {memused / 10:.1f}MB<b>Disk Used</b>: {diskused / 10:.1f}GB\n")
			logging.info(telemetry)
			uptime = get_uptime()
			nowz = f"time={dt.datetime.now(dt.timezone.utc).strftime('%d%H%Mz')}"
			status = "{0}>APP642:>{1}, {2}, {3}".format(cfg.call, nowz, uptime)
			ais.sendall(status)
			await logs_to_telegram(f"<u>{cfg.call} Status-{seq}</u>\n\n{nowz}, {uptime}")
			logging.info(status)
		randsleep = int(random.uniform(cfg.sleep - 30, cfg.sleep + 30))
		logging.info("Sleeping for %d seconds", randsleep)
		time.sleep(randsleep)


if __name__ == "__main__":
	configure_logging()
	try:
		logging.info("Starting the application...")
		asyncio.run(main())
	except KeyboardInterrupt:
		logging.info("Stopping application...")
	except Exception as e:
		logging.error("An error occurred: %s", e)
	finally:
		logging.info("Exiting script...")
		sys.exit(0)
