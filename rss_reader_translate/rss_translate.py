import feedparser
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from gtts import gTTS
import pygame
import os
from langdetect.lang_detect_exception import LangDetectException
from mtranslate import translate

#######################################################################################################################################
# Created by : HAXILL                                                                                                                 #
# Engine     : gTTS                                                                                                                   #
# Date       : 11/04/2023                                                                                                             #
# Version    : 12/04/2023                                                                                                             #
# Langue     : Français                                                                                                               #
# Script     : Il récupère le contenu d'un flux RSS (titre, description et lien), traduit le titre et la description des entrées      #
#              dans n'importe quelle langue, supprime la dernière phrase de la description si elle est identique au titre, affiche    #
#              les résultats et lit à voix haute le titre et la description.                                                          #
#######################################################################################################################################

# Initialisation de colorama
init()

# Configuration de pygame pour la lecture audio
pygame.init()

# URL du flux RSS à récupérer
  # RU :
#url = "https://russiancouncil.ru/rss/analytics-and-comments/"
  # US :
#url = "https://www.kitploit.com//feeds/posts/default"
#url = "https://latesthackingnews.com/feed/"
#url = "https://www.hackerone.com/blog.rss"
#url = "https://www.welivesecurity.com/category/cybercrime,apt-activity-reports/feed/"
#url = "https://feeds.feedburner.com/TheHackersNews"
  # FR :
#url = "https://www.zataz.com/feed/"
url = "https://www.lemondeinformatique.fr/flux-rss/thematique/securite/rss.xml"
#url = "https://www.journaldugeek.com/feed/"
#url = "https://www.generation-nt.com/export/rss_techno.xml"

# Demande de la langue dans laquelle on veut lire les résultats
print(f"\n                              -- HAXILL RSS FEED TRANSLATOR --\n")
langue = input(f"\n Entrez la langue dans laquelle vous voulez lire les résultats (fr, en, es, it, ru,...) : ")

# Récupération du contenu du flux RSS
feed = feedparser.parse(url)

# Parcours des entrées du flux RSS
for entry in feed.entries:
    # Récupération du titre
    title = entry.title.strip()

    if title:
        # Traduction si nécessaire
        try:
            title = translate(title, langue, 'auto')

        except LangDetectException:
            pass

    # Récupération du lien
    link = entry.link.strip()

    # Récupération de la description
    soup = BeautifulSoup(entry.description, "html.parser")
    description = soup.get_text().strip()

    if description:
        # Traduction si nécessaire
        try:
            description = translate(description, langue, 'auto')

        except LangDetectException:
            pass

        # Suppression de la dernière phrase si elle est identique au titre
        if description.endswith(title):
            description = description[:-(len(title)+1)].strip()

        # Affichage des résultats
        print(f"\nTitre: {Fore.GREEN}{title}{Style.RESET_ALL}\n")
        print(f"Description: {Fore.BLUE}{description}{Style.RESET_ALL}\n")
        print(f"Lien: {Fore.MAGENTA}{link}{Style.RESET_ALL}\n")
        print("-" * 100)

        # Lecture du titre et de la description
        tts = gTTS(title, lang=langue)
        tts.save("title.mp3")
        tts = gTTS(description, lang=langue)
        tts.save("description.mp3")

        # Lecture du fichier audio avec pygame
        player = pygame.mixer.Sound("title.mp3")
        player.play()
        pygame.time.wait(int(player.get_length() * 1000))
        player = pygame.mixer.Sound("description.mp3")
        player.play()
        pygame.time.wait(int(player.get_length() * 1000))

        # Suppression du fichier audio
        os.remove("title.mp3")
        os.remove("description.mp3")
    else:
        print(f"\nTitre: {Fore.GREEN}{title}{Style.RESET_ALL}\n")
        print(f"Description: {Fore.RED}Aucune description disponible{Style.RESET_ALL}\n")
        print(f"Lien: {Fore.MAGENTA}{link}{Style.RESET_ALL}\n")
        print("-" * 100)
