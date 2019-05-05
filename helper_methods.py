from time import sleep

from requests import *

from constants import *


session = Session()

r_token_login = session.get(url_api, params=qs_token)
login_token = r_token_login.json()['query']['tokens']['logintoken']
pl_login['lgtoken'] = login_token

r_login = session.post(url_api, params=qs_login, data=pl_login)

del (qs_token['type'])
r_token_csrf = session.get(url_api, params=qs_token)
csrf_token = r_token_csrf.json()['query']['tokens']['csrftoken']
pl_edit['token'] = csrf_token


def parse(text):
    text = text.replace("\"", "QUOTATION")

    if text.startswith("\n"):
        text = text.replace("\n", "", 1)
        text = text.replace("\n ", "\n")

    return text


def de_parse(text):
    return text.replace("QUOTATION", "\"")


def get_cards():
    card_list = get(url_cards_all).json()['cards']
    stats_list = []

    for card in card_list:

        if card['imgurl'] is None:
            continue

        i_uid = card['uid']
        i_imgurl = card['imgurl']
        i_release_group = card['releasegroup']
        i_name = card['name']
        i_rarity = card['rarity']
        i_text = card['static_text']

        if i_release_group is None:
            i_release_group = "Core Set"
        if i_text is None:
            i_text = ""
        i_text = parse(i_text)
        i_name = parse(i_name)

        stats = [i_uid, i_name, i_rarity, i_release_group, i_imgurl, i_text]

        stats_list.append(stats)

    return stats_list


def get_card_extra(stats):
    i_uid = stats[0]

    card_info = get(url_card_target.format(i_uid)).json()['card']

    i_object_type = card_info['Text']['ObjectType']
    i_affinity = card_info['Text']['Affinity']

    card_properties = card_info['Text']['Properties']
    card_play_abilitiy = card_info['Text']['PlayAbility']
    card_abilities = card_info['Text']['Abilities']

    i_cost, i_hp, i_atk, i_tribal_type, i_creator_name, i_artist_name = None, None, None, None, None, None

    for prop in card_properties:
        value = prop['Expression']['Value']
        info_type = prop['Symbol']['Name']

        if info_type == "IGOCost":
            i_cost = value
        elif info_type == "HP":
            i_hp = value
        elif info_type == "ATK":
            i_atk = value
        elif info_type == "TribalType":
            i_tribal_type = value
        elif info_type == "CreatorName":
            i_creator_name = value
        elif info_type == "ArtistName":
            i_artist_name = value

    i_text = stats[5]

    if not i_text:
        if "Properties" in card_play_abilitiy:
            props = card_play_abilitiy['Properties']

            for i in range(len(props)):
                if props[i]['Expression']['$type'] == "StringLiteral":
                    i_text += parse(props[i]['Expression']['Value']) + "\n"

        for i in range(len(card_abilities)):
            if "Properties" in card_abilities[i]:
                props = card_abilities[i]['Properties']

                for j in range(len(props)):
                    if props[j]['Expression']['$type'] == "StringLiteral":
                        i_text += parse(props[j]['Expression']['Value']) + "\n"

            elif "$type" in card_abilities[i]:
                i_text += card_abilities[i]['$type'].replace("Predefines.", "") + "\n"

        if i_text:
            stats[5] = parse(i_text[:-1])

    extras = [i_object_type, i_affinity, i_cost, i_hp, i_atk, i_tribal_type, i_creator_name, i_artist_name]
    stats += extras

    return stats


def upload_file(stats):
    name = stats[1].replace("?", "-").replace("!", "-")
    img_url = stats[4]

    qs_parse['page'] = f"File:{name}.png"
    r_parse = session.get(url_api, params=qs_parse)

    print(name)
    print(r_parse.text)

    if "error" in r_parse.json():
        filename = f"{name}.png"
        image_data = session.get(img_url).content

        files = {'file': (filename, image_data)}

        pl_upload['token'] = csrf_token
        pl_upload['filename'] = filename

        r_upload = session.post(url_api, params=qs_upload, data=pl_upload, files=files)
        print(r_upload.text)

        sleep(7)
    else:
        print("File there")


def update_infobox(stats):
    for i in range(len(stats)):
        stats[i] = de_parse(stats[i])

    i_name = stats[1]
    i_affinity = stats[7]
    i_rarity = stats[2]
    i_tribal_type = stats[11]
    i_release_group = stats[3]
    i_cost = stats[8]
    i_atk = stats[10]
    i_hp = stats[9]
    i_text = stats[5]
    i_creator_name = stats[12]
    i_artist_name = stats[13]

    info_box = info_template.format(i_name.replace("?", "-").replace("!", "-"), i_name,
                                    i_affinity.replace("None", "Neutral"), i_rarity, i_tribal_type,
                                    i_release_group, i_cost, i_atk, i_hp, i_text,
                                    i_creator_name, i_artist_name)

    qs_parse['page'] = i_name
    qs_edit['title'] = i_name
    print(i_name)

    r_parse = session.get(url_api, params=qs_parse)

    if "error" in r_parse.json():
        if r_parse.json()['error']['code'] == "missingtitle":
            pl_edit['text'] = "{{" + info_box + "}}"
        else:
            print("Something bad happened")
            return
    else:
        page_content = r_parse.json()['parse']['wikitext']["*"]

        try:
            true_content = page_content.split("{{")[1].split("}}")[0]
        except IndexError:
            true_content = ""

        new_page = page_content.replace(true_content, info_box)

        if info_box == true_content:
            print("Nothing to see here")
            return
        else:
            pl_edit['text'] = new_page

    r_edit = session.post(url_api, params=qs_edit, data=pl_edit)
    print(r_edit.text)


def upload_template(stats):
    name = stats[1]
    uid = stats[0]

    qs_edit['title'] = f"Template:{name}"
    pl_edit['text'] = "[https://www.collective.gg/try-out?imgurl=" \
                      f"https://files.collective.gg/p/cards/{uid}-s.png " \
                      f"{name}"

    r_edit = session.post(url_api, params=qs_edit, data=pl_edit)
    print(r_edit.text)
