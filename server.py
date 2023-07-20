import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify

# חיבור לבסיס הנתונים
def connect():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='acms_db',
            user='root',
            password='',
            port=3306
        )

        if connection.is_connected():
            print('Connected to MySQL database')
            return connection

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")

    return connection

# שאילתה לחיפוש הערך בטבלה והחזרת הסטטוס, הכותרת והתיאור
def search_status(number):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"""
            SELECT c.ref_code, c.id, t.title, t.description
            FROM cargo_list c
            JOIN tracking_list t ON c.id = t.cargo_id
            WHERE c.ref_code = '{number}'
            ORDER BY t.title, t.description DESC
            LIMIT 0, 25
            """
            cursor.execute(query)
            status = cursor.fetchone()
            if status:
                return {
                    'ref_code': status[0],
                    'id': status[1],
                    'title': status[2],
                    'description': status[3]
                }
            else:
                print('Status not found')
                return {'error': 'Status not found'}

        except Error as e:
            print(f"Error searching for status: {e}")

        finally:
            cursor.close()
            connection.close()
            print('MySQL connection closed')

    else:
        print('Failed to connect to MySQL database')
        return {'error': 'Failed to connect to MySQL database'}


# שרת Flask
app = Flask(__name__)

# מסלול לקבלת המספר והחזרת הסטטוס, הכותרת והתיאור
@app.route('/get_status', methods=['GET'])
def get_status():
    number = request.args.get('number')
    if number:
        status = search_status(number)
        return jsonify({'status': status})  # שינוי כאן
    else:
        return jsonify({'error': 'Number parameter missing'})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
