import json

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import ckan.logic as logic


class ContentPackagesController(toolkit.BaseController):

    def contentpackages(self):
        c = base.c
        context = {'model': model,
                   'user': c.user, 'auth_user_obj': c.userobj}
        try:
            logic.check_access('sysadmin', context, {})
        except logic.NotAuthorized:
            base.abort(403, _('Need to be system administrator to administer'))
        c.revision_change_state_allowed = True

        return base.render('admin/contentpackages.html')

        context = {
            'model': model,
            'session': model.Session,
            'user': toolkit.c.user,
        }
        self._authorize_or_abort(context)

        try:
            params = toolkit.request.params
            dataset = toolkit.get_action('package_create_from_datapackage')(
                context,
                params,
            )
            toolkit.redirect_to(controller='package',
                                action='read',
                                id=dataset['name'])
        except toolkit.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.new(data=params,
                            errors=errors,
                            error_summary=error_summary)
