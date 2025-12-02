#!/usr/bin/python3

"""RaspiAPRS: Send APRS position and telemetry from Raspberry Pi to APRS-IS."""

import aprslib
import datetime as dt
import dotenv
import humanize
import json
import logging
import os
import random
import subprocess
import sys
# import telegram
import time

from aprslib.exceptions import ConnectionError as APRSConnectionError
from dotenv import set_key
from gpsdclient import GPSDClient
from urllib.request import urlopen

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
logging.basicConfig(
  filename=os.path.join("/tmp", "raspiaprs.log"),
  format="%(asctime)s %(levelname)s: %(message)s",
  datefmt="%Y-%m-%dT%H:%M:%S",
  level=logging.INFO,
)


# Configuration class to handle settings
class Config(object):
  """Class to handle configuration settings."""
  def __init__(self):
    dotenv.load_dotenv(".env")

    call = os.getenv("APRS_CALL", "N0CALL")
    ssid = os.getenv("APRS_SSID", "0")
    self.call = f"{call}-{ssid}"
    self.sleep = int(os.getenv("APRS_SLEEP", 600))
    self.symbol_table = os.getenv("APRS_SYMBOL_TABLE", "/")
    self.symbol = os.getenv("APRS_SYMBOL", "n")

    lat = os.getenv("APRS_LATITUDE", "0.0")
    lon = os.getenv("APRS_LONGITUDE", "0.0")
    alt = os.getenv("APRS_ALTITUDE", "0.0")

    if os.getenv("GPSD_ENABLE"):
      self.latitude, self.longitude, self.altitude = get_gpsd_coordinate()
    else:
      if not lat and not lon:
        self.latitude, self.longitude = get_coordinates()
        self.altitude = alt
      else:
        self.latitude, self.longitude, self.altitude = lat, lon, alt

    self.server = os.getenv("APRSIS_SERVER", "rotate.aprs2.net")
    self.port = int(os.getenv("APRSIS_PORT", 14580))

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

  logging.info("Configuration: %s", dotenv.dotenv_values(".env"))


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


def get_gpsd_coordinate():
  """Get latitude and longitude from GPSD."""
  logging.info("Trying to figure out the coordinate using GPSD")
  try:
    with GPSDClient() as client:
      for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
        if result["mode"] == 3:
          logging.info("GPSD 3D fix acquired")
          utc = result.get("time", dt.datetime.now(dt.timezone.utc))
          lat = result.get("lat", "n/a")
          lon = result.get("lon", "n/a")
          alt = result.get("alt", "n/a")
        if lat != "n/a" and lon != "n/a" and alt != "n/a":
          logging.info("%s | GPSD Position: %s, %s, %s", utc, lat, lon, alt)
          set_key(".env", "APRS_LATITUDE", lat, quote_mode="none")
          set_key(".env", "APRS_LONGITUDE", lon, quote_mode="none")
          set_key(".env", "APRS_ALTITUDE", alt, quote_mode="none")
          Config.latitude = lat
          Config.longitude = lon
          Config.altitude = alt
        return lat, lon, alt
  except Exception as e:
    logging.error("Error getting GPSD data: %s", e)
    return (0,0,0)


# def get_modemmanager_coordinates():
#   """Get latitude and longitude from ModemManager."""
#   logging.info("Trying to figure out the coordinate using ModemManager")
#   try:
#     mm_output = subprocess.run(args=["sudo", "/home/pi-star/raspiaprs/mmcli_loc_get.sh"], capture_output=True, text=True).stdout.splitlines()
#     for line in mm_output:
#       if line.startswith("Latitude:"):
#         lat = str(line.split(":")[1].strip())
#       if line.startswith("Longitude:"):
#         lon = str(line.split(":")[1].strip())
#       if line.startswith("Altitude:"):
#         alt = str(line.split(":")[1].strip())
#       if lat != "0.0" and lon != "0.0" and alt != "0.0":
#         logging.info("ModemManager Position: %f, %f, %f", lat, lon, alt)
#         parser = ConfigParser()
#         with open(".env", "r") as fdc:
#           parser.read_file(fdc)
#           parser.set("APRS", "latitude", str(lat))
#           parser.set("APRS", "longitude", str(lon))
#           parser.set("APRS", "altitude", str(alt))
#         with open(".env", "w") as fdc:
#           parser.write(fdc)
#       Config.latitude = lat
#       Config.longitude = lon
#       Config.altitude = alt
#       return lat, lon, alt
#   except Exception as e:
#     logging.error("Error getting modem manager data: %s", e)
#     return lat, lon, alt


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
  """Get CPU load as a percentage of total capacity scaled by 10000."""
  try:
    with open(LOADAVG_FILE) as lfd:
      loadstr = lfd.readline()
  except IOError:
    return 0
  try:
    load5 = float(loadstr.split()[1])
    corecount = float(subprocess.check_output(["grep", "-c", "^processor", CPUINFO_FILE], text=True).strip())
  except ValueError:
    return 0
  return int((load5 / corecount) * 10000)


def get_memused():
  """Get used memory in MB."""
  freemem = 0
  buffmem = 0
  cachemem = 0
  swapfreemem = 0
  try:
    with open(MEMINFO_FILE) as pfd:
      for line in pfd:
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
        if line.startswith("SwapFree"):
          parts = line.split()
          if len(parts) > 1:
            swapfreemem = int(parts[1])
    allfreemem = freemem + swapfreemem
  except (IOError, ValueError):
    return 0
  return int(allfreemem + buffmem + cachemem)


def get_temp():
  """Get CPU temperature in degC scaled by 100."""
  try:
    with open(THERMAL_FILE) as tfd:
      _tmp = tfd.readline()
      temperature = int(_tmp.strip())
  except (IOError, ValueError):
    temperature = 20000
  return temperature


def get_osinfo():
  """Get operating system information."""
  osname = ""
  try:
    with open(OS_RELEASE_FILE) as osr:
      for line in osr:
        if "PRETTY_NAME" in line:
          osname = line.split("=", 1)[1].strip().strip('"')
  except (IOError, OSError):
    logging.warning("OS release file not found: %s", OS_RELEASE_FILE)
  kernelver = ""
  try:
    with open(VERSION_FILE) as ver:
      for line in ver:
        parts = line.split()
        if len(parts) >= 3:
          kernelver = parts[0] + parts[2]
  except (IOError, IndexError):
    logging.warning("Version file not found or unexpected format: %s", VERSION_FILE)
  return f" {osname} [{kernelver}]"


def get_dmrmaster():
  """Get connected DMR master from DMRGateway log files."""
  dmr_master = ""
  # We need to parse MMDVMHost to see if DMR is enabled.
  # A simple string search is easier than using a full ini parser.
  with open(MMDVMHOST_FILE, "r") as mmh:
    if "Enable=1" in mmh.read():
      log_dmrgw_previous = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log")
      log_dmrgw_now = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log")
      log_master_string = "Logged into the master successfully"
      log_ref_string = "XLX, Linking"
      # log_master_dc_string = "Closing DMR Network"
      master_line = list()
      # master_dc_line = list()
      ref_line = list()
      dmrmaster = list()
      dmrmasters = list()
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
        master = master_line[mascount].split()[3].split(",")[0]
        if master == "XLX":
          for refcount in range(ref_line_count):
            master = ref_line[refcount].split()[7] + ref_line[refcount].split()[8]
        dmrmaster.append(master)
        # for dccount in range(master_dc_line_count):
        #   master_dc = master_dc_line[dccount].split()[3].split(",")[0]
        #   if master_dc == "XLX":
        #     xlxdcid = dmrmaster.index(re.search(r"^XLX.+", dmrmaster[dccount])[0])
        #     dmrmaster.pop(xlxdcid)
        #   dmrmaster.remove(master_dc)
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
  # Using string parsing to avoid a full dependency for a few values.
  rx_freq, tx_freq, color_code, dmr_enabled = 0, 0, "1", False
  with open(MMDVMHOST_FILE, "r") as mmh:
    for line in mmh:
      if line.startswith("RXFrequency="):
        rx_freq = int(line.strip().split("=")[1])
      elif line.startswith("TXFrequency="):
        tx_freq = int(line.strip().split("=")[1])
      elif line.startswith("ColorCode="):
        color_code = line.strip().split("=")[1]
      elif "[DMR]" in line:
        dmr_enabled = "Enable=1" in next(mmh, "")

  rx = round(rx_freq / 1000000, 6)
  tx = round(tx_freq / 1000000, 6)
  shift = ""
  if tx > rx:
    shift = f" ({round(rx - tx, 6)}MHz)"
  elif tx < rx:
    shift = f" (+{round(rx - tx, 6)}MHz)"
  cc = f" DMRCC{color_code}" if dmr_enabled else ""
  return (str(tx) + "MHz" + shift + cc) + get_dmrmaster() + ","


# def logs_to_telegram(tg_message: str):
#   """Send log message to Telegram channel."""
#   parser = ConfigParser()
#   parser.read(CONFIG_FILE)
#   if parser.getboolean("TELEGRAM", "enable"):
#     tgbot = telegram.Bot(token=parser.get("TELEGRAM", "token"))
#     try:
#       botcall = tgbot.send_message(
#         chat_id=parser.get("TELEGRAM", "chat_id"),
#         message_thread_id=parser.getint("TELEGRAM", "topic_id"),
#         text=tg_message,
#         parse_mode="HTML",
#         # link_preview_options={"is_disabled": True},
#         disable_web_page_preview=True
#       )
#       logging.info("Sent message to Telegram: %s", botcall)
#     except Exception as e:
#       logging.error("Failed to send message to Telegram: %s", e)


def send_position(ais, cfg):
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
    cur_lat, cur_lon, cur_alt = get_gpsd_coordinate()
  else:
    cur_lat = os.getenv("APRS_LATITUDE", cfg.latitude)
    cur_lon = os.getenv("APRS_LONGITUDE", cfg.longitude)
    cur_alt = os.getenv("APRS_ALTITUDE", cfg.altitude)
  mmdvminfo = get_mmdvminfo()
  osinfo = get_osinfo()
  comment = f"{mmdvminfo}{osinfo} https://github.com/HafiziRuslan/raspiaprs"
  timestamp = dt.datetime.now(dt.timezone.utc).strftime("%d%H%Mz")
  latstr = _lat_to_aprs(int(cur_lat))
  lonstr = _lon_to_aprs(int(cur_lon))
  altstr = _alt_to_aprs(int(cur_alt))
  payload = f"/{timestamp}{latstr}{cfg.symbol_table}{lonstr}{cfg.symbol}{altstr}{comment}"
  packet = f"{cfg.call}>APP642:{payload}"
  # logs_to_telegram(packet)
  logging.info(packet)
  try:
    ais.sendall(packet)
  except APRSConnectionError as err:
    logging.warning(err)


def send_header(ais, cfg):
  """Send APRS header information to APRS-IS."""
  send_position(ais, cfg)
  try:
    ais.sendall("{0}>APP642::{0:9s}:PARM.CPUTemp,CPULoad,MemUsed".format(cfg.call))
    ais.sendall("{0}>APP642::{0:9s}:UNIT.degC,pcnt,Mbytes".format(cfg.call))
    ais.sendall("{0}>APP642::{0:9s}:EQNS.0,0.001,0,0,0.01,0,0,0.001,0".format(cfg.call))
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
      time.sleep(15)
    else:
      return ais
  logging.error("Connection error, exiting")
  sys.exit(getattr(os, "EX_NOHOST", 1))


def main():
  """Main function to run the APRS reporting loop."""
  cfg = Config()
  ais = ais_connect(cfg)
  send_header(ais, cfg)
  for sequence in Sequence():
    if sequence % 12 == 1:
      send_header(ais, cfg)
    if sequence % 2 == 1:
      send_position(ais, cfg)
    temp = get_temp()
    cpuload = get_cpuload()
    memused = get_memused()
    telemetry = "{}>APP642:T#{:03d},{:d},{:d},{:d}".format(cfg.call, sequence, temp, cpuload, memused)
    ais.sendall(telemetry)
    # logs_to_telegram(telemetry)
    logging.info(telemetry)
    uptime = get_uptime()
    nowz = f"time={dt.datetime.now(dt.timezone.utc).strftime('%d%H%Mz')}"
    status = "{0}>APP642:>{1}, {2}".format(cfg.call, nowz, uptime)
    ais.sendall(status)
    # logs_to_telegram(status)
    logging.info(status)
    randsleep = int(random.uniform(cfg.sleep - 30, cfg.sleep + 30))
    logging.info("Sleeping for %d seconds", randsleep)
    time.sleep(randsleep)


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    sys.exit(0)
