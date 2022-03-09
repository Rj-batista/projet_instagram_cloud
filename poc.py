import os
import json


def extract_like_by_id(df_json, number_to_scrap):
    list_like = []
    for item in range(number_to_scrap):
        id_item = str(df_json["GraphImages"][item]["id"])
        id_item = "_" + id_item + "_image{}".format(item)
        item = df_json["GraphImages"][item]["edge_media_preview_like"]
        item[id_item] = item.pop("count")
        list_like.append(item)
    return list_like


def write_json(dict_json):
    with open('peugeot_poc.json', 'w', encoding='utf-8') as f:
        json.dump(dict_json, f, ensure_ascii=False, indent=4)


class scrap:
    def __init__(self, profil_scrap, number_scrap):
        self.username = ""
        self.password = ""
        self.profil_scrap = profil_scrap

        self.number_scrap = number_scrap
        os.system(
            "instagram-scraper {} -u {} -p {} -m {} --comments -t image --cookiejar "
            "cookie.jar --latest "
            .format(self.profil_scrap, self.username, self.password, self.number_scrap))

    def read_json(self):
        file = open("{}/{}.json".format(self.profil_scrap, self.profil_scrap), encoding='utf-8')
        data = json.load(file)
        return data


if __name__ == '__main__':
    profils_scrap = "peugeot"
    number_scrap = 5
    tool = scrap(profils_scrap, number_scrap)
    use_data = tool.read_json()
    first_fct = extract_like_by_id(use_data, number_scrap)
    write_json(first_fct)
