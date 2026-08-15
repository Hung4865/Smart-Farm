from odoo import models, fields


class SmartFarmAlert(models.Model):
    _name = 'smart.farm.alert'
    _description = 'Cảnh báo trang trại'
    _order = 'timestamp desc'

    name = fields.Char(string='Tiêu đề', required=True)
    content = fields.Text(string='Nội dung')
    alert_type = fields.Selection([
        ('danger', '🔴 Nguy hiểm'),
        ('warning', '🟡 Cảnh báo'),
        ('info', '🔵 Thông tin'),
        ('success', '🟢 Thành công'),
    ], string='Mức độ', default='info', required=True)
    area = fields.Char(string='Khu vực')
    timestamp = fields.Datetime(
        string='Thời gian',
        default=fields.Datetime.now,
        required=True,
    )
    is_resolved = fields.Boolean(string='Đã xử lý', default=False)

    def action_resolve(self):
        """Đánh dấu cảnh báo đã xử lý."""
        self.is_resolved = True