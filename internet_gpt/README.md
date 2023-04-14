# Description

Ce script Python utilise l'API Google pour récupérer le premier résultat de recherche en lien avec la requête de l'utilisateur. Si le résultat contient un texte, le script le lit à voix haute. Si le résultat est un article, le script affiche un lien vers l'article.

Le script utilise également l'API OpenAI pour répondre à des requêtes de type chatbot. Si le modèle de langage ne peut pas répondre à la requête, le script renvoie un lien vers un résultat de recherche.

# Requirements

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

# Installation

`$ pip install requests beautifulsoup4 datetime gtts pygame openai colorama`

# Utilisation

Exécutez le script en exécutant la commande `python.exe internet_advanced_gpt-search.py`.

Le script vous demandera de saisir votre requête. Il recherchera ensuite le premier résultat de recherche en lien avec votre requête et l'affichera. Si le résultat est un texte, le script le lira à voix haute. Si le résultat est un article, le script affichera un lien vers l'article.

Si la requête est de type chatbot, le script utilisera l'API OpenAI pour générer une réponse. Si le modèle de langage ne peut pas répondre à la requête, le script renverra un lien vers un résultat de recherche.

# Crédits

- HAXILL - Auteur du script
- Google - API de recherche Google
- OpenAI - API de modèle de langage ChatGPT 3.5 Turbo
