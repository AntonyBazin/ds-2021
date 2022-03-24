import pyodbc
from tabulate import tabulate
# Report about income from sales by product, client and country (region)
# for billing, shipping and client residency as they can be different.
# Is it case according our data? But you should generalize in any case.
# Please mind discounts. You should include in that report
# only data that supported by sales (so no zero entries except
# discounted price is zero).

# CONFIRMED: only address entries for main office & shipping

query = '''SELECT sod.ProductID,
            soh.CustomerID,
            ad.CountryRegion AS ClientResidency,
            ab.CountryRegion AS BillsTo,
            ash.CountryRegion AS ShipTo,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum
            FROM SalesLT.SalesOrderHeader soh
            JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
            JOIN SalesLT.CustomerAddress ca ON soh.CustomerID = ca.CustomerID
            JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            JOIN SalesLT.Address ab ON soh.BillToAddressID = ab.AddressID
            JOIN SalesLT.Address ash ON soh.ShipToAddressID = ash.AddressID
            GROUP BY GROUPING SETS((soh.CustomerID, sod.ProductID, ad.CountryRegion),
            (soh.CustomerID, sod.ProductID, ab.CountryRegion),
            (soh.CustomerID, sod.ProductID, ash.CountryRegion))'''


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
