import pyodbc
from tabulate import tabulate

# Rank regions / states in the country by number of customers (use main office address),
# your report should include country, state or region, number of customers and
# percent rank ordered by country (alphabetically) and number of clients (descending).
# In case of equality in client numbers order region or states alphabetically.


query = '''SELECT ad.CountryRegion,
            ad.StateProvince,
            COUNT(ca.CustomerID) as Customers,
            PERCENT_RANK() OVER(PARTITION BY ad.CountryRegion ORDER BY COUNT(ca.CustomerID) DESC) As Percent_Rank
            FROM SalesLT.CustomerAddress ca
            JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            WHERE ca.AddressType = 'Main Office'
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
