from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Welcome to the Barbell Inventory API!"

def get_db_connection():
    connection = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='barbell_inventory'
    )
    return connection


@app.route('/api/barbell', methods=['GET'])
def get_barbells():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM inventory')
    barbells = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(barbells), 200


@app.route('/api/barbell', methods=['POST'])
def add_barbell():
    new_barbell = request.get_json()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO inventory (barbelltype, brand, msrp, weight, length, color)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (new_barbell['barbelltype'], new_barbell['brand'], new_barbell['msrp'],
          new_barbell['weight'], new_barbell['length'], new_barbell['color']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(new_barbell), 201


@app.route('/api/barbell', methods=['PUT'])
def update_msrp():
    data = request.get_json()
    barbell_id = data['id']
    new_msrp = data['msrp']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE inventory SET msrp = %s WHERE id = %s
    ''', (new_msrp, barbell_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "MSRP updated successfully"}), 200


@app.route('/api/barbell', methods=['DELETE'])
def delete_barbell():
    token = request.headers.get('Authorization')
    if token != '880088':
        return jsonify({"message": "Invalid token"}), 403

    barbell_id = request.get_json()['id']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = %s', (barbell_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Barbell deleted successfully"}), 200


@app.route('/api/inventoryvalue', methods=['GET'])
def get_inventory_value():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT msrp FROM inventory')
    barbells = cursor.fetchall()
    cursor.close()
    connection.close()

    quantity = len(barbells)
    total_value = sum(barbell['msrp'] for barbell in barbells)
    return jsonify({"quantity": quantity, "totalvalue": total_value}), 200

if __name__ == '__main__':
    app.run(debug=True)
