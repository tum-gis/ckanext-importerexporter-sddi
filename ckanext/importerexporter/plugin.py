import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.importerexporter.logic.action.get
import ckanext.importerexporter.logic.action.create
import ckanext.importerexporter.controllers.contentpackage as cp
import ckan.lib.base as base
import ckan.lib.helpers as h


class ImporterexporterPlugin(plugins.SingletonPlugin):
    '''Plugin that adds importing/exporting datasets as Data Packages.
    '''
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    def before_map(self, map_):
        map_.connect(
            'export_dataset',
            '/datahub_resource/{package_id}/dataset.zip',
            controller='ckanext.importerexporter.controllers.dataset:DatasetController',
            action='export_dataset')

        map_.connect(
            'export_contentpackage',
            '/contentpackage/{dataset_list}/contentpackage.zip',
            controller='ckanext.importerexporter.controllers.contentpackage:ContentPackageController',
            action='export_contentpackage')

        map_.connect(
            'contentpackages',
            '/ckan-admin/contentpackages',
            controller='ckanext.importerexporter.controllers.contentpackage:ContentPackageController',
            action='upload_form',
            conditions=dict(method=['GET']))
        map_.connect(
            'contentpackages',
            '/ckan-admin/contentpackages',
            controller='ckanext.importerexporter.controllers.contentpackage:ContentPackageController',
            action='upload_contentpackage',
            conditions=dict(method=['POST']))

        return map_

    def before_search(self, search_params):
        search_params["rows"] = 1000
        return search_params


    def after_search(self, search_result, search_params):
        self.search_result = search_result
        self.s_result = search_params
        base.render('set_url_str.html')
        return search_result



    def get_actions(self):
        return {
            'dataset_show_as_dataset':
                ckanext.importerexporter.logic.action.get.dataset_show_as_dataset,
            'search_list_show_as_contentpackage':
                ckanext.importerexporter.logic.action.get.search_list_show_as_contentpackage,
            'package_create_from_contentpackage':
                ckanext.importerexporter.logic.action.create.package_create_from_contentpackage,
        }


