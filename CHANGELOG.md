# CHANGELOG

All notable changes to this project will be documented in this file.

## [unreleased] - (2025-12-11T08:50:22.104789206+08:00)

### 🚀 Features

- ✨ feat(gpsd): enhance GPS data reporting
- ✨ feat(readme): update installation instructions

### 🐛 Bug Fixes

- 🐛 fix(gps): remove unused nSat variable
- 🐛 fix(gpsd): correct gps position check
- 🐛 fix(gpsd): use 'is not' for float comparison
- 🐛 fix(repo): correct repository URL in cliff config and main script
- ✨ refactor(main): sort import & fix identation
- 🐛 fix(main): reduce tab spacing
- 🐛 fix(scripts): correct virtual environment activation path

### 💼 Other

- Update CHANGELOG

### 🚜 Refactor

- 📝 docs(cliff config): update changelog template and commit parsers

### 📚 Documentation

- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(pyproject): update readme filename
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note

### ⚙️ Miscellaneous Tasks

- 🔧 chore(main.sh): improve uv installation message
- 🔧 chore(uv): remove uv self update
- 🔧 chore(install): remove uv shell completion setup
- 🔧 chore(scripts): improve shell script output and activation
- 🔧 chore(scripts): update uv install message
- 🔧 chore(ci): remove changelog-ci-config.yaml
- 📦 build(release): add main.sh to release artifacts
- 🔧 chore(ci): update cliff.toml path in release workflow
- 🔧 chore(ci): update git-cliff configuration path

## [beta] - (2025-12-10T20:39:10+08:00)

### 🚀 Features

- ✨ feat(deps): update project dependencies and tooling
- ✨ feat(ci): change changelog file extension to md
- ✨ feat(ci): add merge schedule workflow
- ✨ feat(ci): add changelog generation workflow
- ✨ feat(config): consolidate APRS sleep time and update GPSD settings
- ✨ feat(telegram): enhance telegram message link previews
- ✨ feat(telegram): enhance telegram logging with location support
- ✨ feat(gps): enhance gps data handling and aprs message
- ✨ feat(main): enhance application lifecycle logging
- ✨ feat(deps): add aprslib and gpsdclient dependencies
- ♻️ refactor(core): migrate from configparser to dotenv for config management
- ✨ feat(gps): add gpsd socket configuration and improve data handling
- ✨ feat(telegram): add telegram bot integration for notifications
- ✨ feat(gps): integrate modemmanager coordinates
- ✨ feat(gps): persist gpsd coordinates to config
- ✨ feat(gps): integrate gpsdclient for gps data
- ✨ feat(gps): integrate gpsd for precise location data
- ✨ feat(raspiaprs): add gpsd support
- 📦 build(ci): update gitlab sync action version to v2.1.0
- ✨ feat(aprs): enhance telemetry and status reporting
- ✨ feat(position): add altitude support to APRS position reports
- ✨ feat(position): enhance aprs position reporting
- ✨ feat(aprs): add AX.25 support to APRS
- ✨ feat(mmdvm): add POCSAG support and update telemetry
- ✨ feat(mmdvm): add mmdvm mode reporting
- ✨ feat(uptime): include local time in uptime string
- ✨ feat(dmr): Add DMR master connection status to status output
- ✨ feat(system): add DMRGateway status and master info
- ✨ feat(main): add network traffic monitoring
- ✨ feat(config): enhance configuration management and data handling
- ✨ feat(main): add github link to position comment
- ✨ feat(aprs): add modem firmware version to aprs comment
- ✨ feat(readme): add disk usage metric
- ✨ feat(telemetry): add disk usage to APRS telemetry

### 🐛 Bug Fixes

- ♻️ refactor(ci): streamline release asset upload process
- 🔧 chore(config): update cliff configuration and release workflow
- 🐛 fix(ci): adjust git-cliff checkout depth and file paths
- 👷 ci(cliff): disable conventional commits parsing
- 📦 build(ci): update file paths in release workflow
- 🐛 fix(telemetry): correct CPU load calculation in telegram logs
- fix: remove files error for the moment
- fix: files error
- fix: * doesn't match any files in actions
- fix: * doesn't match any files in actions
- fix: sync cpuload precision to 0.1
- fix: sync all precision to 0.1
- fix: type-error
- fix: type-error in telemetry
- 🐛 fix(aprs): correct parameter names for memory units
- 🐛 fix(ais): move filter setting after successful connection
- 🐛 fix(aprs): ensure filter is set after connection attempt
- 🐛 fix(gps): correct gpsd position handling
- 🐛 fix(main): correct telemetry and status timing
- 🐛 fix(main): fix async call in send_position
- 🐛 fix(main): correct telemetry and status sending logic
- 🐛 fix(dmr): correct dmr master list creation
- 🐛 fix(main): correct telemetry sequence and logging
- 🐛 fix(dmr): correct dmrmaster extraction from logs
- 🐛 fix(main): correct header sending frequency
- 🐛 fix(main): correct aprs reporting loop
- 🐛 fix(gpsd): correct gpsd position and add satellite data
- fix identation
- 🐛 fix(osinfo): correct os name parsing in get_osinfo
- 🐛 fix(osinfo): improve os information retrieval
- 🐛 fix(dmr): correct master callsign retrieval
- 🐛 fix(telegram): correct telegram message id logging
- 🐛 fix(osinfo): correct osname parsing in get_osinfo
- 🐛 fix(telegram): correct link_preview_options format
- 🐛 fix(telegram): fix telegram location sending logic
- 🐛 fix(position): correct coordinate conversion in send_position
- 🐛 fix(position): correct lat/lon to integer for aprs
- 🐛 fix(telegram): improve telegram message logging
- 🐛 fix(gps): handle gpsd errors and fallback to env vars
- 🐛 fix(gps): ensure gpsd coordinates are set before return
- 🐛 fix(gps): increase gpsdclient timeout
- 🐛 fix(main): correct ais header sending frequency
- 🐛 fix(telemetry): correct cpu temp decimal places
- 🐛 fix(telemetry): improve telegram logs format
- 🐛 fix(telemetry): fix telemetry sending without await
- 🐛 fix(main): correct async call for send_position
- 🐛 fix(telegram): correct telegram token env variable name
- 🐛 fix(gps): correct .env quoting for gps coordinates
- 🐛 fix(position): correct lat/lon conversion in send_position
- 🐛 fix(gps): correct return type for get_gpsd_coordinate
- 🐛 fix(position): correct lat/lon to integer
- 🐛 fix(config): correct data type for aprs coordinates
- 🐛 fix(gpsd): correct gpsd coordinate retrieval and handling
- 🐛 fix(gpsd): improve gpsd coordinate retrieval logic
- 🐛 fix(gps): ensure valid gpsd data before processing
- 🐛 fix(cli): exit gracefully on keyboard interrupt
- 🐛 fix(gps): handle gpsd coordinate retrieval
- 🐛 fix(deps): update gpsdclient import
- 🐛 fix(gps): correct latitude and longitude type in gpsd
- 🐛 fix(gps): increase GPSDClient timeout
- 🐛 fix(main): correct log and sequence file paths
- 🐛 fix(config): correct logging call in config class
- 🐛 fix(logging): correct log file path
- 🐛 fix(gps): correct conditional statement in coordinate validation
- 🐛 fix(gps): handle gpsd no fix scenario
- 🐛 fix(config): correct logging configuration
- 🐛 fix(modemmanager): handle missing return
- 🐛 fix(gps): fix coordinate return on exception
- 🐛 fix(mmcli): correct modem index usage in location retrieval
- 🐛 fix(aprs): correct modemmanager coordinates and aprs position
- 🐛 fix(gps): correct return statement indentation
- 🐛 fix(gps): fix gpsd coordinate return
- 🐛 fix(gps): correct coordinate handling when GPSD data is invalid
- 🐛 fix(gps): fix return statement in get_gpsd_coordinate function
- 🐛 fix(gps): fix config write when gpsd data is valid
- 🐛 fix(gps): correct typo in gpsd coordinate retrieval
- ♻️ refactor(gps): improve gps data retrieval
- 🐛 fix(gps): correct return statement placement
- 🐛 fix(gps): correct mmcli execution path
- 🐛 fix(gps): correct gps data retrieval
- 🐛 fix(gps): correct script execution path in gps data retrieval
- 🐛 fix(gps): correct mmcli execution path
- 🐛 fix(gps): correct gps data retrieval script execution
- 🐛 fix(gps): correct path for mmcli_loc_get.sh execution
- 🐛 fix(logging): enable timed rotating file handler for logs
- 🐛 fix(logging): disable log rotation to resolve file permission issue
- 🐛 fix(gps): improve gps data logging format
- 🐛 fix(main.sh): add virtual environment setup and dependency installation
- 🐛 fix(gpsd): add enable option to GPSD configuration and adjust sleep timing
- revert [9da0215](https://github.com/HafiziRuslan/raspiaprs/commit/9da02157025d350bb65a93f5dc9bb23fc1a2bb4b)
- 🐛 fix(config): simplify GPSD enable check in configuration
- 🐛 fix(gpsd): add enable option to GPSD configuration
- 🐛 fix(config): update gps device path
- 🐛 fix(raspiaprs): remove unused gpsd device option
- 🐛 fix: correct telemetry data order
- 🐛 fix(raspiaprs): correct telemetry format
- 🐛 fix(telemetry): correct time format in telemetry string
- 🐛 fix(aprs): correct uptime format for aprs
- 🐛 fix(telemetry): improve uptime formatting and connection stability
- 🐛 fix(telemetry): correct status message format
- 🐛 fix(position): correct aprs position format
- 🐛 fix(position): correct altitude formatting in APRS payload
- 🐛 fix(position): correct altitude formatting in APRS payload
- 🐛 fix(position): correct aprs packet format
- 🐛 fix(aprs): correct string formatting in aprs script
- 🐛 fix(dmr): correct XLX master identification
- 🐛 fix(raspiaprs): remove redundant pass statements
- 🐛 fix(dmr): correct dmrmaster count check
- 🐛 fix(dmr): correct dmr master string formatting
- 🐛 fix(raspiaprs): update radio mode names and telemetry format
- 🐛 fix(raspiaprs): correct telemetry format for modes
- 🐛 fix(config): use fallback for configparser get
- 🐛 fix(raspiaprs): correct parameter names in header
- 🐛 fix(config): simplify MMDVM mode detection
- 🐛 fix(raspiaprs): remove AX.25 from MMDVM mode check and telemetry
- 🐛 fix(systemd): ensure network is online before starting service
- 🐛 fix(systemd): ensure network is available before starting service
- 📝 docs(README): simplify systemctl commands
- 🐛 fix(logging): improve reflector log parsing
- 🐛 fix(systemd): adjust service restart limits
- 🐛 fix(dmr): improve dmr master connection string
- 🐛 fix(raspiaprs): Correctly parse DMR master and reflector information
- 🐛 fix(raspiaprs): correct dmr master connection string
- 🐛 fix(raspiaprs): correct DMR master log parsing
- 🐛 fix(raspiaprs): correct regex for XLX identification
- 🐛 fix(raspiaprs): remove unused DMR master DC log parsing
- 🐛 fix(raspiaprs): correct DMR master parsing logic
- 🐛 fix(raspiaprs): Correctly handle DMR master data processing
- 🐛 fix(uptime): remove timezone specifier from uptime string
- 🐛 fix(vnstat): correct parsing of vnstat output
- 🐛 fix(raspiaprs): correct DMR master connection string and position comment
- 🐛 fix(raspiaprs): improve DMR master connection logic
- 🐛 fix(dmr): correct config parsing for dmrgw
- 🐛 fix(dmr): correctly handle DMR master string formatting
- 🐛 fix(raspiaprs): correct XLX DC identification in dmrmaster
- 🐛 fix(dmr): ensure cc is empty when dmr is disabled
- 🐛 fix(dmr): improve dmrgw master detection and handling
- 🐛 fix(traffic): improve network traffic reporting
- 🐛 fix(raspiaprs): sort dmrmasters correctly
- 🐛 fix(raspiaprs): improve DMR master display
- 🐛 fix(raspiaprs): correctly parse DMR master logs
- 🐛 fix(raspiaprs): correctly assign software version
- 🐛 fix(raspiaprs): improve DMR master parsing
- 🐛 fix(raspiaprs): resolve dmrmaster data duplication
- 🐛 fix(dmr): correct dmrmaster parsing logic
- 🐛 fix(raspiaprs): correctly parse DMR master calls
- 🐛 fix(raspiaprs): correct master parsing logic
- 🐛 fix(raspiaprs): correct DMRS master connection string formatting
- 🐛 fix(service): adjust service restart and startup behavior
- 🐛 fix(osinfo): correct Pi-Star/WPSD version string format
- 🐛 fix(osinfo): correct os info formatting
- 🐛 fix(config): resolve passcode retrieval from config file
- 🐛 fix(telemetry): correct formatting of aprs comment field
- 🐛 fix(telemetry): correct data type for traffic value
- 🐛 fix(config): correct passcode retrieval from config file
- 🐛 fix(traffic): correct index for traffic statistics
- 🐛 fix(traffic): correct traffic data type and add logging for sleep
- 🐛 fix(aprs): correct uptime format
- 🐛 fix(general): correct uptime format
- 🐛 fix(telemetry): correct uptime string format
- 🐛 fix(aprs): correct uptime format and add timestamp
- 🐛 fix(aprs): correct EQNS format in send_header
- 🐛 fix(ax.25): correct aprs header equations
- 🐛 fix(telemetry): correct callsign format in telemetry string
- 🐛 fix(telemetry): correct format string in send_header and main
- 🐛 fix(telemetry): correct callsign formatting in aprs messages
- 🐛 fix(telemetry): correct string formatting in telemetry and uptime messages
- 🐛 fix(main): correct uptime string and randomize sleep
- 🐛 fix(aprs): improve uptime format for readability
- Fix get_uptime function: move current time retrieval above uptime calculation for accurate display
- Fix send_header function: update parameter names for consistency in data transmission
- Fix get_modem function: replace subprocess.run with check_output for improved output handling
- Fix get_modem function: update subprocess.run to capture stdout for better error handling
- Fix get_modem function: update datetime usage for log file naming and replace check_output with run for better error handling
- Fix get_freemem function: ensure return value is an integer for accurate free memory percentage
- Fix get_load function: ensure return value is an integer for accurate load percentage
- Fix formatting in rpiaprs.conf: adjust spacing for password and filter comments
- Fix get_freemem function: adjust memory calculation for more precise free memory percentage
- Fix get_freemem function: correct memory calculation by adjusting cache memory division
- Fix get_load function: convert core count to float for accurate CPU load calculation
- Update get_osinfo function: fix kernel and OS version retrieval logic for accurate output
- Fix send_header function: update EQNS parameter for improved precision
- Fix formatting issue in default configuration: separate 'sleep' value from 'pip'
- Fix logging message and adjust indentation in get_uptime function
- Merge pull request #2 from 0x9900/fred/senderror
- fix connection error

### 💼 Other

- Update CHANGELOG
- Update CHANGELOG
- Update changelog
- Update changelog
- Merge branch 'master' of [RasPiAPRS](https://github.com/HafiziRuslan/RasPiAPRS)
- Merge branch 'master' of [RasPiAPRS](https://github.com/HafiziRuslan/RasPiAPRS)
- run changelog on push
- [Changelog CI] Add Changelog for Version ae1c38ed31d5d068814908845ff28e5e766d8146
- Update Python versions in pylint workflow
- Set package-ecosystem to 'pip' in dependabot config
- Delete .github/workflows/pylint.yml
- Merge branch 'master' of [RasPiAPRS](https://github.com/HafiziRuslan/RasPiAPRS)
- Add Pylint workflow for Python code analysis
- Merge pull request #2 from HafiziRuslan/virtual-env
- Add GitHub Actions workflow to sync with GitLab
- Add source reference to README: include link to aprstar repository
- Add new LICENSE file: include BSD 2-Clause License with updated copyright information
- Remove ExecStartPre directive for 90-second delay in raspiaprs.service
- Update raspiaprs.service: increase RestartSec to 15 and add ExecStartPre for a 90-second delay
- Update SSID configuration: change default SSID from 1 to 10 in raspiaprs.conf and from 1 to 0 in raspiaprs.py
- Update configuration files: standardize call sign format and improve comments in raspiaprs.conf and raspiaprs.py
- Refactor project structure: rename files and update configuration for consistency
- Update README.md: enhance clarity and formatting in installation and usage instructions
- Refactor memory and load calculations: improve accuracy in get_load and get_freemem functions
- Update load and memory functions: improve CPU load calculation and refine memory usage metrics
- Update get_osinfo function: adjust OS version formatting for improved readability
- Update README.md: add update instructions for RPi-APRS service
- Update main function: change telemetry data structure from dictionary to string format for improved clarity
- Refactor main function: replace data structure with individual sends for telemetry and uptime, improve logging
- Update main function: change data structure from list to dictionary for improved clarity and logging
- Update get_osinfo function: refine kernel and OS version retrieval logic for improved accuracy
- Update get_osinfo function: enhance kernel and OS version retrieval, improve error handling for PiStar and WPSD release files
- Update get_osinfo function: improve kernel version retrieval and handle exceptions for PiStar and WPSD release files
- Update rpiaprs.py: correct variable names for PiStar and WPSD release files and enhance version retrieval logic
- Refactor Config class: update server and port properties for clarity
- Update README.md: improve installation commands formatting and add troubleshooting tips
- Update README.md and rpiaprs.conf: improve clarity of installation instructions and configuration comments
- Update rpiaprs.conf: enhance comments for latitude, longitude, and altitude fields to improve clarity
- Update README.md: streamline installation instructions by consolidating commands
- Update README.md: improve installation instructions and clarify configuration steps
- Refactor memory and uptime reporting: simplify freemem return value, update piversion formatting, and enhance position packet comment structure
- Update packet comment format: change GitHub link to use HTTPS for improved security
- Update APRS-IS configuration: change password placeholder and modify filter setting
- Reorder packet comment format: move GitHub link to the front for better visibility
- Improve DMR frequency shift display: add conditional formatting for TX/RX frequency differences
- Update send_header call frequency: change condition to every 10th sequence
- Update README.md formatting and enhance rpiaprs.py comments: improve readability and add GitHub link
- Refactor configuration settings and improve logging: update default values and enhance error handling
- Update rpiaprs.service: remove Type=simple line for service configuration
- Update .gitignore to include aprstar-WIP.py file
- Update installation instructions and configuration files: streamline pip install command and correct default call sign
- Update send_position function: change tocall from "APP720" to "APP642"
- Update send_position function: change tocall from "APRS" to "APP720"
- Refactor aprstar.py: streamline imports, enhance logging, and improve configuration handling
- Refactor project structure: rename and update files for RPi-APRS, add configuration and service files
- Merge pull request #3 from 0x9900/fred/senderror
- Python 3
- Hardening ais connections
- Let's make it less verbose
- Create LICENSE
- Logging when the position is infered
- Casting the symbol into a string
- Example of telemetry
- Installation notes for pi-star
- readme...
- Adding the origin of aprstar
- How to install aprstar
- Making the code work on python 2 and 3
- Adding a readme file
- Send the header first when the program starts
- Adding FreeMemory metric
- Initial version

### 🚜 Refactor

- ♻️ refactor(system): clean up type conversions in system metric functions
- ♻️ refactor(config): improve readability and adhere to Python conventions
- ♻️ refactor(main): simplify header sending logic
- ♻️ refactor(dmr): improve dmr master retrieval logic
- ♻️ refactor(main): change send_header to async
- ♻️ refactor(location): remove modemmanager coordinates function
- ♻️ refactor(deps): move urllib import
- ♻️ refactor(main): consolidate imports and update dependencies
- ♻️ refactor(main): convert send_header to async
- ♻️ refactor(main): migrate Telegram logging to asynchronous
- ♻️ refactor(gps): improve gps coordinate handling
- ♻️ refactor(aprs): disable telegram integration
- ♻️ refactor(main): adjust transmission intervals for efficiency
- ♻️ refactor(gps): switch to modemmanager for gps data
- ♻️ refactor(readme): improve documentation clarity and update file paths
- ♻️ refactor: improve raspiaprs configuration and usage
- ♻️ refactor: remove unused import
- ♻️ refactor(raspiaprs): remove unused mode function and telemetry data
- ♻️ refactor: remove modem firmware retrieval
- ♻️ refactor(main): improve code readability and maintainability
- ♻️ refactor(sequence): simplify sequence file name
- Enhance uptime display: prepend current time to uptime string format
- Update README and refactor functions: clarify metrics terminology and rename functions for CPU load and memory usage
- Enhance modem firmware detection: update get_modem function to include additional modem descriptions and improve parsing logic
- Enhance modem information retrieval: update get_modem function and modify packet comment to include modem details
- Enhance rpiaprs configuration: add altitude parameter and improve comments for clarity

### 📚 Documentation

- 📝 docs(ci): standardize changelog file reference
- 📝 docs(changelog): adjust cliff configuration and release workflow
- docs: update CHANGELOG.md
- docs: update CHANGELOG.md
- docs(CHANGELOG): update release notes
- 👷 ci(workflows): streamline release and changelog generation
- 📝 docs(readme): rename README to README.md
- 📝 docs(readme): update license file reference
- 📝 docs(readme): update instructions for RasPiAPRS
- 📝 docs(README): improve installation and configuration instructions
- 📝 docs(readme): update dependencies in readme
- 📝 docs(README): add gpsd to dependency list
- 📝 docs(gitignore): add log folder to gitignore
- 📝 docs(config): update GPSD configuration
- 📝 docs(readme): remove unused metrics
- 📝 docs(main): add docstrings to functions and classes
- 📝 docs(README): update traffic metric description
- 📝 docs(readme): update installation path for raspiaprs
- 📝 docs(readme): correct service disable command order
- 📝 docs(readme): correct installation script paths
- 📝 docs(readme): simplify systemctl status command
- 📝 docs(readme): update service installation instructions
- Update README and rpiaprs.py: enhance documentation clarity and add default APRS-IS server settings

### ⚡ Performance

- ⚡️ perf(aprs): reduce precision for some telegram values
- ⚡️ perf(aprs): reduce precision for some EQNS values
- ⚡️ perf(aprs): reduce precision for some EQNS values
- ⚡️ perf(monitoring): remove unnecessary rounding in system metric calculations
- ⚡️ perf(main): improve ais message sending efficiency
- ⚡️ perf(raspiaprs): adjust random sleep duration
- ⚡️ perf(disk, memory): optimize disk and memory usage calculation
- Implement code changes to enhance functionality and improve performance

### 🧪 Testing

- 👷 ci(release): update GitHub Actions versions

### ⚙️ Miscellaneous Tasks

- 👷 ci(release): restructure workflow jobs
- 📦 build(ci): include requirements and environment file in release
- 📦 build(ci): simplify release asset upload
- 📦 build(ci): adjust file paths in release workflow
- 📦 build(ci): update release workflow to use workspace path
- 🔧 chore(ci): migrate release workflow to use git-cliff
- 👷 ci(pre-release): switch changelog generation action
- 👷 ci(pre-release): set explicit release version in workflow
- 👷 ci(workflow): switch to changelog-ci action
- 👷 ci(pre-release): remove redundant body append setting
- 🔧 chore(ci): remove deprecated changelog configuration
- 👷 ci(workflow): replace changelog generation action
- 👷 ci(pre-release): adjust changelog action input
- 🔧 chore(ci): adjust changelog action tag range
- 👷 ci(pre-release): use GITHUB_TOKEN for changelog action
- 👷 ci(pre-release): improve changelog generation workflow
- 👷 ci(release): adjust pre-release workflow condition
- 🔧 chore(ci): remove changelog workflow and update release process
- 👷 ci(workflows): update changelog flow type
- 👷 ci(workflows): update github actions workflow names and steps
- 👷 ci(workflow): include published event for changelog generation
- 👷 ci(workflows): update github action versions and release files
- 🔧 chore(ci): clean up unused and update GitHub workflows
- 👷 ci(release): add pre-release workflow
- 🔧 chore(ci): clean up obsolete and update workflow triggers
- 🔧 chore(ci): adjust changelog workflow configuration
- 👷 ci(workflows): add auto approve workflow for bots
- Merge pull request #3 from HafiziRuslan/changelog-ci-ae1c38
- 👷 ci(workflow): use commit hash as fallback release version
- 🔧 chore(ci): update changelog workflow inputs
- 🔧 chore(ci): enable manual release version input in changelog workflow
- 🔧 chore(ci): disable manual release version input in workflow
- 🔧 chore(ci): remove redundant changelog step
- 👷 ci(pylint): remove pylint workflow
- 🔧 chore(main): enhance logging and venv management
- 🔧 chore(config): remove logging of environment variables
- 🔧 chore(gitignore): update gitignore file
- 🔧 chore(gitignore): add log folder to gitignore
- 🔧 chore(gitignore): update .gitignore file
- 🔧 chore(gitignore): add vscode and logs to gitignore
- 🔧 chore(config): enhance logging and file path
- 🔧 chore(systemd): configure service restart behavior
- ✨ chore(script): remove raspiaprs.py
- 🔧 chore(gitignore): update .gitignore file
- 🔧 chore(gitignore): update .gitignore file
- 🔧 chore(main): rename raspiaprs.py to main.py
- 📦 build(deps): add new project dependencies
- 🔧 chore(gitignore): add .vscode to gitignore
- 🔧 chore(raspiaprs): reorganize file path definitions and clean up unused code
- 🔧 chore(systemd): improve raspiaprs.service configuration
- 🔧 chore(scripts): remove unused import
- 🔧 chore(raspiaprs.py): simplify DMR master logging
- 🔧 chore(files): update file paths and remove sleep from service
- 📦 build(systemd): delay raspiaprs start
- Update rpiaprs.conf: clarify altitude comment to specify AGL (Above Ground Level)
- Update uptime display format: abbreviate time units and remove unnecessary precision
- Remove aprstar.py file: eliminate unused code and dependencies
- The symbol and symbol table can be speicified in the config

### ◀️ Revert

- revert to ec381c1

---

generated using git-cliff - (2025-12-11T08:50:22.122385110+08:00)
