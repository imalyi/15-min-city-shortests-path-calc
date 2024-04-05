import json


class TrojmiastoplCategoryMapper:
    def __init__(self):
        self.reversed_dict = {}
        self.make_mapper()

    def get_categories_data(self):
        with open("categories.json", "r") as data_file:
            return json.loads(data_file.read())

    def make_mapper(self):
        for main_cagegory, sub_categories in self.get_categories_data().items():
            for sub_category, values in sub_categories.items():
                for value in values:
                    self.reversed_dict[value] = {'main': main_cagegory, 'sub': sub_category}

    def map(self, raw_category):
        return self.reversed_dict.get(raw_category)


class TrojmiastoplCategoryChanger:
    def __init__(self):
        self.data = []
        self.mapper = TrojmiastoplCategoryMapper()

    def get_raw_data(self):
        with open("data.json", "r") as data_file:
            return json.loads(data_file.read())

    def transform_data(self):
        for raw_row in self.get_raw_data():
            for category in raw_row.get('categories'):
                new_category = self.mapper.map(category.lower())
                if not new_category:
                    continue
                self.data.append({'categories': new_category, 'name': raw_row.get('name'), 'address': raw_row.get('address')})
        return self.data

    def save(self):
        with open("recategorized_data.json", "w") as f:
            f.write(json.dumps(self.transform_data(), indent=4, ensure_ascii=False))


TrojmiastoplCategoryChanger().save()
