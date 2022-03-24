import pyodbc
from tabulate import tabulate

# Include in previous report customers without information about address.
# Use dense rank instead of percent rank in that report.


query = '''SELECT ad.CountryRegion,
            ad.StateProvince,
            COUNT(cs.CustomerID) as Customers,
            DENSE_RANK() OVER(PARTITION BY ad.CountryRegion ORDER BY COUNT(ca.CustomerID) DESC) As Rank
            FROM SalesLT.Customer cs
            LEFT JOIN SalesLT.CustomerAddress ca ON cs.CustomerID = ca.CustomerID
            LEFT JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            WHERE (ca.AddressType is NULL OR ca.AddressType = 'Main Office')
            GROUP BY ad.CountryRegion, ad.StateProvince
            ORDER BY 1, 3 DESC'''


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
