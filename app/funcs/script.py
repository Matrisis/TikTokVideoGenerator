import json
import random


def get_random_phrases(file_name, num_phrases):
    with open(file_name, 'r') as f:
        data = json.load(f)

    all_phrases = data["facts"]

    random_phrases = set()

    while len(random_phrases) < num_phrases:
        phrase = random.choice(all_phrases)
        random_phrases.add(phrase)

    return list(random_phrases)


def integrate_phrases(main_list, additional_list):
    assert len(additional_list) <= len(main_list), "La liste supplémentaire est trop longue !"

    # Crée une copie de la liste principale pour éviter de la modifier
    result_list = []
    for i, main in enumerate(main_list):
        if i > 2 and i % 2 and len(additional_list) > 0:
            result_list.append(additional_list[0])
            additional_list.pop(0)
        result_list.append(main)
    return result_list
