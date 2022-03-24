import pyodbc
from tabulate import tabulate

# Create integral report on number of product sales
# by product, client, sales person and hierarchy of regions.

query = '''SELECT pr.ProductID,
            cs.CustomerID,
            cs.SalesPerson,
            ad.PostalCode, 
            ad.City, 
            ad.StateProvince,
            ad.CountryRegion,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum
            FROM SalesLT.Product pr
            LEFT JOIN SalesLT.SalesOrderDetail sod ON sod.ProductID = pr.ProductID
            JOIN  SalesLT.SalesOrderHeader soh ON soh.SalesOrderID = sod.SalesOrderID
            JOIN SalesLT.Customer cs ON soh.CustomerID = cs.CustomerID
            JOIN SalesLT.CustomerAddress ca ON cs.CustomerID = ca.CustomerID
            JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            GROUP BY GROUPING SETS(pr.ProductID, cs.CustomerID, cs.SalesPerson),
            ROLLUP(ad.CountryRegion, ad.StateProvince, ad.City, ad.PostalCode)'''


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
