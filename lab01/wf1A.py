import pyodbc
from tabulate import tabulate

# Rank your sales persons by number of sales, your report should 
# include all sales persons with id, dense rank and number of sales
# in descending order.


# Can also use simple rank here
query = '''SELECT cs.SalesPerson,
            COUNT(cs.CustomerID) as Clients,
            DENSE_RANK() OVER(ORDER BY COUNT(cs.CustomerID) DESC) As DenseRank
            FROM SalesLT.Customer cs
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
