import psycopg2

# Function to connect Flask app to the postgres database
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user="sammy",
                            password="pttinternship2022",
                            port=5432  
    )
    return conn

# Function to create user table
def create_client_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client(
                client_id serial, 
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50),
                PRIMARY KEY (client_id)
            );''')  
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("create client table ERROR : " , str(e))
        return "create client table ERROR : " + str(e)
    else:
        print("Client Table created successfully.")
        return "Client Table created successfully."


# Initialize table with one client
def init_client_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO client (name, email, password)
            VALUES ('Talay Kondhorn', 'talaykd@gmail.com', 'helloworld')
            ''') 
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("initialized client table ERROR : " , str(e))
        return "initialized client table ERROR " + str(e)
    else:
        print("Initialized client table successfully.")
        return "Initialized client table successfully."


# Create education table
def create_education_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS education(
                    education_id serial, 
                    degree VARCHAR(25) NOT NULL,
                    credits integer NOT NULL,
                    duration integer NOT NULL,
                    earnings integer NOT NULL,
                    PRIMARY KEY (education_id)
            );''') 
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("create education table ERROR : " , str(e))
        return "create education table ERROR " + str(e)
    else:
        print("Education Table created successfully.")
        return "Education Table created successfully."


# Create student table
def create_student_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS student(
                    student_id serial, 
                    name VARCHAR(25) NOT NULL,
                    nationality VARCHAR(25) NOT NULL,
                    age integer NOT NULL,
                    gender VARCHAR(25) NOT NULL,
                    grade integer NOT NULL,
                    education_id integer,
                    PRIMARY KEY (student_id),
                    FOREIGN KEY (education_id) REFERENCES education(education_id)
            );''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("create student table ERROR : " , str(e))
        return "create student table ERROR : " + str(e)
    else:
        print("Student Table created successfully.")
        return "Student Table created successfully."

# Initialize values for education table
# Average earnings data from https://www.northeastern.edu/bachelors-completion/wp-content/uploads/2020/06/Annual_Earnings_Unemp_Rates_R2-1.png
def init_education_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO education (degree, credits, duration, earnings)
            VALUES ('High-School', 26, 4, 38792)
            ''') 
        cur.execute('''
            INSERT INTO education (degree, credits, duration, earnings)
            VALUES ('Bachelors', 120, 4, 64896)
            ''') 
        cur.execute('''
            INSERT INTO education (degree, credits, duration, earnings)
            VALUES ('Masters', 30, 2, 77844)
            ''') 
        cur.execute('''
            INSERT INTO education (degree, credits, duration, earnings)
            VALUES ('Doctorate', 90, 6, 97916)
            ''') 
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("initialized education table ERROR : " , str(e))
        return "initialized education table ERROR : " + str(e)
    else:
        print("Initialized education table successfully.")
        return "Initialized education table successfully."


### Table Actions ###

# table is a string of table name
def get_table(table):
    order = "SELECT * from " + str(table) + " ORDER BY " + str(table) + "_id ASC"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# field is a string of field name
def get_table_col(table, field):
    order = "SELECT " + str(field) + " FROM " + str(table)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_table_row(table, col, value):
    order = "SELECT * from " + str(table) + " WHERE " + str(col) + "="
    if (isinstance(value, str)):
        order = order + "\'" + str(value) + "\'"
    else:
        order = order + str(value)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
    

# table is a string of table name
# fields is an array of columns to be inserted into
# values is an array of the corresponding values in each column
def insert_row(table, fields, values):
    order = "INSERT INTO " + str(table) + "("
    for field in fields:
        order = order + str(field) + ','
    order = order[:-1] + ") VALUES("
    for value in values:
        if (isinstance(value, str)):
            order = order + "\'" + str(value) + "\'"
        else:
            order = order + str(value)
        order = order + ","
    order = order[:-1] + ")"
    # Connect to database and execute
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    conn.commit()
    cur.close()
    conn.close()

# data is a dictionary that stores column : value pairs
# update only at row with val if the arguments are given
def update_table(table, data, col=None, row=None):
    order = "UPDATE " + str(table) + " SET"
    for d in data:
        #check if type is string
        if (isinstance(data[d], str)):
            order = order + " " + str(d) + " = " + "\'" + str(data[d]) + "\'"
        else:
            order = order + " " + str(d) + " = " + str(data[d])
        order = order + ","
    order = order[:-1]
    if (col != None):
        if (isinstance(row, str)):
            order = order + " WHERE " + str(col) + "=" + "\'" + str(row) + "\'"
        else:
            order = order + " WHERE " + str(col) + "=" + str(row)
    #connect to database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    conn.commit()
    cur.close()
    conn.close()

# delete only at col with row (value in col) only if arguments are given
# otherwise, delete all rows in the table
def delete_row(table, col=None, row=None):
    order = "DELETE  FROM " + str(table)
    if (col != None):
        if (isinstance(row, str)):
            order = order + " WHERE " + str(col) + "=" + "\'" + str(row) + "\'"
        else:
            order = order + " WHERE " + str(col) + "=" + str(row) 
    #Delete data from database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(order)
    conn.commit()
    cur.close()
    conn.close()
