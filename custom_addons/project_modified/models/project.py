from odoo import fields, models, api


class Project(models.Model):
    # _name = 'project.modified'
    _inherit = 'project.project'
    _description = 'Custom Project'

    test = fields.Char()
    rfq_ids = fields.One2many('purchase.order', 'project_id', help="Holds the RFQs ")
    rfc_count = fields.Integer(default=0, compute='_count_rfc')

    estimation_line_ids = fields.One2many('estimation.line', 'project_id')
    total_estimated_cost = fields.Float(compute='cal_total_estimated_cost')

    location = fields.Many2one('stock.location')

    def requisitions(self):
        data = [(0, 0, {"product_id": line.product_id.id, "name": line.product_id.name,
                        "product_qty": (line.quantity - line.quantity_done), "price_unit": line.price,
                        'product_uom': line.product_id.uom_id.id, 'estimation_line': line.id})
                for line in self.estimation_line_ids
                ]
        for x in data:
            if x[2]['product_qty'] == 0:
                data.remove(x)

        return {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref("purchase.purchase_order_form").id,
            # 'res_id': new_purchase_order.id,
            'context': {'default_project_id': self.id,
                        'default_order_line': data,
                        }
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
        self.rfc_count = len(self.rfq_ids.ids)

    def cal_total_estimated_cost(self):
        for rec in self:
            temp = 0
            for x in rec.estimation_line_ids:
                temp += x.total_price
            rec.total_estimated_cost = temp
