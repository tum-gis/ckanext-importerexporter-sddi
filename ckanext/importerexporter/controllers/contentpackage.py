import json

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.logic.action.get as api_get
import requests
from ckan.common import config


class ContentPackageController(toolkit.BaseController):

    def export_contentpackage(self, dataset_list):
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }
        r = toolkit.response
        
        r.content_type = 'application/zip'
        query_str = h.full_current_url()

        query_str_s = query_str.split("dataset/contentpackage.zip?search_query%3D%252Fdataset%253F")
        if len(query_str_s) == 1:
            query_str_s = query_str_s[0].split("dataset/contentpackage.zip?search_query%3D%252Fdataset")
        search_json = "tags:map"
        search_json = query_str_s[0] + "api/action/package_search?fq=" + search_json + "&rows=1000"
        catalog_url = config.get('ckan.site_url', '')
        if not catalog_url[-1] == "/":
            catalog_url += "/"
        re = requests.get(catalog_url + "api/action/package_search?fq=tags:map&rows=2", verify=False)
        response = json.loads(re.content)
        dat_list = []
        dat_str = "[" + dataset_list[3:-2].replace("', u'", ", ") + "]"
        da_str = dataset_list[3:-2].split("', u'")
        dd_str = []
        for ddd in da_str:
            dd_str.append(ddd)
        
        try:
            content_package = toolkit.get_action('search_list_show_as_contentpackage')(context,{'dataset_list': dd_str})
        except toolkit.ObjectNotFound:
            toolkit.abort(404, 'Dataset not found')

        r.content_disposition = 'attachment; filename=CKAN_CONTENTPACKAGE.zip'
        return content_package





    def upload_form(self, data=None, errors=None, error_summary=None):
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
            'auth_user_obj': toolkit.c.userobj,
        }

        errors = errors or {}
        error_summary = error_summary or {}
        default_data = {
            'owner_org': toolkit.request.params.get('group'),
        }
        data = data or default_data

        return toolkit.render(
            'admin/contentpackages.html',
            extra_vars={
                'data': data,
                'errors': errors,
                'error_summary': error_summary,
            }
        )
        

    def upload_contentpackage(self):
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }

        try:
            params = toolkit.request.params
            upload_result = toolkit.get_action('package_create_from_contentpackage')(context, params)
            severity = 0
            for up in upload_result:
                if up[0] == 1:
                    severity = 1
                if up[0] == 2:
                    severity = 2
            if severity == 0:
                return toolkit.render('admin/contentpackages.html', extra_vars={"data":params, "success": 0, "results":str(len(upload_result)) + " neue Informations-Ressourcen angelegt."})
            if severity == 1:
                return toolkit.render('admin/contentpackages.html', extra_vars={"data":params, "success": 1, "results":upload_result})
            if severity == 2:
                return toolkit.render('admin/contentpackages.html', extra_vars={"data":params, "success": 2, "results":upload_result})
        except toolkit.ValidationError as e:
                return toolkit.render('admin/contentpackages.html', extra_vars={"data":params, "success": 2, "results":["Das Content-Package konnte nicht gelesen werden: " + e]})
