from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
@app.route('/giveTotal', methods=['POST'])
def process():
    try:  
        data = request.get_json()
        nameToFind = data.get('file')
        product = data.get('product')
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        os.chdir(parent_directory)
        os.chdir("krutik_PV_dir")
        file_path = os.path.join(os.getcwd(), nameToFind)
        doesFileExist = os.path.exists(file_path)
        if not doesFileExist:
            return jsonify({"file": nameToFind, "error": "File not found."})
    
        result = calculateTotal(file_path, product)
        if result == 0:
            return jsonify({"file": nameToFind, "error": "Input file not in CSV format."})
        return jsonify({"file": nameToFind, "sum": result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculateTotal(file_path, product):
    try:
        total_amount = 0
        with open(file_path, 'r') as file:
            next(file)
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    product_name = parts[0].strip()
                    amount = int(parts[1].strip())
                    if product_name == product:
                        total_amount += amount
        return total_amount
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)