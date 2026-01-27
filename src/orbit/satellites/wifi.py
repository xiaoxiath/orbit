"""WiFi management satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser, JSONResultParser
import json


# Connect to WiFi
wifi_connect = Satellite(
    name="wifi_connect",
    description="Connect to WiFi network",
    category="wifi",
    parameters=[
        SatelliteParameter(
            name="ssid",
            type="string",
            description="Network SSID",
            required=True
        ),
        SatelliteParameter(
            name="password",
            type="string",
            description="Network password",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set networkSSID to "{{ ssid }}"
    {% if password %}
    do shell script "networksetup -setairportnetwork en0 {{ ssid }} {{ password }}"
    {% else %}
    do shell script "networksetup -setairportnetwork en0 {{ ssid }}"
    {% endif %}

    delay 2

    return "success"
    """,
    examples=[
        {
            "input": {"ssid": "MyNetwork", "password": "password123"},
            "output": "success"
        }
    ]
)

# Disconnect WiFi
wifi_disconnect = Satellite(
    name="wifi_disconnect",
    description="Disconnect from current WiFi",
    category="wifi",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    do shell script "networksetup -setairportnetwork en0 off"
    delay 1
    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# List available networks
wifi_list = Satellite(
    name="wifi_list",
    description="List available WiFi networks",
    category="wifi",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set scanResults to do shell script("/System/Library/Private/Apple80211/Versions/Current/airport -s | grep -v 'BSSID' | grep -v 'SSID'")

    return scanResults
    """,
    result_parser=lambda x: [line.strip() for line in x.split("\n") if line.strip()] if x else [],
    examples=[
        {
            "input": {},
            "output": {"networks": ["Network1", "Network2"]}
        }
    ]
)

# Get current WiFi info
wifi_current = Satellite(
    name="wifi_current",
    description="Get current WiFi connection info",
    category="wifi",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set wifiInfo to do shell script("/System/Library/Private/Apple80211/Versions/Current/airport -I | grep '     AgrNegRssi:'")

    set ssid to do shell script("/System/Library/Private/Apple80211/Versions/Current/airport -I | grep '     SSID:'")

    return ssid & "|" & wifiInfo
    """,
    result_parser=DelimitedResultParser(delimiter="|", field_names=["ssid", "signal_strength"]),
    examples=[
        {
            "input": {},
            "output": {"ssid": "MyNetwork", "signal_strength": "-45"}
        }
    ]
)

# Turn WiFi on/off
wifi_turn_on = Satellite(
    name="wifi_turn_on",
    description="Turn WiFi on",
    category="wifi",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    do shell script "networksetup -setairportpower on"
    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

wifi_turn_off = Satellite(
    name="wifi_turn_off",
    description="Turn WiFi off",
    category="wifi",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    do shell script "networksetup -setairportpower off"
    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Export all wifi satellites
__all__ = [
    "wifi_connect",
    "wifi_disconnect",
    "wifi_list",
    "wifi_current",
    "wifi_turn_on",
    "wifi_turn_off",
]
