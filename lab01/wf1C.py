import pyodbc
from tabulate import tabulate

# Create reports about ranking for sales persons:
# Rank your sales persons by number of clients, 
# report should include rank, sales person id and client number in descending order.


query = '''SELECT cs.SalesPerson,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum,
            RANK() OVER(ORDER BY 
                COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) DESC)
                AS Rank
            FROM SalesLT.Customer cs
            LEFT JOIN SalesLT.SalesOrderHeader soh ON soh.CustomerID = cs.CustomerID
            LEFT JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
            GROUP BY cs.SalesPerson
            ORDER BY 3'''


def get_data(query: str):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=myfirstsqlserv.database.windows.net;DATABASE=myFirstDatabase;'
        'UID=your_login;PWD=your_password')
    cursor = connection.cursor()
    rows = cursor.execute(query)
    head = [tpl[0] for tpl in rows.description]
    rows = cursor.fetchall()
    connection.close()
    return tabulate(rows, headers=head, tablefmt="grid"), len(rows)


if __name__ == '__main__':
    result, amount = get_data(query)
    print(result)
    print(f'Rows fetched: {amount}')