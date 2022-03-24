import pyodbc
from tabulate import tabulate

# Rank cities in the country by number of customers (use main office address),
# your report should include country, state or region, city,  number of clients,
# rank (use plane rank here) and difference in number of client with previous position in by country ranking
# (for first position should be null). Order your report by country name (alphabetically),
# number of clients (descending) and city name (alphabetically).


query = '''SELECT
            RANK() OVER(PARTITION BY ad.CountryRegion ORDER BY COUNT(ca.CustomerID) DESC) AS Rank,
            ad.CountryRegion,
            ad.StateProvince,
            ad.City,
            COUNT(ca.CustomerID) as Customers,
            (COUNT(ca.CustomerID) - LAG(COUNT(ca.CustomerID)) 
            OVER(PARTITION BY ad.CountryRegion ORDER BY COUNT(ca.CustomerID) DESC, ad.City)) AS Diff
            FROM SalesLT.Customer cs
            LEFT JOIN SalesLT.CustomerAddress ca ON cs.CustomerID = ca.CustomerID
            LEFT JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            WHERE ca.AddressType = 'Main Office'
            GROUP BY ad.CountryRegion, ad.StateProvince, ad.City
            ORDER BY 2, 5 DESC, 4'''


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
