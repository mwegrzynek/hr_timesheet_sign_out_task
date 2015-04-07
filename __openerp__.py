# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2005-Today Litex Service Sp. z o.o. 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Allow to use project tasks in timesheet sign in/out forms',
    'version': '1.0.1',
    'category': 'Human Resources',
    'description': """

Allow to use project tasks in timesheet sign in/out forms
=========================================================

In standard Odoo installation you sign in / sign out to an analytic account.
This module changes that to allow signing in / out to project and tasks. It also creates
task work records automatically. 
    """,
    'author': 'Litex Service Sp. z o.o.',
    'website': 'http://www.litex.pl',
    'depends': [
        'hr_timesheet',
        'project_timesheet'
    ],
    'data': [
        'views/hr_so_project.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
    #'images': ['images/claim_categories.jpeg','images/claim_stages.jpeg','images/claims.jpeg'],
}
