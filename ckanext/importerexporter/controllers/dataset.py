import json

import ckan.model as model
import ckan.plugins.toolkit as toolkit


class DatasetController(toolkit.BaseController):

    def export_dataset(self, package_id):
        '''Return the given dataset as a Data Package JSON file.

        '''
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }
        r = toolkit.response
        
        r.content_type = 'application/zip'

        try:
            datapackage_dict = toolkit.get_action('dataset_show_as_dataset')(context,{'id': package_id})
        except toolkit.ObjectNotFound:
            toolkit.abort(404, 'Dataset not found')

        r.content_disposition = 'attachment; filename=CKAN_DATASET_'+datapackage_dict[0]+'.zip'.format(package_id)

        return datapackage_dict[1]
