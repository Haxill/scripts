import os
import importlib
from time import sleep

# Fonction de vérification d'import de bibliothèque
def is_imported(lib_name):
    # Vérifie si la bibliothèque est déjà importée
    try:
        importlib.import_module(lib_name)
        print(f"Bibliothèque {lib_name} = OK")
        
    # Si la bibliothèque n'est pas importée, l'installer
    except ImportError:
        print(f"Bibliothèque {lib_name} = NOK\nInstallation en cours :")
        os.system(f"pip install {lib_name}")

# Vérification des prérequis
os.system("cls")
print("\nVérification des prérequis...\n")

# Vérification de la présence des bibliothèques nécessaires
is_imported("requests")
is_imported("openai")
is_imported("beautifulsoup4")
is_imported("colorama")
is_imported("datetime")
sleep(3)
os.system("cls")
print("\nVérification des prérequis...OK")
sleep(2)
os.system("cls")

import requests
from bs4 import BeautifulSoup
import openai
from colorama import init, Fore, Style
import datetime

# Initialisation de la clé API d'OpenAI
openai.api_key = "<API_KEY>"

# Modele de chatGPT utilisé
model_engine = "gpt-3.5-turbo"
# Initialisation de variables GPT
tokens = 1024
temp = 0.8

# Initialisation de Colorama
init()

# Définition de la fonction pour récupérer le texte depuis une URL
def get_article_text(url):
    # Téléchargement de la page HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Extraction du texte de l'article
    article = ""
    for paragraph in soup.find_all("p"):
        article += paragraph.get_text()
    return article

while True:
    # Entrée utilisateur
    query = input(f"\n{Fore.LIGHTGREEN_EX}Que rechercher sur {Fore.CYAN}G{Fore.RED}o{Fore.YELLOW}o{Fore.CYAN}g{Fore.GREEN}l{Fore.RED}e{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}?{Style.RESET_ALL}\n")

    # Création de l'URL de recherche
    search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")

    # Envoie d'une requête à Google et récupération de l'URL du premier lien
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("div", attrs={"class": "g"})
    result_url_element = result.find("a")
    if result_url_element is not None:
        result_url = result_url_element.get("href")
        url = "{}".format(result_url)

    # Erreur dans la construction de l'URL (généralement du à un premier lien non formaté)
    if "search" in url:
        print(f"\n{Fore.RED}      --- Lien récupéré invalide ---{Style.RESET_ALL}")
        soup = BeautifulSoup(response.text, "html.parser")
        result_links = soup.find_all("a", href=True)
        if len(result_links) > 1:
            result_url = result_links[1]['href']
            url = "{}".format(result_url)
        else:
            print(f"\n{Fore.RED}--- Impossible de trouver un deuxième lien ---{Style.RESET_ALL}")
            continue
    else:
        # Récupération du texte depuis l'URL
        article_text = get_article_text(url)

        try:
            # Obtention de la date actuelle
            now = datetime.datetime.now()
            # Extraction de la date et l'heure pour chatGPT
            year = now.year
            mois_list = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            mois = mois_list[now.month]
            jour = now.day
            heure = now.hour
            minutes = now.minute

            # Utilisation de ChatGPT pour la synthèse du texte de l'article
            response = openai.ChatCompletion.create(
            model=model_engine,
            max_tokens=tokens,
            n=1,
            temperature=temp,
            messages=[
                {"role": "system", "content": "Tu réponds toujours avec plaisir et objectivité, peu importe le sujet tu adores répondre à tout. Nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ ", il est " +str(heure)+ ":" +str(minutes)+ "." },
                {"role": "user", "content": "Réponds à la question '" +query+ "' grâce à ce texte : " + article_text }
            ])
            read_text = response['choices'][0]['message']['content']

            if "désolé" in read_text:
                read_text = "Je n'ai pas cette information..."
                print(f"\n{Fore.MAGENTA}{read_text}{Style.RESET_ALL}")
            else:
                # Affichage de la réponse de chatGPT
                print(f"\n{read_text}")

        # Texte envoyé a chatGPT dépasse le nombre de TOKENS autorisé par OpenAI
        except openai.error.InvalidRequestError:
            print(f"\n{Fore.RED}      --- Texte de la page web trop long pour être analysé ---{Style.RESET_ALL}")
