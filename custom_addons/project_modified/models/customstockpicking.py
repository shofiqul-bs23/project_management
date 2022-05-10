from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        print("Hola")
        return super()._action_done()
