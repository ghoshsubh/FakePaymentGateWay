from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import main
from sql_connections import get_sql_connections
from collections import OrderedDict
from flask import jsonify
from collections import OrderedDict
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
CORS(app)
connections = get_sql_connections()


# Serve the index.html file
@app.route('/PaymentForm')
def home():
    return render_template('index.html')

@app.route('/GetTransactions', methods=['GET'])
def get_transactions():
    connections = get_sql_connections()
    transactions = main.get_all_transactions(connections)
    return jsonify(transactions)

@app.route('/AddTransactions', methods=['POST'])
def add_transaction():
    connections = get_sql_connections()
    transaction = request.json
    payment_id = main.insert_new_transaction(connections, transaction)
    return jsonify({'payment_id': payment_id}), 201

@app.route('/transactions/<int:payment_id>', methods=['DELETE'])
def remove_transaction(payment_id):
    connections = get_sql_connections()
    main.delete_transaction(connections, payment_id)
    return jsonify({'message': 'Transaction deleted successfully'}), 204


@app.route('/transaction/<int:payment_id>', methods=['GET'])
def transaction_detail_front_end(payment_id):
    connections = get_sql_connections()  # Replace with your actual connection handling
    transaction = main.get_transaction_by_id(connections, payment_id)
    if transaction:
        return render_template('transaction_detail.html', transaction=transaction)
    else:
        return jsonify({'error': 'Transaction not found'}), 404





@app.route('/transaction_id/<int:payment_id>', methods=['GET'])
def transaction_detail(payment_id):
    connections = get_sql_connections()  # Replace with your actual connection handling
    transaction = main.get_transaction_by_id(connections, payment_id)
    
    if transaction:
        # Prepare the response data with appropriate formatting
        response_data = OrderedDict([
            ('Massage', 'Transaction Successful'),
            ('Payment Id', transaction['payment_id']),
            ('Name', transaction['card_holder_name']),
            ('Amount', transaction['amount']),
            ('Date of Transaction', transaction['date'].isoformat() if isinstance(transaction['date'], datetime) else transaction['date']),
            ('Time of Transaction', transaction['time'].isoformat() if isinstance(transaction['time'], datetime) else transaction['time'])
        ])
        
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Transaction not found'}), 404

    

if __name__ == '__main__':
    app.run(debug=True)