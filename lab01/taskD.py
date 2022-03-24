import pyodbc
from tabulate import tabulate

# Report about income from sales and provided discounts by product
# and hierarchy of product categories
# (high level category-> next level category->...->low level category->product).
# Please mind that some products can be outside (any) category or be
# only partially categorized (be not in low level of hierarchy).
# You can rely on you data to solve to solve this task
# (especially on that how much subcategories in the current data set),
# but try to think how to solve this task in general
# (with arbitrary category tree).

# select count(*) from [SalesLT].[ProductCategory] ch
# join [SalesLT].[ProductCategory] pt on pt.productcategoryid = ch.parentproductcategoryid
# join [SalesLT].[ProductCategory] ppt on ppt.productcategoryid = pt.parentproductcategoryid

query = '''SELECT pr.ProductID, 
            cat1.ProductCategoryID AS SUBCAT,
            cat2.ProductCategoryID AS CAT,
            COALESCE(SUM(sod.UnitPrice * (1 - sod.UnitPriceDiscount) * sod.OrderQty), 0) AS Sum,
            COALESCE(SUM(sod.UnitPrice * sod.UnitPriceDiscount * sod.OrderQty), 0) AS TotalDiscount
            FROM SalesLT.Product pr
            LEFT JOIN SalesLT.SalesOrderDetail sod ON sod.ProductID = pr.ProductID
            JOIN SalesLT.ProductCategory cat1 ON cat1.ProductCategoryID = pr.ProductCategoryID
            JOIN SalesLT.ProductCategory cat2 ON cat2.ProductCategoryID = cat1.ParentProductCategoryID
            GROUP BY ROLLUP(cat2.ProductCategoryID, cat1.ProductCategoryID, pr.ProductID)'''


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
