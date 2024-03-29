# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug

from odoo import http, _
from odoo.http import request


class MassMailController(http.Controller):

    @http.route(['/mail/mailing/<int:mailing_id>/unsubscribe'], type='http', website=True, auth='public')
    def mailing(self, mailing_id, email=None, res_id=None, **post):
        mailing = request.env['mail.mass_mailing'].sudo().browse(mailing_id)
        if mailing.exists():
            res_ids = []
            if mailing.mailing_model == 'mail.mass_mailing.contact':
                contacts = request.env['mail.mass_mailing.contact'].sudo().search([
                    ('email', '=', email),
                    ('list_id', 'in', [mailing_list.id for mailing_list in mailing.contact_list_ids])
                ])
                res_ids = contacts.ids
            else:
                res_ids = [res_id]
            mailing.update_opt_out(email, res_ids, True)
            return _('You have been unsubscribed successfully')

    @http.route('/page', auth='public', method=['GET'],website=True,type='http')
    def trial_check(self, **post):
        print 'Callllllllllllllllllllllllled'
        return request.render('website.register')

    @http.route(['/some_url'], type='json', auth="user", website=True)

    def input_data_processing(self, **kw):

        cr, context, pool, uid = request.cr, request.context, request.registry, request.uid



        #Fetch input json data sent from js

        input_data = kw.get('input_data')
        print('---------------------------------------------------',input_data)


        # Your code is here 


        return {

               'output_data' : output_data

        }

    @http.route('/mail/track/<int:mail_id>/blank.gif', type='http', auth='none')
    def track_mail_open(self, mail_id, **post):
        """ Email tracking. """
        request.env['mail.mail.statistics'].sudo().set_opened(mail_mail_ids=[mail_id])
        response = werkzeug.wrappers.Response()
        response.mimetype = 'image/gif'
        response.data = 'R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='.decode('base64')

        return response

    @http.route('/r/<string:code>/m/<int:stat_id>', type='http', auth="none")
    def full_url_redirect(self, code, stat_id, **post):
        # don't assume geoip is set, it is part of the website module
        # which mass_mailing doesn't depend on
        country_code = request.session.get('geoip', False) and request.session.geoip.get('country_code', False)

        request.env['link.tracker.click'].add_click(code, request.httprequest.remote_addr, country_code, stat_id=stat_id)
        return werkzeug.utils.redirect(request.env['link.tracker'].get_url_from_code(code), 301)




#     @http.route('/page', auth='public', method=['GET'],website=True,type='http')
#     def trial_check(self, **post):
#         print 'Callllllllllllllllllllllllled'
#         return request.render('website.register')