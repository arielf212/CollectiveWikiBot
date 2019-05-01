# Input prompts
prompt_main = "What would you like to do? Input the corresponding number:\n" \
         "1: Add new entries to the wiki.\n" \
         "2: Update specific entries on the wiki.\n" \
         "3: Thoroughly update the wiki.\n\n"
prompt_1 = "How many new cards should be submitted? (20 per new week should be enough most weeks)\n\n"
prompt_2 = "Write the exact names of the cards which should be updated separated by \"_-_\"\n" \
           "Example: \"Crushing Waves_-_Absolute Scaling_-_???\"\n\n"

# URLs
url_api = "https://collective.gamepedia.com/api.php"
url_cards_all = "https://server.collective.gg/api/public-cards/"
url_card_target = "https://server.collective.gg/api/card/{}"

# Querystring parameters
qs_token = {
    'action': "query",
    'meta': "tokens",
    'format': "json",
    'type': "login"
    }

qs_login = {
    'action': "login",
    'format': "json"
    }

qs_parse = {
    'action': "parse",
    'prop': "wikitext",
    'page': "",
    'format': "json"
    }

qs_edit = {
    'action': "edit",
    'title': "",
    'bot': True,
    'minor': True,
    'watchlist': "nochange",
    'format': "json"
    }

qs_upload = {
    'action': "upload",
    'format': "json"
    }

# Data payload (for POST requests)
pl_login = {
    'lgname': "Collectivewikibot@CollectiveWikiBot",
    'lgpassword': "REPLACE_THIS",
    'lgtoken': ""
    }

pl_edit = {
    'text': "",
    'summary': "Card infobox created/updated",
    'token': ""
    }

pl_upload = {
    'filename': "",
    'token': ""
    }

# Infobox WikiMedia template for card pages
info_template = "Infobox\n" \
                "| image = {}.png\n" \
                "| name = {}\n" \
                "| affinity = {}\n" \
                "| rarity = {}\n" \
                "| tribaltype = {}\n" \
                "| releaseweek = {}\n" \
                "| cost = {}\n" \
                "| atk = {}\n" \
                "| hp = {}\n" \
                "| text = {}\n" \
                "| creatorname = {}\n" \
                "| artistname = {}\n"
