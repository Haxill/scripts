# internet_advanced_gpt-search.py

## Description
Ce script Python utilise l'API Google pour récupérer le premier résultat de recherche en lien avec la requête de l'utilisateur. Si le résultat contient un texte, le script le lit à voix haute. Si le résultat est un article, le script affiche un lien vers l'article.

Le script utilise également l'API OpenAI pour répondre à des requêtes de type chatbot. Si le modèle de langage ne peut pas répondre à la requête, le script renvoie un lien vers un résultat de recherche.

## Information
- Created by: HAXILL
- Engine: gTTS, gpt-3.5-turbo
- Date: 12/04/2023
- Last update: 16/04/2023
- OS: Windows
- Language: French

## Future Improvements (en)
- Add support for other languages besides French.
- Add an automatic translation module for input in any language.
- Improve error handling.

## Requirements
- Python 3.9
- requests
- beautifulsoup4
- webbrowser
- datetime
- time
- os
- gtts
- pygame
- openai
- colorama

## Installation
Sur le store windows, installer le python 3.9 (cela devrait fonctionner avec python 3.6 ou supérieur).

Puis :

`python -m pip install --upgrade pip`

`pip install requests beautifulsoup4 datetime gtts pygame openai colorama`

## Utilisation
Ouvrez une invite de commande :
- Touche Windows.
- Tapez `cmd`.
- Touche Entrée.

Exécutez le script en exécutant la commande `python /Path/To/internet_advanced_gpt-search.py`.

Vérification automatique de la connexion internet avant de lancer le script.

Le script vous demandera de saisir votre requête. Il recherchera ensuite le premier résultat de recherche Google en lien avec votre requête et l'affichera. Si le résultat est un texte, le script le lira à voix haute. Si le résultat est un article, le script affichera un lien vers l'article.

Si la requête est de type chatbot, le script utilisera l'API OpenAI pour générer une réponse. Si le modèle de langage ne peut pas répondre à la requête, le script renverra un lien vers un résultat de recherche.

## Crédits
- HAXILL - Auteur du script
- Google - API de recherche Google
- OpenAI - API de modèle de langage ChatGPT 3.5 Turbo

