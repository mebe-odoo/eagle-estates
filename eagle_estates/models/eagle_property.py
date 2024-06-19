from odoo import models, fields


class EagleProperty(models.Model):
    _name = "eagle.property"
    _description = "Eagle Property"
    _order = 'construction_date DESC, id'
    # There is no need to explicitly set _rec_name to name in this case,
    # as that is the default value.
    _rec_name = 'name'

    name = fields.Char(string="Property Name", required=True)
    construction_date = fields.Date("Construction Date", required=True, default=fields.Date.today)
    surface = fields.Float("Surface", default=0.0)

    tag_ids = fields.Many2many('eagle.tag', string="Tags")
    room_ids = fields.One2many('eagle.property.room', 'property_id', string="Rooms")
