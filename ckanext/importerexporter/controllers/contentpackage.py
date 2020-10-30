import json

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.logic.action.get as api_get
import requests
#import ckan.lib.base as base


class ContentPackageController(toolkit.BaseController):

    def export_contentpackage(self, dataset_list):
        import logging
        log = logging.getLogger(__name__)
        log.info("# # # # # # dataset_list: " + str(dataset_list))
        #return []
        log.info("#################")
        log.info(h.full_current_url())
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }
        r = toolkit.response
        
        r.content_type = 'application/zip'
        #search_result = toolkit.get_action('get_search_results')
        #sr = pc.after_search
        #log.error(sr["count"])

        query_str = h.full_current_url()

#https://catalog.gis.lrg.tum.de/dataset/contentpackage.zip?search_query%3D%252Fdataset
#https://catalog.gis.lrg.tum.de/dataset/contentpackage.zip?search_query%3D%252Fdataset%253Fq%253D%2526sort%253Dscore%252Bdesc%25252C%252Bmetadata_modified%252Bdesc%2526ext_bbox%253D11.821289062500002%25252C47.995895410220555%25252C11.958618164062502%25252C48.10972362702285%2526ext_prev_extent%253D11.690826416015627%25252C47.96050238891509%25252C12.0904541015625%25252C48.144097934938884

        query_str_s = query_str.split("dataset/contentpackage.zip?search_query%3D%252Fdataset%253F")
        log.info("#### Query_Str_s: " + query_str_s[0])
        if len(query_str_s) == 1:
            query_str_s = query_str_s[0].split("dataset/contentpackage.zip?search_query%3D%252Fdataset")
        #search_json = query_str_s[1].replace("%253D", ":").replace("%2526", "+").replace("%25252C", ",").replace("%252C", ",").replace("%252B", "+")
        search_json = "tags:map"
        search_json = query_str_s[0] + "api/action/package_search?fq=" + search_json + "&rows=1000"
        log.info(search_json)
        #re = requests.get(search_json, verify=False)
        re = requests.get("https://catalog.gis.lrg.tum.de/api/action/package_search?fq=tags:map&rows=2", verify=False)
        response = json.loads(re.content)
        log.info("count: " + str(response["result"]["count"]))
        #dataset_list = []
        #for result in response["result"]["results"]:
        #    dataset_list.append(result["name"])
        #log.info(dataset_list)

        #dataset_list = []
        #search_params = {
        #    "rows": 3,
        #    "fq": search_json,
        #}
        #log.info("### ### ### - " + str(h.get_request_param("extras")))
        #log.info("### ### ### - " + search_json)
        #search_result = toolkit.get_action("package_search")(context, search_params)
        #log.info("### ### ### - " + str(search_result))
        #dataset_list = []
        #for result in search_result["results"]:
        #    dataset_list.append(result["name"])
        dat_list = []
        #for dd in dataset_list:
        #    dat_list.append(str(dd))
        dat_str = "[" + dataset_list[3:-2].replace("', u'", ", ") + "]"
        da_str = dataset_list[3:-2].split("', u'")
        dd_str = []
        for ddd in da_str:
            dd_str.append(ddd)
        log.info("# dat_str: " + str(dat_str))
#[u'3d-gebaudemodell', u'planungsmodelle-grafing', u'3d-stadtmodellplattform']
        
        try:
            log.info(dataset_list)
            log.info("## # ## # ## - dataset_list: " + str(dd_str))
            content_package = toolkit.get_action('search_list_show_as_contentpackage')(context,{'dataset_list': dd_str})
            #log.info("GGGGG")
        except toolkit.ObjectNotFound:
            toolkit.abort(404, 'Dataset not found')

        r.content_disposition = 'attachment; filename=CKAN_CONTENTPACKAGE.zip'

        #log.info("HHHHH")
        #log.info(content_package)
        return content_package
        #return json.dumps(datapackage_dict, indent=2)


















    def upload_form(self, data=None, errors=None, error_summary=None):
        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
            'auth_user_obj': toolkit.c.userobj,
        }
        #self._authorize_or_abort(context)

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
        #self._authorize_or_abort(context)

        try:
            params = toolkit.request.params
            upload_result = toolkit.get_action('package_create_from_contentpackage')(context, params)
            #if dataset == "error":
            #    toolkit.redirect_to("/error")
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
