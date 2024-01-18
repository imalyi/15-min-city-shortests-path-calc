import json
from database import MongoDatabase


def read_categories():
    categories = set()
    with open("data.json", "r", encoding="utf8") as f:
        data = json.loads(f.read())
    for line in data:
        for category in line.get('categories'):
            categories.add(category)
    return categories


def save_categories():
    res = {'unknown': []}
    categories = read_categories()
    for category in categories:
        res['unknown'].append(category)
    with open("categories.json", "w", encoding="utf8") as f:
        f.write(json.dumps(res, indent=4, ensure_ascii=False))


def save_categories_to_db():
    with open("categories.json", "r") as f:
        data = json.loads(f.read())

    last_id = 0
    new_data = {}
    for category, items in data.items():
        for item in items:
            if not new_data.get(category):
                new_data[category] = []
            new_data[category].append({'id': last_id, 'name': item})
            last_id += 1

    db = MongoDatabase()
    db.insert_categories(new_data)



save_categories_to_db()