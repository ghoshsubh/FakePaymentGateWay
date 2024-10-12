from __future__ import print_function
from sql_connections import get_sql_connections
from datetime import datetime

def get_all_transactions(connections):
    with connections.cursor() as cursor:
        query = (
            "SELECT payment_info.payment_id, payment_info.card_number, payment_info.cvv, payment_info.card_holder_name, payment_info.expire_date, payment_info.amount, payment_info.date, payment_info.time "
            "FROM payment_info "
        )
        cursor.execute(query)

        response = []
        for (payment_id, card_number, cvv, card_holder_name, expire_date, amount, date, time) in cursor:
            response.append({
                'payment_id': payment_id,
                'card_number': card_number,
                'cvv': cvv,
                'card_holder_name': card_holder_name,
                'expire_date': expire_date,
                'amount': amount, 
                'date': date,
                'time': time
            })
    return response

def get_transaction_by_id(connections, payment_id):
    with connections.cursor() as cursor:
        query = "SELECT payment_id, card_number, cvv, card_holder_name, expire_date, amount, date, time FROM payment_info WHERE payment_id = %s"
        cursor.execute(query, (payment_id,))
        result = cursor.fetchone()
        if result:
            return {
                'payment_id': result[0],
                'card_number': result[1],
                'cvv': result[2],
                'card_holder_name': result[3],
                'expire_date': result[4],
                'amount': result[5],
                'date': result[6],
                'time': result[7]
            }
        else:
            return None
        
def insert_new_transaction(connections, transaction):
    with connections.cursor() as cursor:
        query = (
            "INSERT INTO payment_info (card_number, cvv, card_holder_name, expire_date, amount, date, time) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        data = (transaction['card_number'], transaction['cvv'], transaction['card_holder_name'], transaction['expire_date'], transaction['amount'], transaction['date'], transaction['time'])
        cursor.execute(query, data)
        connections.commit()
        return cursor.lastrowid

def delete_transaction(connections, payment_id):
    with connections.cursor() as cursor:
        query = "DELETE FROM payment_info WHERE payment_id = %s"
        cursor.execute(query, (payment_id,))
        connections.commit()

if __name__ == '__main__':


    # Function to get SQL connections (assuming it's defined elsewhere)
    connections = get_sql_connections()

    # Get the current date and time
    current_date = datetime.now().date()  # Get current date
    current_time = datetime.now().time()  # Get current time

    # Prepare the data dictionary
    data1 = {
        'card_number': '1234567890123456',
        'cvv': '123',
        'card_holder_name': 'John Doe',
        'expire_date': '2028-01-01',
        'amount': 500, 
        'date': current_date,  # Current date
        'time': current_time   # Current time
        }

    # Now you can use data1 to insert into your database


    # Uncomment to insert a new transaction
    # insert_new_transaction(connections, data1)

    # Example to delete a transaction
    insert_new_transaction(connections, data1)
    print("Transaction added successfully.")



