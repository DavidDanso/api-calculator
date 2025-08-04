from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def serve_index():
    """Serve the main web interface"""
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Flask Calculator API is running!",
        "endpoints": {
            "POST /calculate": "Perform calculations with two numbers",
            "POST /batch-calculate": "Batch calculations",
            "GET /health": "Health check",
            "GET /": "Web interface"
        }
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate sum, difference, product, and quotient of two numbers"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'num1' not in data or 'num2' not in data:
            return jsonify({"error": "Both 'num1' and 'num2' are required"}), 400
        
        try:
            num1 = float(data['num1'])
            num2 = float(data['num2'])
        except (ValueError, TypeError):
            return jsonify({"error": "Both numbers must be valid numeric values"}), 400
        
        results = {
            "input": {
                "num1": num1,
                "num2": num2
            },
            "results": {
                "sum": num1 + num2,
                "difference": num1 - num2,
                "product": num1 * num2,
                "quotient": num1 / num2 if num2 != 0 else "undefined (division by zero)"
            }
        }
        
        logger.info(f"Calculation performed: {num1} and {num2}")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error in calculation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/batch-calculate', methods=['POST'])
def batch_calculate():
    """Batch calculate operations for multiple number pairs"""
    try:
        data = request.get_json()
        
        if not data or 'pairs' not in data:
            return jsonify({"error": "JSON with 'pairs' array is required"}), 400
        
        pairs = data['pairs']
        if not isinstance(pairs, list):
            return jsonify({"error": "'pairs' must be an array"}), 400
        
        results = []
        for i, pair in enumerate(pairs):
            try:
                num1 = float(pair['num1'])
                num2 = float(pair['num2'])
                
                pair_result = {
                    "pair_index": i,
                    "input": {"num1": num1, "num2": num2},
                    "results": {
                        "sum": num1 + num2,
                        "difference": num1 - num2,
                        "product": num1 * num2,
                        "quotient": num1 / num2 if num2 != 0 else "undefined (division by zero)"
                    }
                }
                results.append(pair_result)
                
            except (KeyError, ValueError, TypeError):
                results.append({
                    "pair_index": i,
                    "error": f"Invalid data in pair {i}"
                })
        
        return jsonify({"batch_results": results})
        
    except Exception as e:
        logger.error(f"Error in batch calculation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)