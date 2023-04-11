import feedparser
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import pyttsx3
from langdetect.lang_detect_exception import LangDetectException
from mtranslate import translate

#######################################################################################################################################
# Created by : HAXILL                                                                                                                 #
# Date       : 11/04/2023                                                                                                             #
# Langue     : Français                                                                                                               #
# Script     : Il récupère le contenu d'un flux RSS (titre, description et lien), traduit le titre et la description des entrées      #
#              s'ils ne sont pas en français, supprime la dernière phrase de la description si elle est identique au titre, affiche   #
#              les résultats et lit à voix haute le titre et la description.                                                          #
#######################################################################################################################################

# Initialisation de colorama
init()

# Configuration du moteur de synthèse vocale
engine = pyttsx3.init()

# Configuration de la voix
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Réglage de la vitesse de lecture
engine.setProperty('rate', 170)

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
url = "https://www.zataz.com/feed/"
#url = "https://www.lemondeinformatique.fr/flux-rss/thematique/securite/rss.xml"
#url = "https://www.journaldugeek.com/feed/"
#url = "https://www.generation-nt.com/export/rss_techno.xml"

# Récupération du contenu du flux RSS
feed = feedparser.parse(url)

# Parcours des entrées du flux RSS
for entry in feed.entries:
    # Récupération du titre
    title = entry.title.strip()

    if title:
        # Traduction si nécessaire
        try:
            title = translate(title, 'fr', 'auto')
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
            description = translate(description, 'fr', 'auto')
        except LangDetectException:
            pass

        # Suppression de la dernière phrase si elle est identique au titre
        if description.endswith(title):
            description = description[:-(len(title) + 1)].strip()

        # Affichage des résultats
        print(f"\nTitre: {Fore.GREEN}{title}{Style.RESET_ALL}\n")
        print(f"Description: {Fore.BLUE}{description}{Style.RESET_ALL}\n")
        print(f"Lien: {Fore.MAGENTA}{link}{Style.RESET_ALL}\n")
        print("-" * 100)

        # Lecture du titre et de la description
        engine.say(title)
        engine.runAndWait()
        engine.say(description)
        engine.runAndWait()

    else:
        print(f"\nTitre: {Fore.GREEN}{title}{Style.RESET_ALL}\n")
        print(f"Description: {Fore.RED}Aucune description disponible{Style.RESET_ALL}\n")
        print(f"Lien: {Fore.MAGENTA}{link}{Style.RESET_ALL}\n")
        print("-" * 100)
