from odoo import fields, models, api



class RequisitionLine(models.Model):
    _name = 'requisition.line'
    _description = 'Requisition Line'

    product_id = fields.Many2one('product.product')
    name = fields.Char()
    quantity = fields.Integer(default=0)
    price_unit = fields.Float(default=0)
    total_price = fields.Float(compute="cal_total_price")
    quantity_done = fields.Integer(compute="_compute_quantity_done", default=0)
    # quantity_done = fields.Integer(default=0)

    requisition = fields.Many2one('requisition')
    #backed
    estimation_line_id = fields.Many2one('estimation.line')
    purchase_order_line_ids = fields.Many2one('purchase.order.line','requisition_line_id')

    purchase_lines = fields.One2many('purchase.order.line', 'estimation_line')

    @api.depends('quantity', 'price_unit')
    def cal_total_price(self):
        for rec in self:
            rec.total_price = rec.price_unit * rec.quantity


    @api.depends('purchase_order_line_ids')
    def _compute_quantity_done(self):
        for rec in self:
            qty = 0
            for x in rec.purchase_order_line_ids:
                qty += x.qty_received
            rec.quantity_done = qty





class Requisition(models.Model):
    _name = 'requisition'
    _description = 'Requisition'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')],
        required=True, default='draft'
    )

    project_id = fields.Many2one('project.project')

    requisition_line_ids = fields.One2many('requisition.line','requisition')

    def requisitions(self):
        data = [(0, 0, {"product_id": line.product_id.id, "name": line.product_id.name,
                        "product_qty": (line.quantity - line.quantity_done), "price_unit": line.price_unit,
                        'product_uom': line.product_id.uom_id.id, 'requisition_line_id': line.id})
                for line in self.requisition_line_ids
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
            'context': {'default_project_id': self.project_id.id,
                        'default_order_line': data,
                        }
        }



