"""Deliverable1"""
import hashlib
import jwt
import pymysql
import boto3
import json

USEFUL_KEY = 'my2w7wjd7yXF64FIADfJxNs1oupTGAuW'
secret_name = "lambda/rds/connect"
region_name = "us-west-2"


class Token:
    """Login process"""
    @staticmethod
    def db_connection(username):
        """Connects to db and performs query"""
        # session = boto3.session.Session()
        # client = session.client(
        #     service_name='secretsmanager',
        #     region_name=region_name
        # )
        # response = client.get_secret_value(
        #     SecretId=secret_name
        # )
        # secret_value = json.loads(response['SecretString'])
        # data_base = pymysql.connect(
        #     host=secret_value["host"],
        #     user=secret_value["username"],
        #     passwd=secret_value["password"],
        #     database=secret_value["dbname"]
        # )
        data_base = pymysql.connect(
            host="database-1.cvc1c3ipqztj.us-east-2.rds.amazonaws.com",
            user="admin",
            passwd="N0semeolvida987",
            database="bootcamp_tht"
        )  

        cursor = data_base.cursor()
        cursor.execute("SELECT salt, password, role from users where username = %s;", (username, ))
        query = cursor.fetchone()
        cursor.close()
        return query

    def generate_token(self, username, input_password):
        """Validates credentials and generates token"""
        query = self.db_connection(username)
        if query is not None:
            salt = query[0]
            password = query[1]
            role = query[2]
            hash_pass = hashlib.sha512((input_password + salt).encode()).hexdigest()
            if hash_pass == password:
                token = jwt.encode({"role": role}, USEFUL_KEY, algorithm='HS256')
                return token
        return False


class Restricted:
    """Validates token"""
    @staticmethod
    def access_data(header):
        """Validates token"""
        header.strip()
        if len(header.split(" ")) == 2:
            input_token = header.split(" ")[1]
            try:
                jwt.decode(input_token, USEFUL_KEY, algorithms='HS256')
                return True
            except jwt.InvalidTokenError:
                return False
        return False
