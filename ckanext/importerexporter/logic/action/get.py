import ckan.plugins.toolkit as toolkit
from ckan_datapackage_tools import converter
import requests
#import ruamel.std.zipfile as zipfile
import json
import zipfile
import StringIO
import io


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

    dataset_dict = toolkit.get_action('package_show')(context,
                                                      {'id': dataset_id})


    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        for resource in dataset_dict["resources"]:
            if resource["mimetype"] is not None:
                r = requests.get(resource["url"], verify=False)
                file_name = resource["url"].split("/")
                zf.writestr(file_name[-1], r.content)
        zf.writestr("dataset.json", json.dumps(dataset_dict, indent=2))
    return zip_buffer.getvalue()






