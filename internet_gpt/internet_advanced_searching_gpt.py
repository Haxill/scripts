'''
########################################################################################################################################
# Created by : HAXILL                                                                                                                  #
# Engine     : gTTS, gpt-3.5-turbo                                                                                                     #
# Date       : 12/04/2023                                                                                                              #
# Version    : 13/04/2023                                                                                                              #
# Langue     : French                                                                                                                  #
# Script     : Ce script permet de communiquer avec l'API de 'chatGPT 3.5 Turbo' pour répondre à des questions et afficher le résultat #
#              de recherche Google correspondant, tout en lisant la réponse à haute voix.                                              #
########################################################################################################################################
'''

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import webbrowser
from gtts import gTTS
import pygame
import datetime
from time import sleep
import os
import openai

# Remplacez par votre clé d'API OpenAI
openai.api_key = "<VOTRE_CLE_API_OPENAI>"

# Modele de chatGPT utilisé
model_engine = "gpt-3.5-turbo"

# Initialisation de Colorama
init()

# Obtention de la date actuelle
now = datetime.datetime.now()
# Extraction de l'année pour que chatGPT sache quelle est l'année en cours
year = now.year

# Configuration de pygame pour la lecture audio
pygame.init()

while True:
    # (Ré)initialisation des booléens
    repgpt = False
    reptext = False
    repurl = False
    
    os.system("cls")
    # Requête HTTP pour récupérer la page de résultats de recherche Google
    query = input("\n      -> Vous : ")
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Analyse la page HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche du premier élément HTML avec la classe "g"
    result = soup.find("div", attrs={"class": "g"})

    # Check des variables
    if result is not None:
        result_title_element = result.find("h3")
        if result_title_element is not None:
            result_title = result_title_element.get_text()
        else:
            result_title = ""
        result_url_element = result.find("a")
        if result_url_element is not None:
            result_url = result_url_element.get("href")
        else:
            result_url = ""
        result_text_element = result.find("span")
        if result_text_element is not None:
            result_text = result_text_element.get_text()
        else:
            result_text = ""

        # Afficher le texte, le lire, et l'url de description du premier résultat de recherche
        if result_text != '' and result_title != '':
            reptext = True
            repgpt = False
            print(f"\n{result_text}\n")
            
            # Transformation du texte en fichier vocal
            if result_text != '':
                tts = gTTS(result_text, lang='fr')
                tts.save("result_text.mp3")
                
                # Lecture du fichier audio
                player = pygame.mixer.Sound("result_text.mp3")
                player.play()
                pygame.time.wait(int(player.get_length() * 1000))
                
                # Suppression du fichier audio
                os.remove("result_text.mp3")
                
            # Affiche le lien vers l'article
            if "search" in result_url:
                repurl = True
                pass
            else:
                print(Fore.MAGENTA + "{}".format(result_url) + Style.RESET_ALL)
        else:
            repgpt = True
            reptext = False
            
            # Envoie la requête à l'API ChatGPT 3.5 Turbo et récupère la réponse
            response = openai.ChatCompletion.create(
            model=model_engine,
            max_tokens=1024,
            n=1,
            temperature=0.8,
            messages=[
                {"role": "system", "content": "Tu reponds en tant que mon assistant personnel qui connais tout sur tout et tu sais que nous sommes actuellement en " +str(year)+ "." },
                {"role": "user", "content": query }
            ])
            # Affiche la réponse de ChatGPT 3.5 Turbo
            output_text = response['choices'][0]['message']['content']
            # Remplace la réponse si chatGPT ne sait pas répondre
            if "désolé" in output_text:
                output_text = "Je ne peux pas répondre à cette question, mais je te donne quand même un lien..."
                print("\n", output_text, "\n")
            else:
                print("\n", output_text, "\n")

            # Transformation du texte en fichier vocal
            tts = gTTS(output_text, lang='fr')
            tts.save("output_text.mp3")
            
            # Lecture du fichier audio
            player = pygame.mixer.Sound("output_text.mp3")
            player.play()
            pygame.time.wait(int(player.get_length() * 1000))
            
            # Suppression du fichier audio
            os.remove("output_text.mp3")
            
            # Affiche le lien vers l'article
            if "search" in result_url:
                repurl = True
                pass
            else:
                print(Fore.MAGENTA + "{}".format(result_url) + Style.RESET_ALL)
                openweb = input(f"\nOuvrir le lien dans le navigateur (o/N) ? ")
                if openweb == "o":
                    webbrowser.open(result_url)
    else:
        if not repurl and not reptext:
            result_title = ""
            print(f"\n{Fore.RED}    - Veuillez spécifier une recherche -{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}    - Pas de résultat trouvé pour {query} -{Style.RESET_ALL}")
    
    # Extraction des informations de la page Wikipedia si elle existe
    if not repgpt :
        wikipedia_api_url = "https://fr.wikipedia.org/w/api.php"
        wikipedia_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "titles": result_title,
            "exintro": 1,
            "explaintext": 1,
            "redirects": 1
        }
        response = requests.get(wikipedia_api_url, params=wikipedia_params)
        response_json = response.json()

        if not reptext and not repgpt:
            pass
        else:
            if "-1" not in response_json["query"]["pages"]:
                # Récupère l'extrait de la page Wikipedia
                page_id = next(iter(response_json["query"]["pages"]))
                page_extract = response_json["query"]["pages"][page_id]["extract"]
                
                # Affiche les informations de la page Wikipedia
                print("\n *Précisions : {}".format(page_extract))
                tts = gTTS("{}".format(page_extract), lang='fr')
                tts.save("page_extract.mp3")
                
                # Lecture du fichier audio
                player = pygame.mixer.Sound("page_extract.mp3")
                player.play()
                pygame.time.wait(int(player.get_length() * 1000))
                
                # Suppression du fichier audio
                os.remove("page_extract.mp3")

        # Ouvre l'URL dans un navigateur
        if not reptext and not repgpt:
            result_url = "https://perdu.com/"
            openweb = input(f"\nBesoin d'inspiration (o/N) ? ")
            if openweb == "o":
                webbrowser.open(result_url)
        else:
            if "-1" in response_json["query"]["pages"]:
                if repurl:
                    openweb = input(f"\nOuvrir le lien dans le navigateur (o/N) ? ")
                    if openweb == "o":
                        webbrowser.open(result_url)

    # L'utilisateur quitte le script
    if query == "au revoir" or query == "aurevoir":
        print("\nA bientôt --HAXILL\n")
        sleep(2)
        break
