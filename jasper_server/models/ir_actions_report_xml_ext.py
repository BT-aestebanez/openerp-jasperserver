# -*- coding: utf-8 -*-
##############################################################################
#
#   jasper_server module for OpenERP, Management module for Jasper Server
#   Copyright (C) 2011 SYLEAM (<http://www.syleam.fr/>)
#             Christophe CHAUVET <christophe.chauvet@syleam.fr>
#
#   This file is a part of jasper_server
#
#   jasper_server is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   jasper_server is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
from odoo import report

from odoo.addons.jasper_server.common.jasper import report_jasper

from logging import getLogger

_logger = getLogger(__name__)


class IrActionReportXmlExt(models.Model):
    _inherit = 'ir.actions.report.xml'

    report_type = fields.Selection(selection_add=[('jasper', 'Jasper')])

    @api.model_cr
    def _lookup_report(self, name):
        """
        Look up a report definition.
        """
        # First lookup in the deprecated place, because if the report definition
        # has not been updated, it is more likely the correct definition is there.
        # Only reports with custom parser specified in Python are still there.
        if 'report.' + name in report.interface.report_int._reports:
            new_report = report.interface.report_int._reports['report.' + name]
            if not isinstance(new_report, report_jasper):
                new_report = None
        else:
            cr = self._cr
            cr.execute("SELECT * FROM ir_act_report_xml WHERE report_name=%s and report_type=%s", (name, 'jasper'))
            r = cr.dictfetchone()
            if r:
                new_report = report_jasper('report.'+r['report_name'])
            else:
                new_report = None

        if new_report:
            return new_report
        else:
            return super(IrActionReportXmlExt, self)._lookup_report(name)
