import psycopg2
from flask import Flask, request, jsonify
from engine import create_rule, combine_rules, evaluate_rule  # type: ignore
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    try:
        # Fetching the connection string from the environment variables
        db_url = os.getenv('DATABASE_URL')
        if db_url is None:
            raise ValueError("DATABASE_URL is not set in the environment variables.")

        # Attempting to establish a connection
        conn = psycopg2.connect(db_url)
        print("Database connection successful!")
        return conn
    except psycopg2.OperationalError as e:
        print("OperationalError: Could not connect to the database. Details:", e)
        return None
    except ValueError as e:
        print("ValueError:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred while connecting to the database:", e)
        return None


@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    try:
        rule_string = request.json.get('rule_string')
        if not rule_string:
            return jsonify({"error": "No rule string provided"}), 400

        rule_ast = create_rule(rule_string)

        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_name, rule_ast) VALUES (%s, %s) RETURNING id", 
                       (rule_string, str(rule_ast)))
        rule_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"rule_id": rule_id, "rule_ast": str(rule_ast)})
    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "Welcome to the Rule Engine API!"

# Other routes ...
if __name__ == '__main__':
    app.run(debug=True)
