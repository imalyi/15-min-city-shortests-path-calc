from database import MongoDatabase


def get_all_addreses():
    m = MongoDatabase()
    res = []
    inserted = set()
    for poi in m.get_all_pois():
        for main_category, sub_categories in poi.get('points_of_interest', {}).items():
            for sub_category, objects in sub_categories.items():
                for object in objects:
                    if object.get('name') in inserted:
                        continue
                    inserted.add(object.get('name'))
                    res.append({'sub_category': sub_category, 'name': object.get('name'), 'category': main_category})
    return res


def create_pois_collection():
    m = MongoDatabase()
    m.create_pois_collection()
    m.save_pois(get_all_addreses())


create_pois_collection()