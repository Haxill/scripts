'''
########################################################################################################################################
# Created by : HAXILL                                                                                                                  #
# Engine     : gTTS, gpt-3.5-turbo                                                                                                     #
# Date       : 12/04/2023                                                                                                              #
# Version    : 22/04/2023                                                                                                              #
# OS         : Windows                                                                                                                 #
# Langue     : French                                                                                                                  #
# Script     : Ce script permet de communiquer avec l'API de 'chatGPT 3.5 Turbo' pour répondre à des questions et afficher le résultat #
#              de recherche Google correspondant, tout en lisant la réponse à haute voix.                                              #
########################################################################################################################################
'''

import openai
import requests
import sqlite3
import speech_recognition as sr #SpeechRecognition
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import webbrowser
from gtts import gTTS
import pygame
import datetime
from time import sleep
import os

''' PERSONNALISATION DE L'IA '''
# Définition du nom de l'IA
iaName = "Iris"
# Exemple :
#iaName = "Jarvis"

# Définition du mot déclencheur EN MINUSCULES
trigger_word = "iris"
# Exemple :
#trigger_word = "jarvis"

# Background de l'IA
iabackground = "une jeune femme pleine de vie et désireuse d'aider"
# Exemple :
#iabackground = "une ia très humaine et amicale qui travaillait autrefois pour Tony Stark"

# Définition du message d'écoute de l'IA (Exemples : "Je t'écoute" / "Je vous écoute" / "Oui" / ...)
accueil = "Je t'écoute"

# Définition de votre nom
myname = "<votre_nom>"
# Exemple :
#myname = "Monsieur"
'''                          '''

# Remplacez par votre clé d'API OpenAI
openai.api_key = "<API_KEY>"

# Modele de chatGPT utilisé
model_engine = "gpt-3.5-turbo"
# Initialisation de variables GTP
tokens = 1024
temp = 0.8
chatgpt_reponse = ''

# Initialisation de Colorama
init()

# Obtention de la date actuelle
now = datetime.datetime.now()
# Extraction de la date et l'heure pour chatGPT
year = now.year
mois_list = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
mois = mois_list[now.month]
jour = now.day
heure = now.hour
minutes = now.minute


# Configuration de pygame pour la lecture audio
pygame.init()

# Vérification de la connexion internet
os.system("cls")
print("\nVérification de la connection internet...")

# Booléen pour connexion internet
def test_connexion():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

# Connexion internet réussie
if test_connexion():
    os.system("cls")
    print("\nVérification de la connection internet...OK")
    # Initialisation du programme
    print("Initialisation de l'IA en cours...")

    # Initialisation du microphone
    r = sr.Recognizer()
    mic = sr.Microphone()

    # Configuration du microphone
    mic.pause_threshold = 0.7 # Durée minimum de silence pour considérer la fin d'une phrase (defaut: 0.7 0.2 0.1)
    mic.phrase_threshold = 0.3 # Durée minimum d'une phrase pour la considérer valide
    mic.non_speaking_duration = 0.1 # Durée minimum de silence pour considérer une pause dans la phrase

    # Configuration de la requête à l'API pour dire bonjour
    response = openai.ChatCompletion.create(
    model=model_engine,
    max_tokens=tokens,
    n=1,
    temperature=temp,
    messages=[
        {"role": "user", "content": "Tu dis bonjour en tant que " +iaName+ ", " +iabackground+ ", tu m'appelles " +myname+ ", nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ ", il est " +str(heure)+ ":" +str(minutes)+ "." },
    ])
    hello = response['choices'][0]['message']['content']

    # Fonction pour lire un texte avec la synthèse vocale
    def parler(texte):
        tts = gTTS(text=texte, lang='fr')
        tts.save('texte.mp3')
        # Lecture du fichier audio
        player = pygame.mixer.Sound("texte.mp3")
        player.play()
        if texte is not hello:
            pygame.time.wait(int(player.get_length() * 1000))
        os.remove('texte.mp3')

    os.system("cls")
    print("\nVérification de la connection internet...OK")
    print("Initialisation de l'IA en cours...OK")
    print("Initialisation de la base de données...")
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("conversation.db")
    c = conn.cursor()
    # Création de la table "messages" si elle n'existe pas déjà
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                (message text, reponse text)''')
 
    # Fonction pour ajouter un message et sa réponse à la base de données
    def ajouter_message(message, reponse):
        c.execute("INSERT INTO messages (message, reponse) VALUES (?, ?)", (str(message), str(reponse)))
        conn.commit()

    # Initialisation de la conversation
    conversation = []

    # L'IA dit bonjour
    parler(hello)
else:
    # Echec connexion internet
    os.system("cls")
    # Fin du script
    print(f"\n\n{Fore.RED}Veuillez vérifier votre connexion internet puis relancer le script.{Style.RESET_ALL}\n\n")
    sleep(5)
    quit()

query_bool = False

# Boucle du programme principal
while True:
    # (Ré)initialisation des booléens
    repgpt = False
    reptext = False
    repurl = False
    
    os.system("cls")
    while True and not query_bool:
        # En attente du mot déclencheur, micro ouvert
        with mic as source:
            os.system("cls")
            print("En attente de la commande :", trigger_word)
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=2) # Valeurs précédentes 5
            try:
                texte = r.recognize_google(audio, language="fr-FR")
                print(f"\nVous:", texte)
            except sr.UnknownValueError:
                pass

        try:
            # Convertir la parole en texte
            texte = r.recognize_google(audio, language="fr-FR")

            # Si le mot déclencheur est détecté, synthétiser un message d'accueil
            if trigger_word in texte.lower():
                parler(f"{accueil}, {myname}.")

                # Attendre que l'utilisateur dicte une question ou une demande
                with mic as source:
                    os.system("cls")
                    print("\n\n           En attente de votre question ou demande...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)

                # Obtention de la date actuelle
                now = datetime.datetime.now()
                # Extraction de la date et l'heure pour chatGPT
                year = now.year
                mois_list = ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
                mois = mois_list[now.month]
                jour = now.day
                heure = now.hour
                minutes = now.minute

                # Convertir la parole en texte
                query = r.recognize_google(audio, language="fr-FR")

                # Ajout de la saisie de l'utilisateur à la conversation
                conversation.append(query)
                break

        except sr.UnknownValueError:
            pass
        except sr.exceptions.WaitTimeoutError:
            pass
        except sr.RequestError as e:
            print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
            quit()

    query_bool = False
    os.system("cls")
    url = "https://www.google.com/search?q=" +query.replace(" ", "+")
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

        # Afficher le texte, le lire, et afficher l'url du premier résultat de recherche
        if result_text != '' and result_title != '':
            reptext = True
            repgpt = False
            print(f"\n{result_text}\n")
            
            # Transformation du texte en fichier vocal
            if result_text != '':
                # Transformation et lecture du fichier audio
                parler(result_text)
                
            # Affiche le lien vers l'article
            if "search" in result_url:
                repurl = True
                continue
            else:
                print(Fore.MAGENTA + "{}".format(result_url) + Style.RESET_ALL)
        else:
            repgpt = True
            reptext = False
            
            if chatgpt_reponse == '':
                # Génération de la réponse de ChatGPT
                response = openai.ChatCompletion.create(
                model=model_engine,
                max_tokens=tokens,
                n=1,
                temperature=temp,
                messages=[
                    {"role": "system", "content": "Tu réponds en tant que" +iaName+ ", " +iabackground+ ", tu m'appelles " +myname+ ", tu sais que nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ ", il est " +str(heure)+ ":" +str(minutes)+ "." },
                    {"role": "user", "content": query+ "." }
                ])
            else:
                # Envoie la requête à l'API ChatGPT 3.5 Turbo et récupère la réponse
                response = openai.ChatCompletion.create(
                model=model_engine,
                max_tokens=tokens,
                n=1,
                temperature=temp,
                messages=[
                    {"role": "system", "content": "Tu reponds en tant que" +iaName+ ", " +iabackground+ ", tu m'appelles " +myname+ ", tu sais que nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ " à " +str(heure)+ ":" +str(minutes)+ "." },
                    {"role": "assistant", "content": output_text },
                    {"role": "user", "content": query+ "."}
                ])
            # Récupération de la réponse de chatgpt
            output_text = response['choices'][0]['message']['content']
            # Ajout de la réponse de chatgpt à la conversation
            conversation.append(output_text)
            # Ajout du message et de la réponse à la base de données
            ajouter_message(query, output_text)
            # Remplace la réponse si chatGPT ne sait pas répondre
            if "désolé" in output_text:
                output_text = "Je ne peux pas répondre à cette question, mais je te donne quand même un lien..."
                print("\n", output_text, "\n")
            else:
                print("\n", output_text, "\n")

            # Transformation et lecture du fichier audio
            parler(output_text)
            
            # Affiche le lien vers l'article
            if "search" in result_url:
                repurl = True
                continue
            elif not "au revoir" in query:
                print(Fore.MAGENTA + "{}".format(result_url) + Style.RESET_ALL)
                print("\nOuvrir le lien dans le navigateur (oui/Non) ? ")
                #parler("Voulez-vous ouvrir le lien ?")
                try:
                    with mic as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source, timeout=3, phrase_time_limit=5)
                    # Convertir la parole en texte
                    openweb = r.recognize_google(audio, language="fr-FR")
                    if "oui" in openweb:
                        webbrowser.open(result_url)
                    else:
                        query = openweb
                        query_bool = True
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                    break
                except sr.exceptions.WaitTimeoutError:
                    continue
                    
    else:
        if not repurl and not reptext:
            result_title = ""
            print(f"\n{Fore.RED}    - Veuillez spécifier une recherche -{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}    - Pas de résultat trouvé pour {query} -{Style.RESET_ALL}")
    
    if not repgpt:
        # Ouvre l'URL dans un navigateur
        if not reptext and not repgpt:
            result_url = "https://perdu.com/"
            print("\nOuvrir le lien dans le navigateur (oui/Non) ? ")
            parler("En panne d'inspiration ? Voulez-vous ouvrir le lien ?")
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                # Convertir la parole en texte
                openweb = r.recognize_google(audio, language="fr-FR")
                if "oui" in openweb:
                    webbrowser.open(result_url)
                else:
                        query = openweb
                        query_bool = True
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                break
            except sr.exceptions.WaitTimeoutError:
                continue
        else:
            print("\nOuvrir le lien dans le navigateur (oui/Non) ? ")
            #parler("Voulez-vous ouvrir le lien ?")
            try:
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=3, phrase_time_limit=5)
                # Convertir la parole en texte
                openweb = r.recognize_google(audio, language="fr-FR")
                if "oui" in openweb:
                    webbrowser.open(result_url)
                else:
                        query = openweb
                        query_bool = True
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                break
            except sr.exceptions.WaitTimeoutError:
                continue

    # L'utilisateur quitte le script
    if "au revoir" in query:
        print("\nA bientôt --HAXILL\n")
        sleep(2)
        break
