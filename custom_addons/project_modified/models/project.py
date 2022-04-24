from odoo import fields, models, api


class Project(models.Model):
    # _name = 'project.modified'
    _inherit = 'project.project'
    _description = 'This will modify the project'

    test = fields.Char()
    rfq_ids = fields.One2many('purchase.order', 'project_id', help="Holds the RFQs ")

    def requisitions(self):
        print("Hello World")
        return {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref("purchase.purchase_order_form").id,
            'context': {'default_project_id': self.id}
        }

    def open_tree_view(self, context=None):
        # field_ids = self.env['project.project'].search([('department_id', '=', context['department_id'])]).ids

        # domain = [('id', 'in', field_ids)]

        view_id_tree = self.env['ir.ui.view'].search([('name', '=', "model.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            # 'view_id ref="module_name.tree_view"': '',
            'view_id': self.env.ref("purchase.purchase_order_kpis_tree").id,
            'target': 'current',
            # 'domain': domain,
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

    # return {
    #     'name': _('Create invoice/bill'),
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',
    #     'res_model': 'account.move',
    #     'view_id': self.env.ref('account.view_move_form').id,
    #     'context': ctx,
    # }
