import random
import cgi
import json
import tempfile
import zipfile
from StringIO import StringIO
from io import BytesIO
import os.path
from os import path
from ckan.common import config
import shutil
import ckan.model as model

#zip_buffer = io.BytesIO()
#with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:

#import six

import ckan.plugins.toolkit as toolkit
from ckan_datapackage_tools import converter

import logging
log = logging.getLogger(__name__)

import datapackage


def create_package(context, dataset, dataset_name):
    #log.error(dataset)
    #return "error"
    try:
    #if True:


    #if True:
        zf = None
        #if is_content_package:
            #zipfile.write(dataset.seek(0))
            #zf = zipfile.ZipFile(dataset)
        #else:
            #zip_file = StringIO()
            #zip_file.write(dataset.file.read())
            #zf = zipfile.ZipFile(zip_file)
        zf = dataset
        #log.error("##: File: " + str(dataset.filename))
        #json_dataset = json.loads(zf.open(dataset.filename.split(".zip")[0] + "/dataset.json").read())
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
            log.error("GGGGGGG: " + str(present_dataset))
            return [1, "Datensatz bereits vorhanden: ", json_dataset["name"], json_dataset["title"]]
        
        #log.error("HHHHH: " + str(present_dataset))
        #return

        #log.error("##: " + str(json_dataset))
        #resource_list = zf.namelist()
        #resoure_list = [r for r in resource_list if not r == "dataset.json"]
        #create_package(json_dataset, resource_list, context)
        resources = json_dataset["resources"]
        json_dataset["resources"] = []
        json_dataset.pop("id", None)
        #context["return_id_only"] = True
        package_id = "1234"
        package_id = toolkit.get_action("package_create")(context, json_dataset)
        log.error("##### - ##### Created Package (name) : " + str(package_id["name"]))
        log.error("##### - ##### Created Package (id): " + str(package_id["id"]))
        #log.error("##### - ##### Created Package (num resources): " + str(len(package_id["resources"])))
        package_id = package_id["id"]
        for resource in resources:
            resource["package_id"] = package_id
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
            resource.pop("id", None)
            #log.error("##### - ##### Resource: " + str(resource))
            resource_id = toolkit.get_action("resource_create")(context, resource)
            log.error("##### - ##### Created Resource (name): " + str(resource_id["name"].encode("utf-8")))
            log.error("##### - ##### Created Resource (id): " + str(resource_id["id"]))
            log.error("##### - ##### Created Resource (dataset-id): " + str(resource_id["package_id"]))
    #        r_url = resource["url"]
    #        r_id = resource["id"]
    #        r_name = r_url.split("/")[-1]
    #        r_path = r_id[0:3] + "/" + r_id[3:6] + "/" + r_id[6:] + "/" + r_name
    #        r_path_storage = r_id[0:3] + "/" + r_id[3:6] + "/" + r_id[6:]# + "/" + r_name
    #        storage_path = config.get('ckan.storage_path', '')
    #        if storage_path[-1] != "/":
    #            storage_path += "/"
    #        storage_path += "resources/"
    #        log.error("## -- ## -- ## File path: " + storage_path + r_path_storage)
    #        #if path.exists(storage_path + r_path_storage):
    #        #    log.error("## -- ## -- ## File exists!: " + storage_path + r_path_storage)
    #        #else:
    #        #    if not path.exists(storage_path + r_id[0:3]):
    #        #        os.mkdir(storage_path + r_id[0:3])
    #        #    if not path.exists(storage_path + r_id[3:6]):
    #        #        os.mkdir(storage_path + r_id[0:3] + "/" + r_id[3:6])
    #        #    #file = zf.open(dataset.filename.split(".zip")[0] + "/" + r_path).read()
    #        #    #shutil.copy(file, storage_path + r_path_storage)
    #        #    zf.extract(dataset.filename.split(".zip")[0] + "/" + r_path, storage_path + r_id[0:3] + "/" + r_id[3:6])
    #        #    shutil.copy(storage_path + r_id[0:3] + "/" + r_id[3:6] + "/" + dataset.filename.split(".zip")[0] + "/" + r_path, storage_path + r_path_storage)
            #    shutil.rmtree(storage_path + r_id[0:3] + "/" + r_id[3:6] + "/" + dataset.filename.split(".zip")[0])
        if package_id == "1234":
            return [2, "Fehler beim erstellen des Datensatzes: " + json_dataset["title"]]
        else:
            return [0]
    except Exception as e:
        return [2, e]
    return
            
                
    #        #log.error("##: " + str(r_path))
    #        #return
            #headers = {u'content-disposition': u'form-data; name="' + resource["name"] + '"; filename="' + r_name + '"', u'content-length': resource["size"], u'content-type': resource["mimetype"]}
   #         environ = {'REQUEST_METHOD': 'POST'}
   #         content = zf.open(dataset.filename.split(".zip")[0] + "/" + r_path).read()
   #         fp = BytesIO(content)
   #         #resource["upload"] = zf.open(dataset.filename.split(".zip")[0] + "/" + r_path).read()#cgi.FieldStorage(fp=fp, headers=headers, environ=environ)
   #         resource["upload"] = cgi.FieldStorage(fp=fp, headers=headers, environ=environ)
   #         log.error("#F#F#F#F has attrs: " + str(hasattr(resource["upload"], 'file')) + " - " + str(hasattr(resource["upload"].file, 'read')))
   #         log.error("# image # : " + str(resource["upload"]))
   #         return
   #         #resource.pop("id", None)
   #         #resource.pop("package_id", None)
   #         #resource.pop("revision:id", None)
   #         #resource.pop("url", None)
   #         #resource["url"] = ""
   # context["return_id_only"] = True
   # #return
    #package_id = toolkit.get_action("package_create")(context, json_dataset)
   # log.error("##: " + str(package_id))
                



def create_package2(data_dict, resource_list, context):
    resource_create_list = []
    if "resources" in data_dict:
        #resource_create_list = [r for r in data_dict["resources"] if r["mimetype"] is not None]
        #data_dict["resources"] = [r for r in data_dict["resources"] if r["mimetype"] is None]
        log.info("# - # - # - : " + str(resource_create_list))
        log.info("# - # - # - : " + str(data_dict["resources"]))
    for resource in data_dict["resources"]:
        if resource["mimetype"] is not None:
            headers = {u'content-disposition': u'form-data; name="{}"; filename="{}"'.format(data_dict["name"], data_dict["url"].split("/")[-1]), u'content-length': data_dict["size"], u'content-type': data_dict["mimetype"]}
            environ = {'REQUEST_METHOD': 'POST'}
            fp = BytesIO(content)
            resource["upload"] = cgi.FieldStorage(fp=fp, headers=headers, environ=environ)
    #return
    context_package = context
    context_package["return_id_only"] = True
    data_dict["licence_agreement"] = ["licence_agreement_check"]
    log.info("# - # - # - : creating dataset...")
    package_id = toolkit.get_action("package_create")(context_package, data_dict)
    log.info("# - # - # - : " + str(package_id))
    #for resource in resource_create_list:
    #    resource.pop("url", None)
    #    context_resource = context
    #    headers = {u'content-disposition': u'form-data; name="{}"; filename="{}"'.format(name, filename), u'content-length': len(content), u'content-type': mimetype}
    #    field_storage = 
    #    resource["upload"] = field_storage
    #    package_id = toolkit.get_action("resource_create")(context, resource)
#somelist[:] = [x for x in somelist if not determine(x)]



#headers = {u'content-disposition': u'form-data; name="{}"; filename="{}"'.format(name, filename),
#               u'content-length': len(content),
#               u'content-type': mimetype}
#    environ = {'REQUEST_METHOD': 'POST'}
#    fp = BytesIO(content)
#    return cgi.FieldStorage(fp=fp, headers=headers, environ=environ)




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
    #try:
    if True:
        url = data_dict.get('url')
        upload = data_dict.get('upload')
        upload_file = None
        file_name = ""
        is_from_url = False
        if isinstance(upload, unicode):
            is_from_url = True
            log.error("KKKKKK - url : " + str(url))
            import requests
            upload_file = requests.get(url)
            #upload_file.raw.decode_content = True
            file_name = url.split("/")[-1]#.split(".zip")[0]
            headers = {u'content-disposition': u'form-data; name="' + "upload" + '"; filename="' + file_name + '"',}
            environ = {'REQUEST_METHOD': 'POST'}
            #content = zf.open(dataset.filename.split(".zip")[0] + "/" + r_path).read()
            #log.error("KKKKKK: " + str(upload_file.content))
            fp = zipfile.ZipFile(BytesIO(upload_file.content))
            log.error("KKKKKK: " + str(fp.namelist()))
            log.error("KKKKKK: " + str(file_name))
            log.error("KKKKKK: " + str(headers))
            log.error("KKKKKK: " + str(environ))
            #log.error("KKKKKK: " + str(fp.open(fp.namelist()[0]).read()))
            #upload = cgi.FieldStorage(fp=BytesIO(upload_file.content), headers=headers, environ=environ)
            log.error("KKKKKK: " + str(upload))
            upload_file = zipfile.ZipFile(BytesIO(upload_file.content))
            import os
            #log.info("############# - upload_file: " + str(os.fdopen(upload_file)))
        else:
            log.info("############# - data_dict: " + str(data_dict))
            log.info("############# - upload_file: " + str(upload.file))
            log.info("#### ## ### - url: " + str(data_dict["url"][0:13]))
            pass
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
            #if package_id == "1234":
            #    error = True
        #zip_file = StringIO()
        #zip_file.write(upload.file.read())
        #zf = zipfile.ZipFile(zip_file)
        #json_dataset = json.loads(zf.open("dataset.json").read())
        #resource_list = zf.namelist()
        #resoure_list = [r for r in resource_list if not r == "dataset.json"]
            #create_package(json_dataset, resource_list, context)
        if file_name[0:19] == "CKAN_CONTENTPACKAGE":
            log.error("#D#D#D# Content package erkannt")
            log.error(str(upload))
            zf = upload_file
            if not is_from_url:
                zip_file = StringIO()
                zip_file.write(upload_file.read())
                zf = zipfile.ZipFile(zip_file)
            file_list = zf.namelist()
            #file_list = upload_file.namelist()
            for file in file_list:
                log.error("#D#D#D# Content package part")
                #headers = {u'content-disposition': u'form-data; name="' + file_name + '"; filename="' + file_name + '"',}
                #environ = {'REQUEST_METHOD': 'POST'}
                #content = zf.open(dataset.filename.split(".zip")[0] + "/" + r_path).read()
                #fp = BytesIO(zf.read(file))
                #upload = cgi.FieldStorage(fp=fp, headers=headers, environ=environ)
                #f = zf.read(file)
                #package_id = create_package(StringIO(f), context, False)
                zip_file2 = StringIO()
                zip_file2.write(zf.open(file).read())
                zf2 = zipfile.ZipFile(zip_file2)
                dataset_results.append(create_package(context, zf2, file[:-4]))
                #if package_id == "1234":
                #    error = True
                #break
            #zip_file2 = StringIO()
            #zip_file2.write(zf.open(file).read())
            #zf2 = zipfile.ZipFile(zip_file2)
            #json_dataset = json.loads(zf2.open("dataset.json").read())
            #resource_list = zf2.namelist()
            #resoure_list = [r for r in resource_list if not r == "dataset.json"]
            #create_package(json_dataset, resource_list, context)
        return dataset_results
    #except Exception as e:
    #    dataset_results.append([2, e])
    #    return dataset_results

    log.info("############# - dataset: " + str(json_dataset))
    toolkit.get_action("package_create")(context, json_dataset)
        
    return
    #with open(upload.file) as f:
    #log.info("### ### ### file: " + str(upload.file.read()))
    zip_file = StringIO()
    zip_file.write(upload.file.read())
    zf = zipfile.ZipFile(zip_file)
    file_list = zf.namelist()
    json_dataset = json.loads(zf.open("dataset.json").read())

    log.info("############# - dataset: " + str(json_dataset))
    toolkit.get_action("package_create")(context, json_dataset)

    #log.info("## ## ## - zf: " + str(zf.namelist()))
    #dp = datapackage.DataPackage(upload.file)
    #dataset_dict = converter.datapackage_to_dataset(dp)
    #log.info("############# - dataset_dict: " + str(dataset_dict))
    

    return True


    if not url and not _upload_attribute_is_valid(upload):
        msg = {'url': ['you must define either a url or upload attribute']}
        raise toolkit.ValidationError(msg)



    dp = _load_and_validate_datapackage(url=url, upload=upload)

    dataset_dict = converter.datapackage_to_dataset(dp)

    owner_org = data_dict.get('owner_org')
    if owner_org:
        dataset_dict['owner_org'] = owner_org

    private = data_dict.get('private')
    if private:
        dataset_dict['private'] = toolkit.asbool(private)

    name = data_dict.get('name')
    if name:
        dataset_dict['name'] = name

    resources = dataset_dict.get('resources', [])
    if resources:
        del dataset_dict['resources']

    # Create as draft by default so if there's any issue on creating the
    # resources and we're unable to purge the dataset, at least it's not shown.
    dataset_dict['state'] = 'draft'
    res = _package_create_with_unique_name(context, dataset_dict, name)

    dataset_id = res['id']

    if resources:
        try:
            _create_resources(dataset_id, context, resources)
            res = toolkit.get_action('package_show')(
                context, {'id': dataset_id})
        except Exception as e:
            try:
                toolkit.get_action('package_delete')(
                    context, {'id': dataset_id})
            except Exception as e2:
                six.raise_from(e, e2)
            else:
                raise e

    res['state'] = 'active'
    return toolkit.get_action('package_update')(context, res)


def _load_and_validate_datapackage(url=None, upload=None):
    try:
        if _upload_attribute_is_valid(upload):
            dp = datapackage.DataPackage(upload.file)
        else:
            dp = datapackage.DataPackage(url)

        dp.validate()
    except (datapackage.exceptions.DataPackageException,
            datapackage.exceptions.SchemaError,
            datapackage.exceptions.ValidationError) as e:
        msg = {'datapackage': [e.message]}
        raise toolkit.ValidationError(msg)

    if not dp.safe():
        msg = {'datapackage': ['the Data Package has unsafe attributes']}
        raise toolkit.ValidationError(msg)

    return dp


def _package_create_with_unique_name(context, dataset_dict, name=None):
    res = None
    if name:
        dataset_dict['name'] = name

    try:
        res = toolkit.get_action('package_create')(context, dataset_dict)
    except toolkit.ValidationError as e:
        if not name and \
           'That URL is already in use.' in e.error_dict.get('name', []):
            random_num = random.randint(0, 9999999999)
            name = '{name}-{rand}'.format(name=dataset_dict.get('name', 'dp'),
                                          rand=random_num)
            dataset_dict['name'] = name
            res = toolkit.get_action('package_create')(context, dataset_dict)
        else:
            raise

    return res


def _create_resources(dataset_id, context, resources):
    for resource in resources:
        resource['package_id'] = dataset_id
        if resource.get('data'):
            _create_and_upload_resource_with_inline_data(context, resource)
        elif resource.get('path'):
            _create_and_upload_local_resource(context, resource)
        else:
            toolkit.get_action('resource_create')(context, resource)


def _create_and_upload_resource_with_inline_data(context, resource):
    prefix = resource.get('name', 'tmp')
    data = resource['data']
    del resource['data']
    if not isinstance(data, basestring):
        data = json.dumps(data, indent=2)

    with tempfile.NamedTemporaryFile(prefix=prefix) as f:
        f.write(data)
        f.seek(0)
        _create_and_upload_resource(context, resource, f)


def _create_and_upload_local_resource(context, resource):
    path = resource['path']
    del resource['path']
    if isinstance(path, list):
        path = path[0]
    try:
        with open(path, 'r') as f:
            _create_and_upload_resource(context, resource, f)
    except IOError:
        msg = {'datapackage': [(
            "Couldn't create some of the resources."
            " Please make sure that all resources' files are accessible."
        )]}
        raise toolkit.ValidationError(msg)


def _create_and_upload_resource(context, resource, the_file):
    resource['url'] = 'url'
    resource['url_type'] = 'upload'
    resource['upload'] = _UploadLocalFileStorage(the_file)
    toolkit.get_action('resource_create')(context, resource)


def _upload_attribute_is_valid(upload):
    return hasattr(upload, 'file') and hasattr(upload.file, 'read')


class _UploadLocalFileStorage(cgi.FieldStorage):
    def __init__(self, fp, *args, **kwargs):
        self.name = fp.name
        self.filename = fp.name
        self.file = fp
