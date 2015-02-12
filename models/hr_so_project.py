# -*- coding: UTF-8 -*-
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
from datetime import datetime


from openerp import fields, api, _
from openerp.models import Model
from openerp.exceptions import except_orm


class HrSOProject(Model):
    _name = 'hr.sign.out.project'
    _inherit = 'hr.sign.out.project'
    _description = 'Sign Out By Project / Task'
    
    date_start = fields.Datetime('Starting Date', readonly=True)
    project_id = fields.Many2one('project.project', 'Project', domain=[('analytic_account_id', '=', True)], ondelete='cascade')
    account_id = fields.Many2one('account.analytic.account', 'Analytic account', related='project_id.analytic_account_id', store=True, ondelete='cascade')
    task_id = fields.Many2one('project.task', 'Task', domain=[('project_id', '=', project_id)], ondelete='cascade')
    
    @api.model
    def _write(self, *args, **kwargs):
        pass # Everything moved to sign_out
    
    @api.multi
    def sign_out(self, action):
        timesheet_obj = self.pool.get('hr.analytic.timesheet') 
        work_obj = self.env['project.task.work']
        
        for so in self:
            so.with_context(dict(action=action, action_date=so.date)).emp_id.attendance_action_change()
            
            delta = ((fields.Datetime.from_string(so.date) if so.date else datetime.now()) - fields.Datetime.from_string(so.date_start))
            
            hour = delta.days * 24 + delta.seconds / 3600.0
            if so.analytic_amount:
                hour = round(round((hour + so.analytic_amount / 2) / so.analytic_amount) * so.analytic_amount, 2)
            
            # Default route -- no task selected
            if not so.task_id:
                print "No task, hours: ", hour
                res = timesheet_obj.default_get(self.env.cr, self.env.uid, ['product_id','product_uom_id'])
        
                if not res['product_uom_id']:
                    raise except_orm(_('User Error!'), _('Please define cost unit for this employee.'))
                
                up = timesheet_obj.on_change_unit_amount(self.env.cr, self.env.uid, False, res['product_id'], hour, False, res['product_uom_id'])['value']
        
                res['name'] = so.info
                res['account_id'] = so.project_id.analytic_account_id.id
                res['unit_amount'] = hour
                emp_journal = so.emp_id.journal_id
                res['journal_id'] = emp_journal and emp_journal.id or False
                res.update(up)
                
                up = timesheet_obj.on_change_account_id(self.env.cr, self.env.uid, False, res['account_id']).get('value', {})
                res.update(up)
                
                timesheet_obj.create(self.env.cr, self.env.uid, res)    
            else:
                # Task selected
                work_data = dict(
                    name=so.info,
                    date=so.date,
                    task_id=so.task_id.id,
                    hours=hour,
                    user_id=self._uid
                )
                work_obj.create(work_data)
            
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def sign_out_result(self):
        return self.sign_out('action')
    
    @api.multi
    def sign_out_result_end(self):
        return self.sign_out('sign_out')
    