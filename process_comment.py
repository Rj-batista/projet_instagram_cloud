from google.cloud import storage, bigquery
import os
import re
import json
import pandas as pd


def extract_number_comment(df_json, number_to_scrap):
    comment_number = []
    for item in range(number_to_scrap):
        item = df_json["GraphImages"][item]["edge_media_to_comment"]
        tmp = item['count']
        comment_number.append(tmp)
    return comment_number


def extract_like_by_id(df_json, number_to_scrap):
    liste_image_id = []
    liste_like_count = []
    for item in range(number_to_scrap):
        id_item = str(df_json["GraphImages"][item]["id"])
        id_item = "_" + id_item + "_image{}".format(item)
        item = df_json["GraphImages"][item]["edge_media_preview_like"]
        item[id_item] = item.pop("count")
        for key, value in item.items():
            liste_image_id.append(key)
            liste_like_count.append(value)
    dict_tmp = {'Image_Id': liste_image_id, 'Likes': liste_like_count}
    df_like = pd.DataFrame(dict_tmp)
    return df_like


def extract_comment(df_json, number_to_scrap, list_comment):
    list_of_comment = []
    for nb_scrap in range(number_to_scrap):
        for np_co in range(list_comment[nb_scrap] - 10):
            line = df_json["GraphImages"][nb_scrap]["comments"]["data"][np_co]["text"]
            list_of_comment.append(line)
    df = pd.DataFrame(list_of_comment, columns=['Comments'])
    return df


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
    first_fct = extract_number_comment(use_data, number_scrap)
    second_fct = extract_like_by_id(use_data, number_scrap)
    second_fct.to_csv("{}_likes.csv".format(profils_scrap), index=False)

    df_tmp = extract_comment(use_data, number_scrap, first_fct)
    df_comments = df_tmp.Comments.str.split("\n", expand=True).stack()
    df_comments.to_csv("{}_comment.csv".format(profils_scrap), index=False)

    ''' 
    Envoi du csv avec les commentaires sur GCS et sur BQ 
    Ici sur GCS
    '''
    client = storage.Client.from_service_account_json(json_credentials_path="",
                                                      project='')
    bucket = client.get_bucket('bucket_deployment')
    blob = bucket.blob("peugeot/peugeot_comment.csv")
    blob.upload_from_filename("peugeot_comment.csv")
    '''
    Ici pour les likes 
    '''
    blob_likes = bucket.blob("peugeot/peugeot_likes.csv")
    blob_likes.upload_from_filename("peugeot_likes.csv")

    '''
    Ici sur BQ pour les commentaires
    '''
    client = bigquery.Client.from_service_account_json(json_credentials_path="",
                                                       project='')
    table_id = "projet-cloud-instagram.insta_peugeot.insta_peugeot_comment"
    table_id_likes = "projet-cloud-instagram.insta_peugeot.insta_peugeot_likes"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Comments", "STRING"),
        ],
    )
    uri = "gs://bucket_deployment/peugeot/peugeot_comment.csv"
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    load_job.result()
    destination_table = client.get_table(table_id)

    '''
    Ici pour les likes sur BQ 
    '''
    job_config_likes = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Image_Id", "STRING"),
            bigquery.SchemaField("Likes", "INTEGER"),
        ],
    )
    uri_likes = "gs://bucket_deployment/peugeot/peugeot_likes.csv"
    load_job_likes = client.load_table_from_uri(
        uri_likes, table_id_likes, job_config=job_config_likes
    )
    load_job_likes.result()
    destination_table = client.get_table(table_id_likes)