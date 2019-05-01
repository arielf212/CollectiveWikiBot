from helper_methods import *


stats_list = get_cards()
action = input(prompt_main)

if action == "1":
    submit_count = int(input(prompt_1))

    for k in range(submit_count):
        new_stats = get_card_extra(stats_list[k])

        upload_file(new_stats)
        update_infobox(new_stats)

elif action == "2":
    submit_cards = input(prompt_2)

    card_names = submit_cards.split("_-_")

    for card_name in card_names:
        for stats in stats_list:
            if card_name == stats[1]:
                new_stats = get_card_extra(stats)
                update_infobox(new_stats)

elif action == "3":
    for stats in stats_list:
        new_stats = get_card_extra(stats)
        update_infobox(new_stats)
