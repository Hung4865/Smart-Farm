from odoo import http
from odoo.http import request
from datetime import datetime
import json
import requests as req_lib


class SmartFarmDashboard(http.Controller):

    @http.route('/smart_farm/dashboard', type='http', auth='user')
    def dashboard(self, **kwargs):
        env = request.env

        gps_records = env['smart.farm.gps'].search(
            [], limit=5, order='timestamp desc'
        )

        weather = None
        soil = None
        chart_data_json = "{}"
        try:
            r = req_lib.get(
                "https://api.open-meteo.com/v1/forecast"
                "?latitude=10.82&longitude=106.63"
                "&current_weather=true&past_days=1&hourly=temperature_2m,relative_humidity_2m,soil_temperature_0cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,shortwave_radiation",
                timeout=5,
            )
            if r.status_code == 200:
                data = r.json()
                cw = data['current_weather']
                hourly = data.get('hourly', {})
                
                current_hour = datetime.now().hour
                current_index = 24 + current_hour
                
                start_idx = current_index - 23
                end_idx = current_index + 1
                
                chart_times = hourly.get('time', [])[start_idx:end_idx]
                chart_temps = hourly.get('temperature_2m', [])[start_idx:end_idx]
                chart_hums = hourly.get('relative_humidity_2m', [])[start_idx:end_idx]
                
                chart_labels = [t.split('T')[1] for t in chart_times]
                chart_data_json = json.dumps({
                    'labels': chart_labels,
                    'temps': chart_temps,
                    'hums': chart_hums
                })
                
                humidity = hourly.get('relative_humidity_2m', [75]*48)[current_index]
                soil_temp = hourly.get('soil_temperature_0cm', [28]*48)[current_index]
                soil_m_a = hourly.get('soil_moisture_0_to_1cm', [0.72]*48)[current_index]
                soil_m_b = hourly.get('soil_moisture_1_to_3cm', [0.38]*48)[current_index]
                soil_m_c = hourly.get('soil_moisture_3_to_9cm', [0.81]*48)[current_index]
                radiation = hourly.get('shortwave_radiation', [70]*48)[current_index]
                
                moisture_a_pct = int(soil_m_a * 100) if soil_m_a is not None else 72
                moisture_b_pct = max(0, int(soil_m_b * 100) - 15) if soil_m_b is not None else 38
                moisture_c_pct = min(100, int(soil_m_c * 100) + 12) if soil_m_c is not None else 81
                lux = int(radiation * 120) if radiation is not None else 8400

                weather = {
                    'temperature': cw['temperature'],
                    'windspeed': cw['windspeed'],
                    'humidity': humidity,
                    'source': 'live',
                }
                soil = {
                    'temp': soil_temp,
                    'moisture_a': moisture_a_pct,
                    'moisture_b': moisture_b_pct,
                    'moisture_c': moisture_c_pct,
                    'lux': lux,
                    'source': 'live'
                }
        except Exception:
            pass

        if not weather:
            latest = env['smart.farm.weather'].search(
                [], limit=1, order='timestamp desc'
            )
            if latest:
                weather = {
                    'temperature': latest.temperature,
                    'windspeed': latest.windspeed,
                    'humidity': latest.humidity,
                    'source': 'db',
                }
            else:
                weather = {
                    'temperature': 31,
                    'windspeed': 12,
                    'humidity': 78,
                    'source': 'mock',
                }
            
            soil = {
                'temp': 28,
                'moisture_a': 72,
                'moisture_b': 38,
                'moisture_c': 81,
                'lux': 8400,
                'source': 'mock'
            }

        alerts = env['smart.farm.alert'].search(
            [], limit=6, order='timestamp desc'
        )
        unresolved_count = env['smart.farm.alert'].search_count(
            [('is_resolved', '=', False)]
        )

        values = {
            'gps_records': gps_records,
            'weather': weather,
            'soil': soil,
            'alerts': alerts,
            'unresolved_count': unresolved_count,
            'now': datetime.now(),
            'chart_data_json': chart_data_json,
        }

        return request.render('smart_farm.dashboard_main', values)

    @http.route('/smart_farm/api/gps', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def update_gps(self, **kwargs):
        """API endpoint để nhận dữ liệu GPS từ điện thoại (ví dụ: qua app GPSLogger)"""
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        name = kwargs.get('name', 'Điện thoại (App)')
        
        if not lat or not lon:
            return request.make_response('Missing lat or lon', status=400)
            
        try:
            # Dùng sudo() để cho phép public request (từ app ngoài) ghi vào database
            request.env['smart.farm.gps'].sudo().create({
                'name': name,
                'latitude': float(lat),
                'longitude': float(lon),
                'device_type': 'phone',
            })
            return request.make_response('OK', status=200)
        except Exception as e:
            return request.make_response(str(e), status=500)