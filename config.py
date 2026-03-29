# config.py
IPINFO_TOKEN = "6eb6a1f3c36e0f"


JUNIPER_DEVICES = {
    "NDU-OPT1": {
        "host": "101.53.0.51",
        "device_type": "juniper_junos", 
    },
    "NTK-OPT1": {
        "host": "101.53.0.52",
        "device_type": "juniper_junos",
    },
    "NTK-OPT2": {
        "host": "101.53.0.97",
        "device_type": "juniper_junos",
    }
}

DEFAULT_OPTIMIZER_DEVICES = ["NDU-OPT1", "NTK-OPT1"]

PREFIX_DEVICE_MAPPING = {
    '101.53.6.0/24': ['NTK-OPT2'],
    '101.53.12.0/24': ['NTK-OPT2'],
    '101.53.21.0/24': ['NTK-OPT2'],
    '210.86.238.0/24': ['NTK-OPT2'],
}

UPSTREAM_PREFIX_LISTS = {
    "VIETTEL-QT (101.53.60.0)": "Vietel-IXP-Dest",
    "CMC-QT (101.53.50.0)": "CMC-IXP-Dest",
    "VNPT-QT (119.15.178.0)": "VNPT-IXP-Dest",
    "NTT-HKG (101.53.55.0)": "NTT-Dest",
    "IPTP-SG (119.17.238.0)": "IPTP-SG-Dest",
    "IPTP-HKG (101.53.63.0)": "IPTP-Dest",
    "LUMEN-HK (101.53.46.0)": "LUMEN-HKG-Dest",
    "LUMEN-SGP (101.53.48.0)": "Lumen-SGP-Dest",
}
ISP_SUGGESTION_KEYWORDS = {
    "VIETTEL": "VIETTEL-QT",
    "CMC": "CMC-QT",
    "VNPT": "VNPT-QT",
    "GOOGLE": "google-peering",  
    "CLOUDFLARE": "cloudflare-peering",
    "AMAZON": "aws-peering",
    "NTT": "NTT-HKG",
}

JUNIPER_USERS = [
    "long.dm",
    "thien.nm",
    "nhat.nm",
    "hai.nt1",
    "vu.th",
]

INBOUND_PREFIXES = {
    '101.53.58.0/24': '101.53.58.0/24',
    '101.53.50.0/24': '101.53.50.0/24',
    '101.53.1.0/24': '101.53.1.0/24',  
    '101.53.3.0/24': '101.53.3.0/24',  
    '101.53.4.0/24': '101.53.4.0/24',
    '101.53.5.0/24': '101.53.5.0/24',
    '101.53.6.0/24': '101.53.6.0/24',
    '101.53.7.0/24': '101.53.7.0/24', 
    '101.53.8.0/24': '101.53.8.0/24', 
    '101.53.9.0/24': '101.53.9.0/24',
    '101.53.10.0/24': '101.53.10.0/24',
    '101.53.11.0/24': '101.53.11.0/24',
    '101.53.12.0/24': '101.53.12.0/24',
    '101.53.13.0/24': '101.53.13.0/24',
    '101.53.14.0/24': '101.53.14.0/24',
    '101.53.15.0/24': '101.53.15.0/24',
    '101.53.16.0/24': '101.53.16.0/24',
    '101.53.17.0/24': '101.53.17.0/24',
    '101.53.18.0/24': '101.53.18.0/24',
    '101.53.19.0/24': '101.53.19.0/24',
    '101.53.20.0/24': '101.53.20.0/24',
    '101.53.21.0/24': '101.53.21.0/24',
    '101.53.22.0/24': '101.53.22.0/24',
    '101.53.23.0/24': '101.53.23.0/24',
    '101.53.24.0/24': '101.53.24.0/24',
    '101.53.25.0/24': '101.53.25.0/24',
    '101.53.26.0/24': '101.53.26.0/24',
    '101.53.27.0/24': '101.53.27.0/24',
    '101.53.28.0/24': '101.53.28.0/24',
    '101.53.29.0/24': '101.53.29.0/24',
    '101.53.30.0/24': '101.53.30.0/24',
    '101.53.31.0/24': '101.53.31.0/24',
    '101.53.32.0/24': '101.53.32.0/24',
    '101.53.33.0/24': '101.53.33.0/24',
    '101.53.34.0/24': '101.53.34.0/24',
    '101.53.35.0/24': '101.53.35.0/24',
    '101.53.36.0/24': '101.53.36.0/24',
    '101.53.37.0/24': '101.53.37.0/24',
    '101.53.38.0/24': '101.53.38.0/24',
    '101.53.39.0/24': '101.53.39.0/24',
    '101.53.40.0/24': '101.53.40.0/24',
    '101.53.41.0/24': '101.53.41.0/24',
    '101.53.42.0/24': '101.53.42.0/24',
    '101.53.43.0/24': '101.53.43.0/24',
    '101.53.44.0/24': '101.53.44.0/24',
    '101.53.45.0/24': '101.53.45.0/24', 
    '101.53.47.0/24': '101.53.47.0/24',
    '101.53.49.0/24': '101.53.49.0/24',
    '101.53.51.0/24': '101.53.51.0/24',    
    '101.53.52.0/24': '101.53.52.0/24',
    '101.53.53.0/24': '101.53.53.0/24',
    '101.53.56.0/24': '101.53.56.0/24',
    '101.53.61.0/24': '101.53.61.0/24',
    '101.53.62.0/24': '101.53.62.0/24',
    '103.88.122.0/24': '103.88.122.0/24',
    '119.15.176.0/24': '119.15.176.0/24',
    '119.15.177.0/24': '119.15.177.0/24',
    '119.15.179.0/24': '119.15.179.0/24',
    '119.15.180.0/24': '119.15.180.0/24',
    '119.15.181.0/24': '119.15.181.0/24',
    '119.15.185.0/24': '119.15.185.0/24',
    '119.15.188.0/24': '119.15.188.0/24',
    '119.15.190.0/24': '119.15.190.0/24',
    '119.15.191.0/24': '119.15.191.0/24',
    '119.17.229.0/24': '119.17.229.0/24',
    '119.17.232.0/24': '119.17.232.0/24',
    '119.17.234.0/24': '119.17.234.0/24',
    '119.17.235.0/24': '119.17.235.0/24',
    '119.17.236.0/24': '119.17.236.0/24',
    '119.17.237.0/24': '119.17.237.0/24',
    '119.17.239.0/24': '119.17.239.0/24',
    '119.17.240.0/24': '119.17.240.0/24',
    '119.17.241.0/24': '119.17.241.0/24',
    '119.17.247.0/24': '119.17.247.0/24',
    '119.17.249.0/24': '119.17.249.0/24',
    '119.17.252.0/24': '119.17.252.0/24',
    '119.17.254.0/24': '119.17.254.0/24',
    '202.151.170.0/24': '202.151.170.0/24',
    '202.151.171.0/24': '202.151.171.0/24',
    '202.151.172.0/24': '202.151.172.0/24',
    '202.151.173.0/24': '202.151.173.0/24',
    '202.151.174.0/24': '202.151.174.0/24',
    '202.151.175.0/24': '202.151.175.0/24',
    '202.151.175.0/24': '202.151.175.0/24',
    '210.86.227.0/24': '210.86.227.0/24',
    '210.86.234.0/24': '210.86.234.0/24',
    '210.86.235.0/24': '210.86.235.0/24',
    '210.86.237.0/24': '210.86.237.0/24',
    '210.86.238.0/24': '210.86.238.0/24'
}

BGP_COMMUNITIES = {
    "VIETTEL-QT": {
        "announce": {"description": "Advertise","community": "65031:7552"},
        "prepend": {"description": "Prepend AS-Path","community": "65033:7552"},
        "do_not_announce": {"description": "No Advertise","community": "65030:7552"}
    },
    "VNPT-QT": {
        "announce": { "community": "65031:45899", "description": "Advertise" },
        "prepend": { "community": "65033:45899", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:45899", "description": "No Advertise"}
    },
    "CMC-QT": {
        "announce": { "community": "65031:45903", "description": "Advertise" },
        "prepend": { "community": "65033:45903", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:45903", "description": "No Advertise"}
    },
    "PNI-AWS": {
        "announce": { "community": "65031:16509", "description": "Advertise" },
        "prepend": { "community": "65033:16509", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:16509", "description": "No Advertise"}
    },
    "Equinix-Sing": {
        "announce": { "community": "65131:24115", "description": "Advertise" },
        "prepend": { "community": "65133:24115", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:24115", "description": "No Advertise"}
    },
    "Equinix-HK": {
        "announce": { "community": "65031:24115", "description": "Advertise" },
        "prepend": { "community": "65033:24115", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:24115", "description": "No Advertise"}
    },
    "Facebook-Cache-SGN": {
        "announce": { "community": "65131:63293", "description": "Advertise" },
        "do_not_announce": { "community": "65130:63293", "description": "No Advertise"}
    },
    "Google-Cache-SGN": {
        "announce": { "community": "65031:65535", "description": "Advertise" },
        "prepend": { "community": "65033:65535", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:65535", "description": "No Advertise"}
    },
    "Google-Sing": {
        "announce": { "community": "65131:15169", "description": "Advertise" },
        "prepend": { "community": "65133:15169", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:15169", "description": "No Advertise"}
    },
    "Google-HK": {
        "announce": { "community": "65031:15169", "description": "Advertise" },
        "prepend": { "community": "65033:15169", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:15169", "description": "No Advertise"}
    },
    "IPTP-Sing": {
        "announce": { "community": "65131:41095", "description": "Advertise" },
        "prepend": { "community": "65133:41095", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:41095", "description": "No Advertise"}
    },
    "IPTP-Taiwan": {
        "announce": { "community": "65031:14095", "description": "Advertise" },
        "prepend": { "community": "65033:14095", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:14095", "description": "No Advertise"}
    },
    "IPTP-HK": {
        "announce": { "community": "65031:41095", "description": "Advertise" },
        "prepend": { "community": "65033:41095", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:41095", "description": "No Advertise"}
    },
    "LUMEN-HK": {
        "announce": { "community": "65021:3356", "description": "Advertise" },
        "prepend": { "community": "65023:3356", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65020:3356", "description": "No Advertise"}
    },
    "META-HNI": {
        "announce": { "community": "65111:32934", "description": "Advertise" },
        "prepend": { "community": "65113:32934", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65110:32934", "description": "No Advertise"}
    },
    "META-SGN": {
        "announce": { "community": "65131:32934", "description": "Advertise" },
        "prepend": { "community": "65133:32934", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:32934", "description": "No Advertise"}
    },
    "PNI-Microsoft": {
        "announce": { "community": "65031:8075", "description": "Advertise" },
        "prepend": { "community": "65033:8075", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:8075", "description": "No Advertise"}
    },
    "NTT-HK": {
        "announce": { "community": "65031:2914", "description": "Advertise" },
        "prepend": { "community": "65033:2914", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65030:2914", "description": "No Advertise"}
    },
    "VNPT-TN": {
        "announce": { "community": "65131:45899", "description": "Advertise" },
        "prepend": { "community": "65133:45899", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:45899", "description": "No Advertise"}
    },
    "VIETTEL-TN": {
        "announce": { "community": "65131:7552", "description": "Advertise" },
        "prepend": { "community": " 65133:7552", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": " 65130:7552", "description": "No Advertise"}
    },
    "LUMEN-SGP": {
        "announce": { "community": "65131:3356", "description": "Advertise" },
        "prepend": { "community": "65133:3356", "description": "Prepend AS-Path" },
        "do_not_announce": { "community": "65130:3356", "description": "No Advertise"}
    },
}