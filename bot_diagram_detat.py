#!/usr/bin/env python
# -*- coding: utf-8 -*-
#	U+1F601
# Simple Bot to reply to Telegram messages

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import sys, logging, requests, time, math


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO) # Dans l'exercice des TPG c'est level=logging.DEBUG

logger = logging.getLogger(__name__)

TRANSPORT, CHOOSE, SAVEURS_RESTAURANTS, SORTIES, DETAILS_RESTAURANT, RETOUR, LIEU_COORDONNEES, = range(7)



def start(bot, update):
    reply_keyboard = [['Sorties', 'Restaurants']]
    update.message.reply_text(
        'Yo {}, je suis Interstar-bot je suis la pour t\'aider a faire ton choix parmis une liste d\'activités à Genève. \n\n'
        '(Tu peut a tout moment sortir du programme).\n\n'
        'Vasy je te laisse faire ton choix entre : \n\n'.format(update.message.from_user.first_name),
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHOOSE

def saveurs_restaurants(bot, update):
    reply_keyboard_restaurant= [
        ['French-food', 'Africain', 'Italien'],
        ['Japonnais', 'Chinoix'],
        ['Menu principal']
    ]
    update.message.reply_text(
        'Voici les différentes type de saveurs que l\'on peut manger à Genève?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_restaurant,
            one_time_keyboard=True
        )
    )

    return SAVEURS_RESTAURANTS


def les_differentes_sorties(bot, update):
    reply_keyboard_sorties = [
        ['Musées', 'Bars', 'Clubs'],
        ['Menu principal']
    ]
    update.message.reply_text(
        'J\'ai crue entendre que tu souhaitais sortir voici les activité que l\'on peut faire a Genève?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_sorties,
            one_time_keyboard=True
        )
    )

    return SORTIES


def restau_resultats(bot, update):
    reply_keyboard_liste_restaurant = [
        ['Restaurant Izumi', 'Restaurant Funky Monkey Room'],
        ['Pizzaria Happy Days ','Restaurant Beau-Rivage - Le Chat-Botté'],
        ['Wasabi', 'Restaurant Fiskebar'],
        ['Retour en arrière']
    ]
    update.message.reply_text(
        'Voici les meilleurs restaurants de la ville: \n\n',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_liste_restaurant,
            one_time_keyboard=True
        )
    )

    return DETAILS_RESTAURANT

def details_restaurant(bot, update):
    update.message.reply_text(
        ' {} \n\n'
        'Note: 3 étoiles\n'
        'Prix : 25 - 35 CHF \n'
        'Horaire : 11:00 - 23:00\n'
        '234 Routes des choinoix\n'
        '1200 Versoix'.format(update.message.text),
    )
    update.message.reply_location(46.2022200, 6.1456900)


def Top3musees(bot, update):
    update.message.reply_text(
        'Musée D\'histoire Naturelle \n\n'
        'Routes des Malagnou - 1203 Carouge\n'
        'Horaire : 09:00 - 18:00\n'
        'Prix: 30fr\n '
    )
    update.message.reply_text(
        ' Musée d\'art et d\'histoire\n'
        'Rue Charles-Gallons - 1220 Genève\n'
        'Horaire : 08:00 - 18:00\n'
        'Prix: Free\n '
    )
    reply_keyboard_retour = [
        ['Retour au choix des sorties']
    ]
    update.message.reply_text(
        'Musée d\'éthnographie \n\n'
        'Boulevard Carl-Vogt 65-67, 1205 Genève\n'
        'Horaire 11:00 - 18:00\n'
        'Prix: Free\n ',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )
    return RETOUR

def Top3bars(bot, update):
    update.message.reply_text(
        ' Bar la Comtesse - Champagne & Cocktail Bar \n\n'
        '2 rue de la Scie - 1202 Genève\n'
        'Horaire : 07:00 - 19:00\n'
        'Prix : 39 fr\n ',
    )
    update.message.reply_text(
        ' N\'vY Bar \n\n'
        ' Rue Henri-Blanvalet 12, 1207 Geneva\n'
        'Horaire: 17:00 - 00:00\n'
        'Prix: 15 fr\n ',
    )
    reply_keyboard_retour = [
        ['Retour au choix des sorties']
    ]
    update.message.reply_text(
        'La moule bar \n\n'
        ' Rue Henri-Blanvalet 12, 1207 Geneva\n'
        'Horaire: 17:00 - 00:00\n'
        'Prix: 15 CHF\n ',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )
    return RETOUR

def Top3clubs(bot, update):
    update.message.reply_text(
        'Le Baroque Club - Genève\n\n'
        'Place de la Fusterie 12  ⋅\n'
        'Horaire  Ouvre à 00:00 (sam.)\n'
        'Prix : 50 CHF')
    update.message.reply_text(
        ' Java Club\n\n'
         'Place de la Fusterie 12  ⋅\n'
        'Horaire  Ouvre à 00:00 (sam.)\n'
        'Prix : 50 CHF')
    reply_keyboard_retour = [
        ['Retour au choix des sorties']
    ]
    update.message.reply_text(
        'Moulin Rouge Geneva\n\n'
        'Adresse :Avenue du Mail 1, 1205 Genève\n'
        'Horaire d\'aujourd\'hui: 22:00 - 05:30\n'
        'Prix d\'entrée : 50 CHF',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_retour,
            one_time_keyboard=True
        )
    )

    return RETOUR


def exit(bot, update):
    update.message.reply_text('j\'esspere t\'avoir été utile Aureoir',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

##################### PARTI TRANSPORT #############################

def transport(bot, update):
    update.message.reply_text("Yo {} je suis le bot interstar je peut t\'aider a trouver des horaire de bus tpg "
                              "Envoi moi ta localisation ou ecrit simplement ta localité ( tu peut a tout moment quitter l'application appui sur /exit)"
                              .format(update.message.from_user.first_name))

    return LIEU_COORDONNEES

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




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(sys.argv[1])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

# PARTIE LOISIRS % Restaurant
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('python_chatbot_etats_py_TOKEN', start)],

        states={
            CHOOSE: [
                RegexHandler('Sorties', les_differentes_sorties),
                RegexHandler('Restaurants', saveurs_restaurants)
            ],

            SAVEURS_RESTAURANTS: [
                RegexHandler('French-food', restau_resultats),
                RegexHandler('Africain', restau_resultats),
                RegexHandler('Italien', restau_resultats),
                RegexHandler('Japonnais', restau_resultats),
                RegexHandler('Chinoix', restau_resultats),
                RegexHandler('Menu principal', start)
            ],

            SORTIES: [
                RegexHandler('Musées', Top3musees),
                RegexHandler('Bars', Top3bars),
                RegexHandler('Clubs', Top3clubs),
                RegexHandler('Menu principal', start)
            ],

            DETAILS_RESTAURANT: [
                RegexHandler('Restaurant Izumi', details_restaurant),
                RegexHandler('Restaurant Funky Monkey Room', details_restaurant),
                RegexHandler('Pizzaria Happy Days', details_restaurant),
                RegexHandler('Restaurant Beau-Rivage - Le Chat-Botté', details_restaurant),
                RegexHandler('Wasabi', details_restaurant),
                RegexHandler('Restaurant Fiskebar', details_restaurant),
                RegexHandler('Retour en arrière', saveurs_restaurants)
            ],

            RETOUR: [
                RegexHandler('Retour au choix des sorties', les_differentes_sorties)
            ]
        },

        fallbacks=[CommandHandler('exit', exit)]
    )

# TRANSPORT
    conv_handler_transport = ConversationHandler(
        entry_points = [CommandHandler('transport', transport)],

        states={

        LIEU_COORDONNEES:[
            MessageHandler(Filters.text, lieu_a_chercher),
            MessageHandler(Filters.location, coordonnees_a_traiter),
            MessageHandler(Filters.command, details_arret)
        ],





    },

        fallbacks=[CommandHandler('exit', exit)]
    )


    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_transport)



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()