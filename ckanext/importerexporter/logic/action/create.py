import random
import cgi
import json
import tempfile
import zipfile
from StringIO import StringIO
from io import BytesIO
import os
import os.path
from os import path
from ckan.common import config
import shutil
import ckan.model as model

import ckan.plugins.toolkit as toolkit
from ckan_datapackage_tools import converter
import requests

import datapackage

def create_package(context, dataset, dataset_name):
    #try:
    if True:
        zf = None
        zf = dataset
        json_dataset = json.loads(zf.open(dataset_name + "/dataset.json").read())
        json_dataset["licence_agreement"] = ["licence_agreement_check"]
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }
        present_dataset = None
        try:
            present_dataset = toolkit.get_action("package_show")(context, {"id":json_dataset["name"]})
        except:
            pass
        if present_dataset is not None:
            return [1, "Datensatz bereits vorhanden: ", json_dataset["name"], json_dataset["title"]]
        resources = json_dataset["resources"]
        json_dataset["resources"] = []
        json_dataset.pop("id", None)
        package_id = "1234"
        package_id2 = toolkit.get_action("package_create")(context, json_dataset)
        package_id = package_id2["id"]
        resource_replacer = []
        for resource in resources:
            resource["package_id"] = package_id
            resource_url = resource["url"]
            resource_id2 = resource["id"]
            resource_p_id = resource["package_id"]
            if resource["mimetype"] is not None:
                r_url = resource["url"]
                r_id = resource["id"]
                r_name = r_url.split("/")[-1]
                r_path = r_id[0:3] + "/" + r_id[3:6] + "/" + r_id[6:] + "/" + r_name
                headers = {u'content-disposition': u'form-data; name="' + resource["name"] + '"; filename="' + r_name + '"', u'content-length': resource["size"], u'content-type': resource["mimetype"]}
                environ = {'REQUEST_METHOD': 'POST'}
                content = zf.open(dataset_name + "/" + r_path).read()
                fp = BytesIO(content)
                resource["upload"] = cgi.FieldStorage(fp=fp, headers=headers, environ=environ)
            resource_id = toolkit.get_action("resource_create")(context, resource)
            resource_replacer.append([resource_url, resource_id["url"], resource_p_id, resource_id2, resource_id["package_id"], resource_id["id"]])

        dataset_new = toolkit.get_action("package_show")(context, {"id":json_dataset["name"]})
        description = dataset_new["notes"]
        for rr in resource_replacer:
            description = description.replace(rr[0], rr[1])
            description = description.replace(rr[2] + "/resource/" + rr[3], rr[4] + "/resource/" + rr[5])
        dataset_new["notes"] = description
        toolkit.get_action("package_update")(context, dataset_new)

        if package_id == "1234":
            return [2, "Fehler beim erstellen des Datensatzes: " + json_dataset["title"]]
        else:
            return [0]
    #except Exception as e:
    #    return [2, e]
    return [0]


def package_create_from_contentpackage(context, data_dict):
    '''Create a new dataset (package) from a Data Package file.

    :param url: url of the datapackage (optional if `upload` is defined)
    :type url: string
    :param upload: the uploaded datapackage (optional if `url` is defined)
    :type upload: cgi.FieldStorage
    :param name: the name of the new dataset, must be between 2 and 100
        characters long and contain only lowercase alphanumeric characters,
        ``-`` and ``_``, e.g. ``'warandpeace'`` (optional, default:
        datapackage's name concatenated with a random string to avoid
        name collisions)
    :type name: string
    :param private: the visibility of the new dataset
    :type private: bool
    :param owner_org: the id of the dataset's owning organization, see
        :py:func:`~ckan.logic.action.get.organization_list` or
        :py:func:`~ckan.logic.action.get.organization_list_for_user` for
        available values (optional)
    :type owner_org: string
    '''
    dataset_results = []
    try:
        url = data_dict.get('url')
        upload = data_dict.get('upload')
        upload_file = None
        file_name = ""
        is_from_url = False
        if isinstance(upload, unicode):
            is_from_url = True
            upload_file = requests.get(url)
            file_name = url.split("/")[-1]
            headers = {u'content-disposition': u'form-data; name="' + "upload" + '"; filename="' + file_name + '"',}
            environ = {'REQUEST_METHOD': 'POST'}
            fp = zipfile.ZipFile(BytesIO(upload_file.content))
            upload_file = zipfile.ZipFile(BytesIO(upload_file.content))
        else:
            upload_file = upload.file
            file_name = data_dict["url"]
        package_id = ""
        error = False
        if file_name[0:13] == "CKAN_DATASET_":
            if not is_from_url:
                zip_file2 = StringIO()
                zip_file2.write(upload_file.read())
                upload_file = zipfile.ZipFile(zip_file2)
            dataset_results.append(create_package(context, upload_file, file_name[:-4]))
        if file_name[0:19] == "CKAN_CONTENTPACKAGE":
            zf = upload_file
            if not is_from_url:
                zip_file = StringIO()
                zip_file.write(upload_file.read())
                zf = zipfile.ZipFile(zip_file)
            file_list = zf.namelist()
            for file in file_list:
                zip_file2 = StringIO()
                zip_file2.write(zf.open(file).read())
                zf2 = zipfile.ZipFile(zip_file2)
                dataset_results.append(create_package(context, zf2, file[:-4]))
        return dataset_results
    except Exception as e:
        dataset_results.append([2, e])
        return dataset_results
