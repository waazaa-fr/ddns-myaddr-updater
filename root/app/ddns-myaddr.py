import requests
import time
import os
import threading
import logging
import yaml
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log_lock = threading.Lock()  # Création d'un verrou pour les logs

# Charge le fichier de configuration
def load_config(file_path='/config/config.yml'):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_public_ip(version):
    if version == 'ipv4':
        return requests.get('https://api.ipify.org').text.strip()
    elif version == 'ipv6':
        return requests.get('https://api64.ipify.org').text.strip()
    return None

def update_ip(api_key, ip):
    url = 'https://myaddr.tools/update'
    data = {'ip': ip, 'key': api_key}
    response = requests.post(url, data=data)
    return response.text

def process_configuration(name, config):
    last_ipv4               = None
    last_ipv6               = None
    last_update_ipv4_time   = datetime.now() - timedelta(days=config['NO_UPDATE_LIMIT'])
    last_update_ipv6_time   = datetime.now() - timedelta(days=config['NO_UPDATE_LIMIT'])
    api_key                 = config['KEY']
    while True:
        current_time = datetime.now()
        
        # Traitement de l'IPv4
        ipv4_action = config['IPv4']
        if ipv4_action == 'auto':
            public_ipv4 = get_public_ip('ipv4')
            if public_ipv4 != last_ipv4 and public_ipv4:
                result = update_ip(api_key, public_ipv4)
                with log_lock:  # Utiliser le verrou pour synchroniser les logs
                    logging.info(f"{name} - IPv4 updated : {public_ipv4}, Response : {result}")
                last_ipv4 = public_ipv4
                last_update_ipv4_time = current_time
        elif ipv4_action != 'none':  # Privé une IPv4
            if ipv4_action != last_ipv4 and current_time - last_update_ipv4_time > timedelta(days=config['NO_UPDATE_LIMIT']):
                result = update_ip(api_key, ipv4_action)
                with log_lock:  # Utiliser le verrou pour synchroniser les logs
                    logging.info(f"{name} - IPv4 set to : {ipv4_action}, Response : {result}")
                last_ipv4 = ipv4_action
                last_update_ipv4_time = current_time

        # Traitement de l'IPv6
        ipv6_action = config['IPv6']
        if ipv6_action == 'auto':
            public_ipv6 = get_public_ip('ipv6')
            if public_ipv6 != last_ipv6 and public_ipv6:
                result = update_ip(api_key, public_ipv6)
                with log_lock:  # Utiliser le verrou pour synchroniser les logs
                    logging.info(f"{name} - IPv6 updated : {public_ipv6}, Response : {result}")
                last_ipv6 = public_ipv6
                last_update_ipv6_time = current_time
        elif ipv6_action != 'none':  # Privé une IPv6
            if ipv6_action != last_ipv6 and current_time - last_update_ipv6_time > timedelta(days=config['NO_UPDATE_LIMIT']):
                result = update_ip(api_key, ipv6_action)
                with log_lock:  # Utiliser le verrou pour synchroniser les logs
                    logging.info(f"{name} - IPv6 set to : {ipv6_action}, Response : {result}")
                last_ipv6 = ipv6_action
                last_update_ipv6_time = current_time
        
        time.sleep(15 * 60)  # Vérifie tous les 15 minutes

if __name__ == '__main__':
    configurations = load_config()

    threads = []
    try:
        for config_name, config in configurations.items():
            thread = threading.Thread(target=process_configuration, args=(config_name, config))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        logging.info("Arrêt du script en cours...")
        # Optionnel : tu peux ajouter une logique pour arrêter les threads proprement si nécessaire.
        for thread in threads:
            thread.join(timeout=1)  # Attendre un peu pour que les threads finissent
        logging.info("Script arrêté.")