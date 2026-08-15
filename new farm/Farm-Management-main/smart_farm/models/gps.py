from odoo import models, fields, api


class SmartFarmGPS(models.Model):
    _name = 'smart.farm.gps'
    _description = 'Vị trí GPS'
    _order = 'timestamp desc'

    name = fields.Char(
        string='Thiết bị / Người dùng',
        required=True,
    )
    latitude = fields.Float(
        string='Vĩ độ',
        digits=(10, 6),
        required=True,
    )
    longitude = fields.Float(
        string='Kinh độ',
        digits=(10, 6),
        required=True,
    )
    timestamp = fields.Datetime(
        string='Thời gian ghi nhận',
        default=fields.Datetime.now,
        required=True,
    )
    device_type = fields.Selection([
        ('phone', 'Điện thoại'),
        ('tractor', 'Máy kéo'),
        ('sensor', 'Cảm biến'),
        ('other', 'Khác'),
    ], string='Loại thiết bị', default='phone')
    notes = fields.Text(string='Ghi chú')

    @api.model
    def log_gps(self, name, latitude, longitude, device_type='phone', notes=''):
        """Tạo bản ghi GPS mới."""
        return self.create({
            'name': name,
            'latitude': latitude,
            'longitude': longitude,
            'device_type': device_type,
            'notes': notes,
        })