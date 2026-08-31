# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Swetha Anand (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
import json
import logging
import traceback
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

_logger = logging.getLogger(__name__)


class XLSXReportController(http.Controller):
    @http.route('/xlsx_report', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, data, output_format, report_name, report_action, options=None):
        """Generate an XLSX report based on the provided data and return it as
        a response.
            Args:
                model (str): The name of the model on which the report is based.
                data (str): The data required for generating the report.
                output_format (str): The desired output format for the report
                (e.g., 'xlsx').
                report_name (str): The name to be given to the generated report
                file.
            Returns:
                Response: The generated report file as a response.
            Raises:
                Exception: If an error occurs during report generation.
            """
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(data, response, report_name,
                                           report_action)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            _logger.exception(
                "Dynamic report XLSX generation failed for model %s "
                "(report_action=%s)", model, report_action)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': {
                    'name': '%s.%s' % (type(e).__module__, type(e).__name__),
                    'message': str(e),
                    'arguments': [str(arg) for arg in e.args],
                    'context': {},
                    'debug': ''.join(
                        traceback.format_exception(
                            type(e), e, e.__traceback__)),
                },
            }
            return request.make_response(html_escape(json.dumps(error)))
