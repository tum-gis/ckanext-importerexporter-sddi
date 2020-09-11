import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.importerexporter.logic.action.get


class ImporterexporterPlugin(plugins.SingletonPlugin):
    '''Plugin that adds importing/exporting datasets as Data Packages.
    '''
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    def before_map(self, map_):
        map_.connect(
            'export_dataset',
            '/datahub_resource/{package_id}/dataset.zip',
            controller='ckanext.importerexporter.controllers.dataset:DatasetController',
            action='export_dataset'
        )
        return map_

    def get_actions(self):
        return {
            'dataset_show_as_dataset':
                ckanext.importerexporter.logic.action.get.dataset_show_as_dataset,
        }
