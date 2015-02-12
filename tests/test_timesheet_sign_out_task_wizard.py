# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from datetime import datetime, timedelta


from openerp import SUPERUSER_ID 
from openerp.tests import common
from openerp.tools import mute_logger
from openerp.exceptions import except_orm


class TestTimeSheetSignoutTask(common.TransactionCase):
    
    def setUp(self):
        super(TestTimeSheetSignoutTask, self).setUp()
        
    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.osv.orm')     
    def test_signout_task(self):
        now = datetime.now()
        five_min_before = now - timedelta(minutes=5)
        
        sip = self.env['hr.sign.in.project'].create(dict(date=five_min_before))
        
        res = sip.check_state()
        self.assertEqual(res['views'][0][0], self.env.ref('hr_timesheet.view_hr_timesheet_sign_in').id)
        
        sip.sign_in_result()
        
        # Can not sign in twice in a row
        self.assertRaises(except_orm, sip.sign_in_result)
       
        task_22 = self.env.ref('project.project_task_22')
        sop = self.env['hr.sign.out.project'].create(dict(
            project_id=self.env.ref('project.project_project_5').id,
            task_id=task_22.id,
            info='Test sign out for task Customer analysis...',
            date=now
        ))
        sop.sign_out_result_end()
        
        last_wk_id = task_22.work_ids[-1]
        self.assertEqual(last_wk_id.name, u'Test sign out for task Customer analysis...')
        self.assertAlmostEqual(last_wk_id.hours, 5.0 / 60)
        
    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.osv.orm')     
    def test_signout_project(self):
        now = datetime.now()
        five_min_before = now - timedelta(minutes=5)
        
        sip = self.env['hr.sign.in.project'].create(dict(date=five_min_before))
        
        res = sip.check_state()
        self.assertEqual(res['views'][0][0], self.env.ref('hr_timesheet.view_hr_timesheet_sign_in').id)
        
        sip.sign_in_result()
        
        # Can not sign in twice in a row
        self.assertRaises(except_orm, sip.sign_in_result)
        sop = self.env['hr.sign.out.project'].create(dict(
            project_id=self.env.ref('project.project_project_5').id,
            info='Test sign out for project Data import',
            date=now
        ))
        sop.sign_out_result_end()
        
        self.env.cr.commit()
        
        
        
        
    