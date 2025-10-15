#!/usr/bin/python3

import datetime as dt
import json
import logging
import os
import random
# import re
import subprocess
import sys
import time
from configparser import ConfigParser
from io import StringIO
from urllib.request import urlopen

import aprslib
import humanize
from aprslib.exceptions import ConnectionError

# Default configuration file path
CONFIG_FILE = "/etc/raspiaprs.conf"
CONFIG_DEFAULT = """
[APRS]
call: N0CALL
ssid: 0
latitude: 0.0
longitude: 0.0
altitude: 0.0
sleep: 600
symbol: n
symbol_table: /
[APRS-IS]
server: rotate.aprs2.net
port: 14580
"""

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
  filename="/var/log/raspiaprs.log",
  format="%(asctime)s %(levelname)s: %(message)s",
  datefmt="%Y-%m-%dT%H:%M:%S",
  level=logging.INFO,
)


# Configuration class to handle settings
class Config(object):
  """Class to handle configuration settings."""
  def __init__(self):
    parser = ConfigParser()
    parser.read_file(StringIO(CONFIG_DEFAULT))
    self._passcode = ""
    self._call = "NOCALL"
    self._longitude = 0.0
    self._latitude = 0.0
    self._altitude = 0.0
    self._sleep = 600
    self._symbol = "n"
    self._symbol_table = "/"
    self._server = "rotate.aprs2.net"
    self._port = 14580
    if not os.path.exists(CONFIG_FILE):
      logging.info("Using default config")
    else:
      try:
        logging.info("Reading config file")
        with open(CONFIG_FILE, "r") as fdc:
          parser.read_file(fdc)
        logging.info("Config file %s read", CONFIG_FILE)
      except (IOError, SystemError):
        raise SystemError("No [APRS] section configured")
    self.call = parser.get("APRS", "call") + "-" + parser.get("APRS", "ssid")
    self.sleep = parser.get("APRS", "sleep")
    self.symbol_table = parser.get("APRS", "symbol_table")
    self.symbol = parser.get("APRS", "symbol")
    self.altitude = float(parser.get("APRS", "altitude"))
    lat, lon = [float(parser.get("APRS", c)) for c in ("latitude", "longitude")]
    if not lat or not lon:
      self.latitude, self.longitude = get_coordinates()
    else:
      self.latitude, self.longitude = lat, lon
    if parser.has_option("APRS-IS", "server"):
      self.server = parser.get("APRS-IS", "server")
    else:
      logging.warning("Using default APRS-IS server: %s", self._server)
      self.server = self._server
    if parser.has_option("APRS-IS", "port"):
      self.port = int(parser.get("APRS-IS", "port"))
    else:
      self.port = self._port
    if parser.has_option("APRS", "passcode"):
      self.passcode = parser.get("APRS", "passcode")
    else:
      logging.warning("Generating passcode")
      self.passcode = aprslib.passcode(self.call)

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
    self.sequence_file = "/tmp/raspiaprs.seq"
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


def get_coordinates():
  """Get approximate latitude and longitude using IP address lookup."""
  logging.warning("Trying to figure out the coordinate using your IP address")
  url = "http://ip-api.com/json/"
  try:
    response = urlopen(url)
    _data = response.read()
    data = json.loads(_data.decode())
  except IOError as err:
    logging.error(err)
    return (0, 0)
  else:
    logging.warning("Position: %f, %f", data["lat"], data["lon"])
    return data["lat"], data["lon"]


def get_cpuload():
  """Get CPU load as a percentage of total capacity scaled by 10000."""
  try:
    with open(LOADAVG_FILE) as lfd:
      loadstr = lfd.readline()
  except IOError:
    return 0
  try:
    load5 = float(loadstr.split()[1])
    corecount = float(subprocess.check_output(f"grep -c '^processor' {CPUINFO_FILE}", shell=True, text=True).strip())
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


def get_diskused():
  """Get used disk space in GB."""
  try:
    df = subprocess.check_output("df -k /", shell=True, text=True).strip().split("\n")
    diskinfo = df[1].split()
    diskused = int(diskinfo[2])
  except (IOError, ValueError, IndexError, subprocess.CalledProcessError):
    return 0
  return int(diskused / 1000)


def get_traffic():
  """Get average network traffic in kbit/s over the last 5 minutes scaled by 100."""
  timenow = dt.datetime.now()
  roundedtime = timenow - dt.timedelta(minutes=timenow.minute % 5 + 5)
  try:
    today = subprocess.check_output(f"vnstat -i wlan0 -5 1 | grep {dt.datetime.strftime(roundedtime, '%H:%M')}", shell=True, text=True).strip()
    # time = today.split()[0]
    # up = float(today.split()[1])
    # upunit = today.split()[2]
    # down = float(today.split()[4])
    # downunit = today.split()[5]
    # total = float(today.split()[7])
    # totalunit = today.split()[8]
    avg = float(today.split()[10])
    avgunit = today.split()[11]
  except (IOError, ValueError, IndexError, subprocess.CalledProcessError):
    return 0
  if avgunit == "Mbit/s":
    avg = avg * 1000
  elif avgunit == "Gbit/s":
    avg = avg * 1000000
  return int(avg * 100)


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
  parser = ConfigParser()
  osname = ""
  osver = ""
  kernelver = ""
  try:
    with open(OS_RELEASE_FILE) as osr:
      for line in osr:
        if "PRETTY_NAME" in line:
          osname = line.split("=", 1)[1].strip().strip('"')
  except (IOError, OSError):
    logging.warning("OS release file not found: %s", OS_RELEASE_FILE)
  try:
    with open(VERSION_FILE) as ver:
      for line in ver:
        parts = line.split()
        # Ensure expected indexes exist before accessing
        if len(parts) >= 7:
          kernelver = parts[0] + parts[2]
          osver = parts[5] + " " + parts[6]
        elif len(parts) >= 3:
          kernelver = parts[0] + parts[2]
  except (IOError, IndexError):
    logging.warning("Version file not found or unexpected format: %s", VERSION_FILE)
  softver = " Unknown"
  try:
    with open(PISTAR_RELEASE_FILE, "r") as pir:
      parser.read_file(pir)
      softver = " " + parser.get("Pi-Star", "MMDVMHost") + "#" + parser.get("Pi-Star", "Version")
  except (IOError, ValueError):
    try:
      with open(WPSD_RELEASE_FILE, "r") as wps:
        parser.read_file(wps)
        softver = " " + parser.get("WPSD", "MMDVMHost").split()[0] + "#" + parser.get("WPSD", "WPSD_Ver")
    except (IOError, ValueError):
      pass
  return f" {osname} {osver} [{kernelver}] {softver}"


def get_modem():
  """Get modem firmware information from MMDVM log files."""
  log_mmdvm_now = os.path.join(MMDVMLOGPATH, f"{MMDVMLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log")
  log_mmdvm_previous = os.path.join(MMDVMLOGPATH, f"{MMDVMLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log")
  log_search_string = "MMDVM protocol version"
  log_line = str()
  modem_firmware = str()
  try:
    log_line = subprocess.check_output(f'grep "{log_search_string}" {log_mmdvm_now} | tail -1', shell=True, text=True).strip()
  except subprocess.CalledProcessError:
    try:
      log_line = subprocess.check_output(f'grep "{log_search_string}" {log_mmdvm_previous} | tail -1', shell=True, text=True).strip()
    except subprocess.CalledProcessError:
      pass
  if log_line:
    if "DVMEGA" in log_line:
      modem_firmware = log_line[67 : 67 + 15]
    elif "description: MMDVM " in log_line:
      modem_firmware = f"MMDVM-{log_line[73 : 73 + 8]}"
    elif "description: D2RG_MMDVM_HS-" in log_line:
      modem_firmware = f"D2RG_MMDVM_HS-{log_line[81 : 81 + 12].split()[0]}"
    elif "description: MMDVM_HS_Hat-" in log_line:
      modem_firmware = f"MMDVM_HS_Hat-{log_line[80 : 80 + 12].split()[0]}"
    elif "description: MMDVM_HS_Dual_Hat-" in log_line:
      modem_firmware = f"MMDVM_HS_Dual_Hat-{log_line[85 : 85 + 12].split()[0]}"
    elif "description: MMDVM_HS-" in log_line:
      modem_firmware = f"MMDVM_HS-{log_line[76 : 76 + 12].split()[0].lstrip('v')}"
    elif "description: MMDVM_MDO " in log_line:
      modem_firmware = f"MMDVM_MDO-{log_line[85 : 85 + 12].split()[0].lstrip('v')}"
    elif "description: MMDVM_HS" in log_line:
      modem_firmware = f"MMDVM_HS-{log_line[84 : 84 + 8].lstrip('v')}"
    elif "description: Nano_DV-" in log_line:
      modem_firmware = f"NanoDV-{log_line[75 : 75 + 12].split()[0]}"
    elif "description: Nano_hotSPOT-" in log_line:
      modem_firmware = f"Nano_hotSPOT-{log_line[80 : 80 + 12].split()[0].lstrip('v')}"
    elif "description: Nano-Spot-" in log_line:
      modem_firmware = f"NanoSpot-{log_line[77 : 77 + 12].split()[0]}"
    elif "description: OpenGD77 Hotspot" in log_line:
      modem_firmware = f"OpenGD77-{log_line[83 : 83 + 12].split()[0]}"
    elif "description: OpenGD77_HS " in log_line:
      modem_firmware = f"OpenGD77_HS-{log_line[79 : 79 + 12].split()[0]}"
    elif "description: SkyBridge-" in log_line:
      modem_firmware = f"SkyBridge-{log_line[77 : 77 + 12].split()[0]}"
    elif "description: ZUMspot-" in log_line:
      modem_firmware = f"ZUMspot-{log_line[75 : 75 + 12].split()[0]}"
    elif "description: ZUMspot " in log_line:
      modem_firmware = f"ZUMspot-{log_line[83 : 83 + 12].split()[0]}"
  return f" {modem_firmware}"


def get_dmrmaster():
  """Get connected DMR master from DMRGateway log files."""
  parser = ConfigParser()
  dmr_master = ""
  with open(MMDVMHOST_FILE, "r") as mmh:
    parser.read_file(mmh)
    if parser.getboolean("DMR", "Enable"):
      log_dmrgw_now = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log")
      log_dmrgw_previous = os.path.join(MMDVMLOGPATH, f"{DMRGATEWAYLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log")
      log_master_string = "Logged into the master successfully"
      log_ref_string = "XLX, Linking"
      # log_master_dc_string = "Closing DMR Network"
      master_line = list()
      # master_dc_line = list()
      ref_line = list()
      dmrmaster = list()
      dmrmasters = list()
      try:
        master_line = subprocess.check_output(f'grep "{log_master_string}" {log_dmrgw_now}', shell=True, text=True).splitlines()
        # master_dc_line = subprocess.check_output(f'grep "{log_master_dc_string}" {log_dmrgw_now}', shell=True, text=True).splitlines()
        ref_line = subprocess.check_output(f'grep "{log_ref_string}" {log_dmrgw_now} | tail -1', shell=True, text=True).splitlines()
      except subprocess.CalledProcessError:
        try:
          master_line = subprocess.check_output(f'grep "{log_master_string}" {log_dmrgw_previous}', shell=True, text=True).splitlines()
          # master_dc_line = subprocess.check_output(f'grep "{log_master_dc_string}" {log_dmrgw_previous}', shell=True, text=True).splitlines()
          ref_line = subprocess.check_output(f'grep "{log_ref_string}" {log_dmrgw_previous} | tail -1', shell=True, text=True).splitlines()
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
  nowz = dt.datetime.now(dt.UTC).strftime("%H%M%Sz")
  now = dt.datetime.now().strftime("%H%M%S")
  with open(UPTIME_FILE) as upf:
    uptime_seconds = float(upf.readline().split()[0])
    uptime = dt.timedelta(seconds=uptime_seconds)
  return f"up {humanize.precisedelta(uptime, minimum_unit='seconds', format='%0.0f').replace(' and', ',').replace('seconds', 'sec').replace('minutes', 'min').replace('hours', 'hr')} @ {nowz}/{now}"


def get_mmdvminfo():
  """Get MMDVM configured frequency and color code."""
  parser = ConfigParser()
  with open(MMDVMHOST_FILE, "r") as mmh:
    parser.read_file(mmh)
    rx = round(int(parser.get("Info", "RXFrequency")) / 1000000, 6)
    tx = round(int(parser.get("Info", "TXFrequency")) / 1000000, 6)
    if tx > rx:
      shift = " (" + str(round(rx - tx, 6)) + "MHz)"
    elif tx < rx:
      shift = " (+" + str(round(rx - tx, 6)) + "MHz)"
    else:
      shift = ""
    if parser.getboolean("DMR", "Enable"):
      cc = " DMRCC" + parser.get("DMR", "ColorCode")
    else:
      cc = ""
  return (str(tx) + "MHz" + shift + cc) + get_dmrmaster() + ","


def get_mmdvmmode():
  """Get enabled modes from MMDVMHost configuration."""
  parser = ConfigParser()
  with open(MMDVMHOST_FILE, "r") as mdh:
    parser.read_file(mdh)
    dmr = parser.get("DMR", "Enable", fallback=0)
    dstar = parser.get("D-Star", "Enable", fallback=0)
    c4fm = parser.get("System Fusion", "Enable", fallback=0)
    p25 = parser.get("P25", "Enable", fallback=0)
    nxdn = parser.get("NXDN", "Enable", fallback=0)
    pocsag = parser.get("POCSAG", "Enable", fallback=0)
  return f"{dmr}{dstar}{c4fm}{p25}{nxdn}{pocsag}"


def send_position(ais, config):
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

  mmdvminfo = get_mmdvminfo()
  osinfo = get_osinfo()
  modem = get_modem()
  comment = f"{mmdvminfo}{osinfo}{modem} https://github.com/HafiziRuslan/raspiaprs"
  latstr = _lat_to_aprs(config.latitude)
  lonstr = _lon_to_aprs(config.longitude)
  # Use uncompressed APRS position format: !DDMM.mmN/SymbolTableDDDMM.mmWSymbol comment
  payload = f"!{latstr}{config.symbol_table}{lonstr}{config.symbol} {comment}"
  packet = f"{config.call}>APP642::{config.call:9s}:{payload}"
  logging.info(packet)
  try:
    ais.sendall(packet)
  except ConnectionError as err:
    logging.warning(err)


def send_header(ais, config):
  """Send APRS header information to APRS-IS."""
  send_position(ais, config)
  try:
    ais.sendall("{0}>APP642::{0:9s}:PARM.CPUTemp,CPULoad,MemUsed,DiskUsed,NetAvg,DMR,DSTAR,C4FM,P25,NXDN,POCSAG".format(config.call))
    ais.sendall("{0}>APP642::{0:9s}:UNIT.degC,pcnt,Mbytes,Gbytes,kbit/s,on,on,on,on,on,on".format(config.call))
    ais.sendall("{0}>APP642::{0:9s}:EQNS.0,0.001,0,0,0.01,0,0,0.001,0,0,0.001,0,0,0.01,0,000000".format(config.call))
  except ConnectionError as err:
    logging.warning(err)


def ais_connect(config):
  """Establish connection to APRS-IS with retries."""
  logging.info("Connecting to APRS-IS server %s:%d as %s", config.server, config.port, config.call)
  ais = aprslib.IS(config.call, passwd=config.passcode, host=config.server, port=config.port)
  for retry in range(5):
    try:
      ais.connect()
    except ConnectionError as err:
      logging.warning(err)
      time.sleep(10)
    else:
      return ais
  logging.error("Connection error, exiting")
  sys.exit(getattr(os, "EX_NOHOST", 1))


def main():
  """Main function to run the APRS reporting loop."""
  config = Config()
  ais = ais_connect(config)
  send_header(ais, config)
  for sequence in Sequence():
    if sequence % 10 == 1:
      send_header(ais, config)
    temp = get_temp()
    cpuload = get_cpuload()
    memused = get_memused()
    diskused = get_diskused()
    netavg = get_traffic()
    modes = get_mmdvmmode()
    uptime = get_uptime()
    tel = "{}>APP642:T#{:03d},{:d},{:d},{:d},{:d},{:d},{}00".format(config.call, sequence, temp, cpuload, memused, diskused, netavg, modes)
    ais.sendall(tel)
    logging.info(tel)
    upt = "{0}>APP642:>{1}".format(config.call, uptime)
    ais.sendall(upt)
    logging.info(upt)
    randsleep = int(random.uniform(config.sleep, config.sleep + 30))
    logging.info("Sleeping for %d seconds", randsleep)
    time.sleep(randsleep)


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    sys.exit()
