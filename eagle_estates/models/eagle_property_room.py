from odoo import models, fields


class EaglePropertyRoom(models.Model):
    _name = 'eagle.property.room'
    _description = 'Eagle Property Room'

    type = fields.Selection([('bedroom', 'Bedroom'), ('bathroom', 'Bathroom'), ('dining', 'Dining Room'),
                             ('living', 'Living Room'), ('garage', 'Garage'), ('kitchen', 'Kitchen'),
                             ('other', 'Other')], default="other")
    surface = fields.Float('Surface')
    property_id = fields.Many2one('eagle.property')

    construction_date = fields.Date(related='property_id.construction_date')

    # Address fields
    street = fields.Char(related='property_id.street')
    street2 = fields.Char(related='property_id.street2')
    zip = fields.Char(related='property_id.zip')
    city = fields.Char(related='property_id.city')
    state_id = fields.Many2one(related='property_id.state_id')
    country_id = fields.Many2one(related='property_id.country_id')
