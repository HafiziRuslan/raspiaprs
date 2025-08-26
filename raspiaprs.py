#!/usr/bin/python3

import json
import logging
import os
import sys
import time
import aprslib
import humanize
import datetime as dt
import subprocess

from configparser import ConfigParser
from io import StringIO
from urllib.request import urlopen
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
THERMAL_FILE = "/sys/class/thermal/thermal_zone0/temp"
LOADAVG_FILE = "/proc/loadavg"
CPUINFO_FILE = "/proc/cpuinfo"
MEMINFO_FILE = "/proc/meminfo"
VERSION_FILE = "/proc/version"
OS_RELEASE_FILE = "/etc/os-release"
PISTAR_RELEASE_FILE = "/etc/pistar-release"
WPSD_RELEASE_FILE = "/etc/WPSD-release"
MMDVMHOST_FILE = "/etc/mmdvmhost"
MMDVMLOGPATH = "/var/log/pi-star"
MMDVMLOGPREFIX = "MMDVM"

# Set up logging
logging.basicConfig(
  filename="/var/log/raspiaprs.log",
  format="%(asctime)s %(levelname)s: %(message)s",
  datefmt="%Y-%m-%dT%H:%M:%S",
  level=logging.INFO,
)

class Config(object):
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
  def passcode(self):
    return self._passcode

  @passcode.setter
  def passcode(self, val):
    self._passcode = str(val)

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

class Sequence(object):
  """Generate an APRS sequence number."""
  def __init__(self):
    self.sequence_file = "/tmp/raspiaprs.sequence"
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
  try:
    with open(MEMINFO_FILE) as pfd:
      for line in pfd:
        if "MemTotal" in line:
          totalmem = int(line.split()[1])
        if "MemFree" in line:
          freemem = int(line.split()[1])
        if "Buffers" in line:
          buffmem = int(line.split()[1])
        if "Cached" in line:
          cachemem = int(line.split()[1])
        if "SwapTotal" in line:
          swaptotalmem = int(line.split()[1])
        if "SwapFree" in line:
          swapfreemem = int(line.split()[1])
    alltotalmem = totalmem + swaptotalmem
    allfreemem = freemem + swapfreemem
  except (IOError, ValueError):
    return 0
  return int(((allfreemem + buffmem + cachemem) / alltotalmem) * 10000)

def get_temp():
  try:
    with open(THERMAL_FILE) as tfd:
      _tmp = tfd.readline()
      temperature = int(_tmp.strip())
  except (IOError, ValueError):
    temperature = 20000
  return temperature

def get_osinfo():
  parser = ConfigParser()
  with open(OS_RELEASE_FILE) as osr:
    for line in osr:
      if "PRETTY_NAME" in line:
        osname = line.split("=", 1)[1].strip().strip('"')
  with open(CPUINFO_FILE) as cpu:
    for line in cpu:
      if "Model" in line:
        modelname = line.split(":", 1)[1].strip().strip('"')
  with open(VERSION_FILE) as ver:
    for line in ver:
      kernelver = " [" + line.split()[0] + line.split()[2] + "]"
      osver = " " + line.split()[5] + line.split()[6]
  try:
    with open(PISTAR_RELEASE_FILE, "r") as pir:
      parser.read_file(pir)
      version = "PiStar" + parser.get("Pi-Star", "Version") + "-" + parser.get("Pi-Star", "MMDVMHost")
  except (IOError, ValueError):
    try:
      with open(WPSD_RELEASE_FILE, "r") as wps:
        parser.read_file(wps)
        version = "WPSD" + parser.get("WPSD", "WPSD_Ver") + "-" + parser.get("WPSD", "MMDVMHost").split()[0]
    except (IOError, ValueError):
      version = "Unknown"
  return osname + osver + kernelver + "; " + modelname + "; " + version + "; "

def get_modem():
  log_mmdvm_now = os.path.join(MMDVMLOGPATH, f"{MMDVMLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log")
  log_mmdvm_previous = os.path.join(MMDVMLOGPATH, f"{MMDVMLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log")
  log_search_string = "MMDVM protocol version"
  log_line = ''
  modem_firmware = ''
  try:
    log_line = subprocess.run(f"grep \"{log_search_string}\" {log_mmdvm_now} | tail -1", shell=True, text=True).strip()
  except subprocess.CalledProcessError:
    try:
      log_line = subprocess.run(f"grep \"{log_search_string}\" {log_mmdvm_previous} | tail -1", shell=True, text=True).strip()
    except subprocess.CalledProcessError:
      pass
  if log_line:
    if 'DVMEGA' in log_line:
      modem_firmware = log_line[67:67+15]
    elif 'description: MMDVM ' in log_line:
      modem_firmware = f"MMDVM-{log_line[73:73+8]}"
    elif 'description: D2RG_MMDVM_HS-' in log_line:
      modem_firmware = f"D2RG_MMDVM_HS-{log_line[81:81+12].split()[0]}"
    elif 'description: MMDVM_HS_Hat-' in log_line:
      modem_firmware = f"MMDVM_HS_Hat-{log_line[80:80+12].split()[0]}"
    elif 'description: MMDVM_HS_Dual_Hat-' in log_line:
      modem_firmware = f"MMDVM_HS_Dual_Hat-{log_line[85:85+12].split()[0]}"
    elif 'description: MMDVM_HS-' in log_line:
      modem_firmware = f"MMDVM_HS-{log_line[76:76+12].split()[0].lstrip('v')}"
    elif 'description: MMDVM_MDO ' in log_line:
      modem_firmware = f"MMDVM_MDO-{log_line[85:85+12].split()[0].lstrip('v')}"
    elif 'description: MMDVM_HS' in log_line:
      modem_firmware = f"MMDVM_HS-{log_line[84:84+8].lstrip('v')}"
    elif 'description: Nano_DV-' in log_line:
      modem_firmware = f"NanoDV-{log_line[75:75+12].split()[0]}"
    elif 'description: Nano_hotSPOT-' in log_line:
      modem_firmware = f"Nano_hotSPOT-{log_line[80:80+12].split()[0].lstrip('v')}"
    elif 'description: Nano-Spot-' in log_line:
      modem_firmware = f"NanoSpot-{log_line[77:77+12].split()[0]}"
    elif 'description: OpenGD77 Hotspot' in log_line:
      modem_firmware = f"OpenGD77-{log_line[83:83+12].split()[0]}"
    elif 'description: OpenGD77_HS ' in log_line:
      modem_firmware = f"OpenGD77_HS-{log_line[79:79+12].split()[0]}"
    elif 'description: SkyBridge-' in log_line:
      modem_firmware = f"SkyBridge-{log_line[77:77+12].split()[0]}"
    elif 'description: ZUMspot-' in log_line:
      modem_firmware = f"ZUMspot-{log_line[75:75+12].split()[0]}"
    elif 'description: ZUMspot ' in log_line:
      modem_firmware = f"ZUMspot-{log_line[83:83+12].split()[0]}"
  return modem_firmware

def get_uptime():
  with open("/proc/uptime") as upf:
    uptime_seconds = float(upf.readline().split()[0])
    uptime = dt.timedelta(seconds=uptime_seconds)
  return "up " + humanize.precisedelta(uptime, suppress=['milliseconds', 'microseconds'], format="%0.0f").replace("seconds", "sec").replace("minutes", "min").replace("hours", "hr") + "; "

def get_mmdvminfo():
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
    if parser.getboolean("DMR", "Enable") == True:
      cc = " DMRCC" + parser.get("DMR", "ColorCode")
  return (str(tx) + "MHz" + shift + cc) + "; "

def send_position(ais, config):
  pos = aprslib.packets.PositionReport()
  pos.fromcall = config.call
  pos.tocall = "APP642"
  pos.symbol = config.symbol
  pos.symbol_table = config.symbol_table
  pos.timestamp = time.time()
  pos.latitude = config.latitude
  pos.longitude = config.longitude
  pos.altitude = config.altitude
  pos.comment = get_mmdvminfo() + get_osinfo() + get_modem()
  logging.info(str(pos))
  try:
    ais.sendall(pos)
  except ConnectionError as err:
    logging.warning(err)

def send_header(ais, config):
  send_position(ais, config)
  try:
    ais.sendall("{0}>APP642::{0:9s}:PARM.CPUTemperature,CPULoad,MemoryUsed".format(config.call))
    ais.sendall("{0}>APP642::{0:9s}:UNIT.degC,pcnt,pcnt".format(config.call))
    ais.sendall("{0}>APP642::{0:9s}:EQNS.0,0.001,0,0,0.01,0,0,0.01,0".format(config.call))
  except ConnectionError as err:
    logging.warning(err)

def ais_connect(config):
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
  sys.exit(os.EX_NOHOST)

def main():
  config = Config()
  ais = ais_connect(config)
  send_header(ais, config)
  for sequence in Sequence():
    if sequence % 10 == 1:
      send_header(ais, config)
    temp = get_temp()
    cpuload = get_cpuload()
    memused = get_memused()
    uptime = get_uptime()
    tel = "{}>APP642:T#{:03d},{:d},{:d},{:d},0,0,00000000".format(config.call, sequence, temp, cpuload, memused)
    ais.sendall(tel)
    logging.info(tel)
    upt = "{0}>APP642:>{1}https://github.com/HafiziRuslan/raspiaprs".format(config.call, uptime)
    ais.sendall(upt)
    logging.info(upt)
    time.sleep(config.sleep)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    sys.exit()
