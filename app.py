from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Flask Calculator API is running!",
        "endpoints": {
            "POST /calculate": "Perform calculations with two numbers",
            "GET /": "Health check"
        }
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate sum, difference, product, and quotient of two numbers
    Expected JSON payload: {"num1": float, "num2": float}
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if 'num1' not in data or 'num2' not in data:
            return jsonify({"error": "Both 'num1' and 'num2' are required"}), 400
        
        # Extract numbers and convert to float
        try:
            num1 = float(data['num1'])
            num2 = float(data['num2'])
        except (ValueError, TypeError):
            return jsonify({"error": "Both numbers must be valid numeric values"}), 400
        
        # Perform calculations
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
    """
    Bonus endpoint: Calculate operations for multiple number pairs
    Expected JSON: {"pairs": [{"num1": float, "num2": float}, ...]}
    """
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
    # Run the app on port 8080 for containerization
    app.run(host='0.0.0.0', port=8080, debug=True)