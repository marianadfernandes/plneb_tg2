import json

file = open("sim.json", encoding='utf-8')
sim = dict(json.load(file))
file.close()

category_dict = {}

for key, values in sim.items():
    if not values:  # Check if the list is empty
        category = "No Category"
    else:
        max_value = float('-inf')  # Initialize with a very small value
        max_term = ""

        for item in values:
            for term, value in item.items():
                if value > max_value:
                    max_value = value
                    max_term = term

        category = max_term

    if category not in category_dict:
        category_dict[category] = []

    category_dict[category].append(key)

with open('sim_cat.json', 'w', encoding="utf8") as file:
    json.dump(category_dict, file, ensure_ascii=False, indent=4)