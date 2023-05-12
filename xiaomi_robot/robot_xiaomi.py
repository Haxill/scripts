'''
########################################################################################################################################
# Created by : HAXILL                                                                                                                  #
# Engine     : python-miio, scapy                                                                                                      #
# Date       : 18/04/2023                                                                                                              #
# Version    : 03/05/2023                                                                                                              #
# OS         : Windows                                                                                                                 #
# Langue     : French                                                                                                                  #
# Script     : Ce script permet de communiquer avec l'aspirateur robot 'Mi Robot Vacuum-Mop 2 Pro' et de programmer des heures de      #
#              passages lorsque vous êtes absent de la maison uniquement. A adapter selon modèle du robot.                             #
########################################################################################################################################
'''

import miio # pip install netifaces python-miio
from miio import RoidmiVacuumMiot
import datetime
import time
import os
from scapy.all import ARP, Ether, srp

# Adresse IP et token de mon aspirateur robot Xiaomi
ip = "192.168.1.128"
token = "TOKEN" # Télécharger 'Get.token.exe' pour l'obtenir facilement
# Mon téléphone Xiaomi
telephone = "192.168.1.122"
# Mon adresse mac du téléphone Xiaomi
adresseMac = "AB:CD:EF:AB:CD:EF"

# Initialisation du booléen de passage de l'aspirateur ce jour
aspiAujourdhui = False
# Initialisation du booléen de détection de présence
isconnected = False
# Initialisation du booléen indiquant si le robot fait le ménage ou non
nettoyage = False

# Heure de réinitialisation (minuit = 0:0)
reinitH = 0  # Heure
reinitM = 0  # Minutes

# Connexion à l'aspirateur robot Xiaomi
aspirobot = RoidmiVacuumMiot(ip, token)

# Fonction de démarrage de l'aspirateur ou de retour au dock
def aspiStartRetour():
    if not isconnected :
        print("Démmarage du robot.\n")
        aspirobot.start()
    else:
        aspirobot.home()


while True:
    # Obtention de la date actuelle
    now = datetime.datetime.now()
    # Extraction de la date et l'heure pour chatGPT
    year = now.year
    mois_list = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    mois = mois_list[now.month]
    jour = now.day
    heure = now.hour
    minutes = now.minute

    if heure == reinitH and minutes == reinitM:
        aspiAujourdhui = False # On réinitialise si l'aspirateur est déjà passé

    # Vérification de ma présence à la maison
    # Création d'une requête ARP
    arp = ARP(pdst=telephone)
    # Création d'une trame Ethernet avec l'@MAC du téléphone
    ether = Ether(dst=adresseMac)
    # Fusion de la requête et de la trame
    packet = ether/arp
    # Envoie de la requête ARP et récupération des réponses
    result = srp(packet, timeout=2, verbose=0)[0]
    result = srp(packet, timeout=2, verbose=0)[0]
    
    # Récupération des informations de l'aspirateur et traitement des erreurs
    try:
        status = aspirobot.status()
    except miio.exceptions.RecoverableError:
        status = aspirobot.status()
    except miio.exceptions.DeviceException:
        status = aspirobot.status()

    os.system("cls")

    try:
        # Obtention du niveau de batterie
        battery_level = status.battery
        # Détermination de l'action en cours du robot
        is_on = status.is_on
        if not is_on:
            is_on = "Nettoyage en cours..." # False
            nettoyage = True
        else:
            if battery_level < 100:
                is_on = "En charge..." # True
            else:
                is_on = "En veille"
            nettoyage = False
    except Exception as e:
        print("Une erreur s'est produite :")
        print(e)

    # Analyse de la réponse à la requête
    if len(result) > 0:
        isconnected = True # Présent
    else:
        isconnected = False # Absent

    if not isconnected: # Pas de présence détectée
        current_time = datetime.datetime.now()  
        if heure == 13 and minutes == 30 and not aspiAujourdhui: # 1er essai à une heure donnée
            aspiStartRetour()
            aspiAujourdhui = True
        elif heure == 15 and minutes == 30 and not aspiAujourdhui: # 2eme essai si l'aspirateur n'a pas démarré au premier horaire
            aspiStartRetour()
            aspiAujourdhui = True
        else:
            os.system("cls")
            print("\nSTATUS DU ROBOT ASPIRATEUR :")
            print("\n   - Etat : {}".format(is_on))
            print("   - Niveau de batterie : {}%".format(battery_level))
            if nettoyage:
                print("\nPersonne dans les parrages. Passage de l'aspirateur en cours...\n\n")
            else:
                print("\nPersonne dans les parrages.")
    else: # Présence détectée
        os.system("cls")
        if nettoyage:
            aspiStartRetour()
            os.system("cls")
            print("\nSTATUS DU ROBOT ASPIRATEUR :")
            print("\n   - Etat : Retour au socle en cours...")
        else:
            print("\nSTATUS DU ROBOT ASPIRATEUR :")
            print("\n   - Etat : {}".format(is_on))
        print("   - Niveau de batterie : {}%".format(battery_level))
        print("\nPrésence détectée. Vous êtes à la maison.")
    if aspiAujourdhui:
        print(f"\nL'aspirateur est déjà passé pour aujourd'hui.\n")
    elif aspiAujourdhui and nettoyage:
        print(f"\nL'aspirateur est en train d'être passé.\n")
    else:
        print(f"\nL'aspirateur n'a pas encore été passé aujourd'hui.\n")
    #print(f"\nAspirateur passé {aspiAujourdhui} fois aujourd'hui.\n")
    time.sleep(30)

'''
-> Actions disponibles :

  call_action                    Call an action by a name in the mapping.
  call_action_by                 Call an action.
  cleaning_summary               Return information about cleaning runs.
  consumable_status              Return information about consumables.
  disable_dnd                    Disable do-not-disturb.
  fan_speed_presets              Return available fan speed presets.
  get_property_by                Get a single property (siid/piid).
  home                           Return to home.
  identify                       Locate the device (i am here).
  info                           Get (and cache) miIO protocol...
  raw_command                    Send a raw command to the device.
  reset_filter_life              Reset filter life.
  reset_mainbrush_life           Reset main brush life.
  reset_sensor_dirty_life        Reset sensor dirty life.
  reset_sidebrush_life           Reset side brushes life.
  set_carpet_mode                Set auto boost on carpet.
  set_dnd                        Set do-not-disturb.
  set_double_clean               Set double clean (True/False).
  set_dust_collection_frequency  Set frequency for emptying the dust bin.
  set_fan_speed_preset           Set fan speed preset speed.
  set_fanspeed                   Set fan speed.
  set_led                        Enable vacuum led.
  set_lidar_collision_sensor     When ON, the robot will use lidar as the...
  set_path_mode                  Set path_mode.
  set_property_by                Set a single property (siid/piid) to...
  set_sound_muted                Set sound volume muted.
  set_sound_volume               Set sound volume [0-100].
  set_station_led                Enable station led display.
  set_sweep_type                 Set sweep_type.
  set_timing                     Set repeated clean timing.
  set_water_level                Set water_level.
  start                          Start cleaning.
  start_dust                     Start base dust collection.
  status                         State of the vacuum.
  stop                           Stop cleaning.
  test_properties                Helper to test device properties.
'''
