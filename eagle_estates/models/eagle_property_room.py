from odoo import models, fields


class EaglePropertyRoom(models.Model):
    _name = 'eagle.property.room'
    _description = 'Eagle Property Room'

    type = fields.Selection([('bedroom', 'Bedroom'), ('bathroom', 'Bathroom'), ('dining', 'Dining Room'),
                             ('living', 'Living Room'), ('garage', 'Garage'), ('kitchen', 'Kitchen'),
                             ('other', 'Other')], default="other")
    surface = fields.Float('Surface')
    property_id = fields.Many2one('eagle.property')
