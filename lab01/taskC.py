import pyodbc
from tabulate import tabulate
# Report about income from sales and provided discounts
# by location in form of hierarchy
# city>state/province>country/region.
# In that report you can rely on unique geographical names,
# but in general it is not the case. Think about how to
# solve that task in case that there is a possibility of
# existence of multiple cities in the same province with
# the same name. For big cities someone would need more
# detailed report that can include city districts, solve
# this task for extra points.


query = '''SELECT ad.PostalCode, ad.City, ad.StateProvince,
            ad.CountryRegion,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum,
            COALESCE(SUM(sod.UnitPrice * sod.UnitPriceDiscount * sod.OrderQty), 0) AS TotalDiscount
            FROM SalesLT.SalesOrderHeader soh
            JOIN SalesLT.Customer cs ON soh.CustomerID = cs.CustomerID
            JOIN SalesLT.CustomerAddress ca ON cs.CustomerID = ca.CustomerID
            JOIN SalesLT.Address ad ON ca.AddressID = ad.AddressID
            JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
            GROUP BY ROLLUP(ad.CountryRegion, ad.StateProvince, ad.City, ad.PostalCode)'''


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
