import ckan.plugins.toolkit as toolkit
from ckan_datapackage_tools import converter
import json
import zipfile
import StringIO
import io
import ckanext.importerexporter.lib.util as util

def zip_dataset(dataset_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        for resource in dataset_dict["resources"]:
            if resource["mimetype"] is not None:
                try:
                    r_path = util.get_path_to_resource_file(resource)
                    r_path_zip = r_path.split("resources/")[1] + "/" + resource["url"].split("/")[-1]
                    r_file = open(r_path, "r")
                    zf.writestr("CKAN_DATASET_" + dataset_dict["name"] + "/" + r_path_zip, r_file.read())
                    r_file.close()
                except Exception as e:
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
            zf.writestr("CKAN_DATASET_" + dataset + ".zip", zip_buffer2.getvalue())
    return zip_buffer.getvalue()


