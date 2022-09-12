# Webpage Monitor Integration For Home Assistant
[![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white)](https://www.home-assistant.io/)
![Tested on](https://img.shields.io/badge/tested%20on-2022.5-%2341BDF5.svg?style=for-the-badge)
[![Maintainer](https://img.shields.io/badge/maintainer-Nikolai%20Eidsheim%20%40eidsheim98-blue.svg?style=for-the-badge)](https://github.com/eidsheim98)

# THIS SOFTWARE IS CURRENTLY UNDER TESTING AND MAY NOT WORK CORRECTLY

This integration lets you monitor both internal and external URLs to check if they are accessible. This can be used as a more reliable alternative instead of pinging.

## Installation

### Option 1: HACS
1. Under HACS -> Integrations, select `+`, search for `webpage-monitor`, and install.
2. Restart Home Assistant
3. Configure configuration.yaml with data TODO
4. Restart Home Assistant again

### Option 2: MANUALLY
```bash
cd YOUR_HASS_CONFIG_DIRECTORY    # same place as configuration.yaml
mkdir -p custom_components/webpage-monitor
cd custom_components/webpage-monitor
unzip webpage-monitor-X.Y.Z.zip
mv webpage-monitor-X.Y.Z/custom_components/webpage-monitor/* .  
```

## Usage
### YAML
Insert into configuration.yaml
```yaml
sensor:
  - platform: webpage-monitor
    entities:
    - name: WebPageName
      data:
        - WebPageIPaddress or WebAddress
        - WebPagePort
```

This means that for checking if Google is down:

```yaml
sensor:
  - platform: webpage-monitor
    entities:
    - name: Google
      data:
        - google.com
        - 80
```

Or for checking a web server on the same machine running on port 5000:

```yaml
sensor:
  - platform: webpage-monitor
    entities:
    - name: Server
      data:
        - 127.0.0.1
        - 5000
```

You can continue this with as many entity entries as you want. If no port is provided, port 80 will be used as default for HTTP, and 443 for HTTPS


## Current Support
* Internal and external URLs
* HTTP and HTTPS