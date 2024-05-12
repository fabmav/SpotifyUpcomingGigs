#functions shared accross multiple librairies
import logging
import sqlite3

logger = logging.getLogger(__name__)

#DECORATORS
def write_to_file(file) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            with open(file,'a',encoding='UTF-8') as file_write : 
                for i in result : 
                    file_write.write(f'{i}\n')
        return wrapper
    return decorator


def json_write_to_file(file) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            try : 
                logger.info(f'''result json write to file  : {result[0:30]}\n
                            longueur fichier : {len(result)}''')
            except Exception as e : 
                logger.info(f'result : {result, len(result)}')
            with open(file,'a',encoding='UTF-8') as file_write : 
                    file_write.write(result)
        return wrapper
    return decorator


def write_to_db(db) : 
    def decorator(func) : 
        def wrapper(*args,**kwargs) : 
            result = func(*args,**kwargs)
            conn= sqlite3.connect(db)
            cursor = conn.cursor()
            # Define the SQL statement to insert data into the table
            insert_query = '''INSERT INTO evenements (
                    nom_evenement,
                    artiste,
                    date,
                    salle,
                    uri_artiste,
                    genre) VALUES (?,?,?,?,?,?);'''
            # Execute the SQL statement to insert multiple rows of data
            cursor.executemany(insert_query, result)
            # Commit the changes to the database
            conn.commit()
            # Close the cursor and the connection
            cursor.close()
            conn.close()
        return wrapper
    return decorator

if __name__ == "__main__" : 
    None