import ckan.plugins.toolkit as toolkit
from ckan_datapackage_tools import converter
import json
import zipfile
import StringIO
import io
import ckanext.importerexporter.lib.util as util

import logging
log = logging.getLogger(__name__)

def zip_dataset(dataset_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        for resource in dataset_dict["resources"]:
            if resource["mimetype"] is not None:
                try:
                    r_path = util.get_path_to_resource_file(resource)
                    r_path_zip = r_path.split("resources/")[1] + "/" + resource["url"].split("/")[-1]
                    log.error("###: " + str(r_path))
                    log.error("####: " + str(r_path_zip))
                    r_file = open(r_path, "r")
                    zf.writestr("CKAN_DATASET_" + dataset_dict["name"] + "/" + r_path_zip, r_file.read())
                    r_file.close()
                except Exception as e:
                    log.error("## ckanext-importer-exporter ERROR ##: " + str(e))
        zf.writestr("CKAN_DATASET_" + dataset_dict["name"] + "/dataset.json", json.dumps(dataset_dict, indent=2))
    return zip_buffer

@toolkit.side_effect_free
def dataset_show_as_dataset(context, data_dict):
    '''Return the given CKAN dataset into a Data Package.

    This returns just the data package metadata in JSON format (what would be
    the contents of the datapackage.json file), it does not return the whole
    multi-file package including datapackage.json file and additional data
    files.

    :param id: the ID of the dataset
    :type id: string

    :returns: the datapackage metadata
    :rtype: JSON

    '''
    try:
        dataset_id = data_dict['id']
    except KeyError:
        raise toolkit.ValidationError({'id': 'missing id'})

    dataset_dict = toolkit.get_action('package_show')(context, {'id': dataset_id})


    #zip_buffer = io.BytesIO()
    #with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
    #    for resource in dataset_dict["resources"]:
    #        try:
    #            r_path = util.get_path_to_resource_file(resource)
    #            file_name = resource["url"].split("/")
    #            r_file = open(r_path, "r")
    #            zf.writestr(file_name[-1], r_file.read())
    #            r_file.close()
    #        except:
    #            pass
    #    zf.writestr("dataset.json", json.dumps(dataset_dict, indent=2))
    zip_buffer = zip_dataset(dataset_dict)
    return [dataset_dict["name"], zip_buffer.getvalue()]









#@toolkit.side_effect_free
def search_list_show_as_contentpackage(context, dataset_list):
    '''Return the given CKAN dataset into a Data Package.

    This returns just the data package metadata in JSON format (what would be
    the contents of the datapackage.json file), it does not return the whole
    multi-file package including datapackage.json file and additional data
    files.

    :param id: the ID of the dataset
    :type id: string

    :returns: the datapackage metadata
    :rtype: JSON

    '''
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:

        for dataset in dataset_list["dataset_list"]:
            dataset_dict = toolkit.get_action('package_show')(context, {'id': dataset})
            zip_buffer2 = zip_dataset(dataset_dict)
        #    zip_buffer2 = io.BytesIO()
        #    with zipfile.ZipFile(zip_buffer2, "a", zipfile.ZIP_DEFLATED, False) as zf2:
        #try:
        #    dataset_id = dataset['id']
        #except KeyError:
        #    raise toolkit.ValidationError({'id': 'missing id'})

                #import logging
                #log = logging.getLogger(__name__)
                #log.info("Dataset-ID ######### : " + str(dataset_list))
                #log.info("Dataset-ID ######### : " + dataset)
#
#                dataset_dict = toolkit.get_action('package_show')(context, {'id': dataset})
#
#
#   
#                for resource in dataset_dict["resources"]:
#                    try:
#                        r_path = util.get_path_to_resource_file(resource)
#                        file_name = resource["url"].split("/")
#                        r_file = open(r_path, "r")
#                        zf2.writestr(file_name[-1], r_file.read())
#                        r_file.close()
#                    except:
#                        pass
#                zf2.writestr("dataset.json", json.dumps(dataset_dict, indent=2))
            zf.writestr("CKAN_DATASET_" + dataset + ".zip", zip_buffer2.getvalue())
    return zip_buffer.getvalue()


