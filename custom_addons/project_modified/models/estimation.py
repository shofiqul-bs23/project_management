from odoo import fields, models, api


class Estimation(models.Model):
    _name = 'estimation.line'
    _description = 'Simply an estimation line'

    product_id = fields.Many2one('product.product')
    quantity = fields.Integer(default=1)
    price = fields.Float(default=1)
    total_price = fields.Float(compute="cal_total_price")
    quantity_done = fields.Integer(compute="_compute_quantity_done", default=0)

    project_id = fields.Many2one('project.project')
    purchase_lines = fields.One2many('purchase.order.line', 'estimation_line')


    @api.depends('quantity','price')
    def cal_total_price(self):
        for rec in self:
            rec.total_price = rec.price * rec.quantity

    @api.depends('purchase_lines')
    def _compute_quantity_done(self):
        for rec in self:
            qty = 0
            for x in rec.purchase_lines:
                qty += x.qty_received
            rec.quantity_done = qty
