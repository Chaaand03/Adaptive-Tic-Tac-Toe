import bs4 as bs
import random


def get_question(parsed_data,correct_count):

    data = {}
    if correct_count == 0:
        random_number = random.randint(0, 4)
    elif correct_count == 1:
        random_number = random.randint(5, 9)
    else:
        random_number = random.randint(10,14)

    data["question"] = parsed_data["questions"][random_number]
    options = []
    start_index = random_number * 4
    options.append(parsed_data["answers"][start_index])
    options.append(parsed_data["answers"][start_index + 1])
    options.append(parsed_data["answers"][start_index + 2])
    options.append(parsed_data["answers"][start_index + 3])
    data["options"] = options
    data['ans'] = parsed_data["correct_answers"][random_number]

    return data



