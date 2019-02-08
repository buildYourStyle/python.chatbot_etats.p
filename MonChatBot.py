import sys, logging, requests, time, math
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot_token = sys.argv[1]

# Utile

def appeler_opendata(path):
    url = "http://transport.opendata.ch/v1/" + path
    reponse = requests.get(url)
    return reponse.json()


def calcul_temps_depart(timestamp):
    seconds = timestamp-time.time()
    minutes = math.floor(seconds/60)
    if minutes < 1:
        return "FAUT COURIR!"
    if minutes > 60:
        return "> {} h.".format(math.floor(minutes/60))
    return "dans {} min.".format(minutes)



# Preparation des messages

def afficher_arrets(update, arrets):
    texte_de_reponse = "Voici les arrets:\n"
    for station in arrets['stations']:
        if station['id'] is not None:
            texte_de_reponse += "\n/a" + station['id'] + " " + station['name']
    update.message.reply_text(texte_de_reponse)


def afficher_departs(update, departs):
    texte_de_reponse = "Voici les prochains departs:\n\n"
    for depart in departs['stationboard']:
        texte_de_reponse += "{} {} dest. {} - {}\n".format(
            depart['category'],
            depart['number'],
            depart['to'],
            calcul_temps_depart(depart['stop']['departureTimestamp'])
        )
    texte_de_reponse += "\nAfficher a nouveau: /a" + departs['station']['id']

    coordinate = departs['station']['coordinate']
    update.message.reply_location(coordinate['x'], coordinate['y'])
    update.message.reply_text(texte_de_reponse)



# Les differentes reponses

def bienvenue(bot, update):
    update.message.reply_text("Merci d'envoyer votre localisation (via piece jointe ou simplement en texte)")


def lieu_a_chercher(bot, update):
    resultats_opendata = appeler_opendata("locations?query=" + update.message.text)
    afficher_arrets(update, resultats_opendata)


def coordonnees_a_traiter(bot, update):
    location = update.message.location
    resultats_opendata = appeler_opendata("locations?x={}&y={}".format(location.latitude, location.longitude))
    afficher_arrets(update, resultats_opendata)


def details_arret(bot, update):
    arret_id = update.message.text[2:]
    afficher_departs(update, appeler_opendata("stationboard?id=" + arret_id))



# Creation du service de bot
updater = Updater(bot_token)

# Ajout des evenements pour traiter les messages
updater.dispatcher.add_handler(CommandHandler('start', bienvenue))
updater.dispatcher.add_handler(MessageHandler(Filters.text, lieu_a_chercher))
updater.dispatcher.add_handler(MessageHandler(Filters.location, coordonnees_a_traiter))
updater.dispatcher.add_handler(MessageHandler(Filters.command, details_arret))

# Démarrer le bot avec les configurations
updater.start_polling()
updater.idle()