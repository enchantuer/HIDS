import os
import json

CONFIG_PATH = "config.json"

# Valeurs par défaut au cas où le fichier est absent
default_config = {
    "YARA": True,
    "SURICATA": True,
    "SNORT": True,
    "VIRUS_TOTAL": True,
    "IPDB": True,
    "IA": True,
    "RANDOM_FOREST": True,
    "SUPPORT_VECTOR_MACHINE": True
}

# Charger la config depuis le JSON
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        user_config = json.load(f)
else:
    user_config = {}

# Fusionner avec les valeurs par défaut
config = {**default_config, **user_config}

# Utilisable ailleurs
YARA = config["YARA"],
SURICATA = config["SURICATA"],
SNORT = config["SNORT"],
VIRUS_TOTAL = config["VIRUS_TOTAL"],
IPDB = config["IPDB"],
IA = config["IA"]
RANDOM_FOREST = config["RANDOM_FOREST"]
SUPPORT_VECTOR_MACHINE = config["SUPPORT_VECTOR_MACHINE"]

# Clés API via variables d'environnement
VT_API_KEY = os.environ.get("VT_API_KEY")
ABUSEIPDB_API_KEY = os.environ.get("ABUSEIPDB_API_KEY")
