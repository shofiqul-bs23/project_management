from odoo import fields, models, api


class Project(models.Model):
    # _name = 'project.modified'
    _inherit = 'project.project'
    _description = 'This will modify the project'

    test = fields.Char()
    rfq_ids = fields.One2many('purchase.order', 'project_id', help="Holds the RFQs ")
    rfc_count = fields.Integer(default=0, compute = '_count_rfc')

    estimation_line_ids = fields.One2many('estimation.line', 'project_id')



    def requisitions(self):
        print("Hello World")
        return {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref("purchase.purchase_order_form").id,
            'context': {'default_project_id': self.id}
        }

    def show_rfqs(self):
        self.ensure_one()

        return {
            'name': "RFQ form",
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('project_id', '=', self.id)]
            # 'view_id': self.env.ref('purchase.purchase_order_kpis_tree').id
        }

    @api.depends('rfq_ids')
    def _count_rfc(self):
        self.rfc_count= len(self.rfq_ids.ids)

    # return {
    #     'name': _('Create invoice/bill'),
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',
    #     'res_model': 'account.move',
    #     'view_id': self.env.ref('account.view_move_form').id,
    #     'context': ctx,
    # }
