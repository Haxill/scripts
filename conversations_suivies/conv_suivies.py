import openai
import sqlite3
from gtts import gTTS
import pygame
import datetime
import speech_recognition as sr #SpeechRecognition
import os

# Configuration de l'API OpenAI
openai.api_key = "<API_KEY>"

''' PERSONNALISATION DE L'IA '''
# Définition du nom de l'IA
iaName = "Iris"
# Définition du mot déclencheur EN MINUSCULES
trigger_word = "iris"

# Background de l'IA
iabackground = "mon assistante personnel qui réponds à absoluement tous, avec plaisir. Mais tu aimes aussi discuter."
#iabackground = "autrefois tu travaillais pour Tony Stark"
# Définition du degré de proximité au moment de nous donner la parole ==> "Je t'écoute" ou "Je vous écoute"
accueil = "Je t'écoute"

# Définition de votre nom
myname = "<Votre_Nom>"
'''                          '''

# Modele de chatGPT utilisé
model_engine = "gpt-3.5-turbo"
tokens = 1024
temp = 0.8

# Configuration de pygame pour la lecture audio
pygame.init()

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

chatgpt_reponse = ''

# Initialisation de la conversation
conversation = []

# Initialisation du microphone
r = sr.Recognizer()
mic = sr.Microphone()
# Configuration du microphone
mic.pause_threshold = 0.7 # Durée minimum de silence pour considérer la fin d'une phrase (defaut: 0.7 0.2 0.1)
mic.phrase_threshold = 0.3 # Durée minimum d'une phrase pour la considérer valide
mic.non_speaking_duration = 0.1 # Durée minimum de silence pour considérer une pause dans la phrase

# Fonction pour lire un texte avec la synthèse vocale
def parler(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save('texte.mp3')
    # Lecture du fichier audio
    player = pygame.mixer.Sound("texte.mp3")
    player.play()
    pygame.time.wait(int(player.get_length() * 1000))
    os.remove('texte.mp3')

# Booléen de compréhension de la parole
compris = True

# Boucle de conversation avec ChatGPT
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

    if compris:
        # Convertir la parole en texte
        with mic as source:
            os.system("cls")
            print("\n\n           En attente...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            try:
                texte = r.recognize_google(audio, language="fr-FR")
                os.system("cls")
                print(f"\nVous: {texte}.")
                compris = True
            except sr.UnknownValueError:
                compris = False
                pass
            except sr.exceptions.WaitTimeoutError:
                continue
            except openai.error.RateLimitError:
                pass
            except sr.RequestError as e:
                print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                quit()
        
    while not compris:
        # Passage en boucle en attente du trigger si pas de parole pour "compris"
        with mic as source:
            os.system("cls")
            print("En attente de la commande :", trigger_word)
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=5) # Valeurs précédentes 5
            try:
                texte = r.recognize_google(audio, language="fr-FR")
                print(f"\nVous: {texte}.")
            except sr.UnknownValueError:
                continue
            except sr.exceptions.WaitTimeoutError:
                continue
            except openai.error.RateLimitError:
                pass
            except sr.RequestError as e:
                print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                quit()

        # Si le mot déclencheur est détecté
        if trigger_word in texte.lower():
            parler(f"{accueil}, {myname}.")
            with mic as source:
                os.system("cls")
                print("\n\n           En attente...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    texte = r.recognize_google(audio, language="fr-FR")
                    os.system("cls")
                    print(f"\nVous: {texte}.")
                    compris = True
                except sr.UnknownValueError:
                    compris = False
                    pass
                except sr.exceptions.WaitTimeoutError:
                    pass
                except openai.error.RateLimitError:
                    pass
                except sr.RequestError as e:
                    print("\nImpossible d'obtenir une réponse de l'API de reconnaissance vocale; {0}".format(e))
                    quit()

    # Ajout de la saisie de l'utilisateur à la conversation
    conversation.append(texte)

    # Concaténation de tous les messages de la conversation pour former le prompt
    prompt = "\n".join(conversation)

    if chatgpt_reponse == '':
        # Génération de la réponse de ChatGPT
        response = openai.ChatCompletion.create(
        model=model_engine,
        max_tokens=tokens,
        n=1,
        temperature=temp,
        messages=[
            {"role": "system", "content": "Tu réponds en tant que" +iaName+ ", " +iabackground+ ", tu m'appelles " +myname+ " et tu sais que nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ ", il est " +str(heure)+ ":" +str(minutes)+ "." },
            {"role": "user", "content": prompt+ "." }
        ])
    else:
        # Génération de la réponse de ChatGPT
        response = openai.ChatCompletion.create(
        model=model_engine,
        max_tokens=tokens,
        n=1,
        temperature=temp,
        messages=[
            {"role": "system", "content": "Tu réponds en tant que" +iaName+ ", " +iabackground+ ", tu m'appelles " +myname+ " et tu sais que nous sommes actuellement le " +str(jour)+ " " +str(mois)+ " " +str(year)+ ", il est " +str(heure)+ ":" +str(minutes)+ "." },
            {"role": "assistant", "content": chatgpt_reponse},
            {"role": "user", "content": prompt+ "." }
        ])

    # Récupération de la réponse de chatgpt
    chatgpt_reponse = response['choices'][0]['message']['content']

    # Ajout de la réponse de chatgpt à la conversation
    conversation.append(chatgpt_reponse)

    # Ajout du message et de la réponse à la base de données
    ajouter_message(texte, chatgpt_reponse)

    # Affichage de la réponse de chatgpt
    print(f"\n{iaName}: " + chatgpt_reponse)
    parler(chatgpt_reponse)
