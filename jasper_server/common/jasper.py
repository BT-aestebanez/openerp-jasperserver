# -*- coding: utf-8 -*-
##############################################################################
#
#    jasper_server module for OpenERP,
#    Copyright (C) 2009-2011 SYLEAM Info Services (<http://www.syleam.fr/>)
#                  Christophe CHAUVET <christophe.chauvet@syleam.fr>
#
#    This file is a part of jasper_server
#
#    jasper_server is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    jasper_server is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.api import Environment
from odoo.report.interface import report_int

from ..report.report_soap import Report
from ..report.report_exception import JasperException

import logging

_logger = logging.getLogger(__name__)


class report_jasper(report_int):
    """
    Extend report_int to use Jasper Server
    """

    def create(self, cr, uid, res_ids, data, context=None):

        env = Environment(cr, uid, context or {})
        if _logger.isEnabledFor(logging.DEBUG):
            _logger.debug('Call %s' % self.name)
        try:
            report = Report(self.name, env, res_ids, data)
            return report.execute()
        except JasperException as e:
            raise JasperException(e.name, e.value)

report_jasper('report.print.jasper.server')
