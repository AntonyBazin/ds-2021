# myfirstsqlserv.database.windows.net
# Report about income from sales by product, client and sales person.
# Please mind discounts.
# Also mind that for some combinations of values in these dimensions
# there are no sales at all, so create two versions of queries
# with and without zero values.
import pyodbc
from tabulate import tabulate

queries = ['''SELECT pr.ProductID,
            cs.CustomerID,
            cs.SalesPerson,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum
            FROM SalesLT.SalesOrderHeader soh
            JOIN SalesLT.Customer cs ON soh.CustomerID = cs.CustomerID
            JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
            JOIN SalesLT.Product pr ON sod.ProductID = pr.ProductID
            GROUP BY GROUPING SETS(pr.ProductID, cs.CustomerID, cs.SalesPerson)''',

           '''SELECT pr.ProductID,
            cs.CustomerID,
            cs.SalesPerson,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum
            FROM SalesLT.SalesOrderHeader soh
            FULL JOIN SalesLT.Customer cs ON soh.CustomerID = cs.CustomerID
            FULL JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
            FULL JOIN SalesLT.Product pr ON sod.ProductID = pr.ProductID
            GROUP BY GROUPING SETS(pr.ProductID, cs.CustomerID, cs.SalesPerson)''']


def get_data(query: str):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=myfirstsqlserv.database.windows.net;DATABASE=myFirstDatabase;'
        'UID=your_login;PWD=your_password')
    cursor = connection.cursor()
    rows = cursor.execute(query)
    head = [tpl[0] for tpl in rows.description]
    rows = cursor.fetchall()
    connection.close()
    return tabulate(rows, headers=head, tablefmt='grid'), len(rows)


if __name__ == '__main__':
    qtype = 1 if int(input('Input query type (0 or 1): ')) else 0
    result, amount = get_data(queries[qtype])
    print(result)
    print(f'Rows fetched: {amount}')
