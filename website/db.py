# db.py
import mysql.connector

# Global database connection
def get_db_connection():
    connection = mysql.connector.connect(
    host="localhost", #localhost kapag local lang, kapag shared na yung ipv4 add
    port=3306,
    user="root", #root for local host, remote_user for shared
    password="", #"" for local host, for shared DelaPenaJohnBenedict
    database="library_software" # Replace with your database name
    )
    return connection