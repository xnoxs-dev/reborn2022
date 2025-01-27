from quart import Quart, request, jsonify
from reborn2022.recaptcha import solve_recaptcha
from logmagix import Logger
from typing import Optional
import sys

app = Quart(__name__)
logger = Logger()
@app.route('/solve', methods=['POST'])
async def solve_captcha():
    try:
        data = await request.get_json()
        if not data or 'url' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required parameters: url and sitekey"
            }), 400

        url: str = data['url']
        headless: bool = data.get('headless', True)
        token = solve_recaptcha(url, headless=headless)

        if "Error" in token:
            return jsonify({
                "success": False,
                "error": token
            }), 500

        return jsonify({
            "success": True,
            "token": token
        })

    except Exception as e:
        logger.failure(f"Server error: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

def start_api(host="0.0.0.0", port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)


