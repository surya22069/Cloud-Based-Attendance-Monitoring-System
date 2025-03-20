import pyodbc

def get_conn():

    connection_string = (
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=tcp:attendancemonitoring.database.windows.net,1433;'
        'Database=attendancemonitoring;'
        'Uid=cloudpro;'
        'Pwd=Goli@123;'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30'
    )
    return pyodbc.connect(connection_string)
