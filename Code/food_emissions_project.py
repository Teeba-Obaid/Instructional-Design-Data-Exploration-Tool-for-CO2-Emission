from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update-data', methods=['POST'])
def update_data():
    data = request.get_json()  # Get the data from the request

    # Iterate over each row and update calculations
    for row in data:
        try:
            # Convert fields to floats to perform arithmetic operations
            current = float(row['current'])
            future = float(row['future'])
            rate = float(row['rate'])

            # Calculate yearly usage for current and future consumption
            row['currentuse'] = current * rate * 365
            row['futureuse'] = future * rate * 365

            # Calculate CO₂ saved per year and convert to pounds
            row['co2saved'] = row['currentuse'] - row['futureuse']
            row['poundco2saved'] = row['co2saved'] * 2.20462  # Convert kg to pounds
        except ValueError:
            # Handle conversion error
            row['co2saved'] = 0
            row['poundco2saved'] = 0

    response = {
        'updatedData': data
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Ensure this port is different from those already in use
