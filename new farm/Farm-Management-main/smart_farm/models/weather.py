from odoo import models, fields, api
import requests


class SmartFarmWeather(models.Model):
    _name = 'smart.farm.weather'
    _description = 'Dữ liệu thời tiết'
    _order = 'timestamp desc'

    name = fields.Char(
        string='Bản ghi',
        required=True,
        default='Cập nhật thời tiết',
    )
    temperature = fields.Float(string='Nhiệt độ (°C)')
    windspeed = fields.Float(string='Tốc độ gió (km/h)')
    humidity = fields.Float(string='Độ ẩm (%)')
    timestamp = fields.Datetime(
        string='Thời gian',
        default=fields.Datetime.now,
        required=True,
    )
    location = fields.Char(
        string='Vị trí',
        default='TP. Hồ Chí Minh',
    )
    latitude = fields.Float(string='Vĩ độ', default=10.82)
    longitude = fields.Float(string='Kinh độ', default=106.63)

    @api.model
    def fetch_and_save(self):
        """Gọi API Open-Meteo và lưu vào database."""
        lat = 10.82
        lon = 106.63
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
            f"&hourly=relative_humidity_2m"
        )
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                cw = data['current_weather']
                humidity = data.get('hourly', {}).get('relative_humidity_2m', [0])[0]
                return self.create({
                    'name': f"Thời tiết {fields.Datetime.now()}",
                    'temperature': cw['temperature'],
                    'windspeed': cw['windspeed'],
                    'humidity': humidity,
                    'latitude': lat,
                    'longitude': lon,
                })
        except Exception:
            pass
        return False