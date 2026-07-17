import os
import json
import psycopg2
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    connection = None
    cursor = None
    
    try:
        connection = psycopg2.connect(
            host="cpp-x24219479-rds.cql8vr2cz2bb.us-east-1.rds.amazonaws.com",
            database="cpp-x24219479-rds",
            user="postgres",
            password="cpp-x24219479-rds",
            port=5432
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Get query parameters for date filtering
        start_date = None
        end_date = None
        if event.get('queryStringParameters'):
            start_date = event['queryStringParameters'].get('start_date')
            end_date = event['queryStringParameters'].get('end_date')
        
        # Build date filter condition
        date_condition = ""
        date_params = []
        if start_date and end_date:
            date_condition = "WHERE s.sale_date BETWEEN %s AND %s"
            date_params = [start_date, end_date]
        elif start_date:
            date_condition = "WHERE s.sale_date >= %s"
            date_params = [start_date]
        elif end_date:
            date_condition = "WHERE s.sale_date <= %s"
            date_params = [end_date]
        
        # Sales by Product (using app_product and app_sale)
        try:
            query = f"""
                SELECT
                    p.name AS product,
                    COALESCE(SUM(s.total_price), 0) AS total_sales
                FROM app_sale s
                JOIN app_product p ON s.product_id = p.id
                {date_condition}
                GROUP BY p.name
                ORDER BY total_sales DESC;
            """
            cursor.execute(query, date_params)
            sales_by_product = [
                {"product": row[0], "total_sales": float(row[1])}
                for row in cursor.fetchall()
            ]
            logger.info(f"Sales by product: {len(sales_by_product)} products")
        except Exception as e:
            logger.warning(f"Could not fetch sales by product: {str(e)}")
            sales_by_product = []
        
        # Inventory by Product (using app_productinventory)
        try:
            cursor.execute("""
                SELECT
                    p.name AS product,
                    COALESCE(SUM(pi.stock), 0) AS total_stock
                FROM app_product p
                LEFT JOIN app_productinventory pi ON p.id = pi.product_id
                GROUP BY p.name
                ORDER BY total_stock DESC;
            """)
            inventory_by_product = [
                {"product": row[0], "total_stock": int(row[1])}
                for row in cursor.fetchall()
            ]
            logger.info(f"Inventory by product: {len(inventory_by_product)} products")
        except Exception as e:
            logger.warning(f"Could not fetch inventory by product: {str(e)}")
            inventory_by_product = []
        
        # Monthly Sales
        try:
            query = f"""
                SELECT
                    TO_CHAR(s.sale_date, 'Mon') AS month,
                    COALESCE(SUM(s.total_price), 0) AS sales
                FROM app_sale s
                {date_condition}
                GROUP BY month, DATE_TRUNC('month', s.sale_date)
                ORDER BY DATE_TRUNC('month', s.sale_date);
            """
            cursor.execute(query, date_params)
            monthly_sales = [
                {"month": row[0], "sales": float(row[1])}
                for row in cursor.fetchall()
            ]
            logger.info(f"Monthly sales: {len(monthly_sales)} months")
        except Exception as e:
            logger.warning(f"Could not fetch monthly sales: {str(e)}")
            monthly_sales = []
        
        # Also get total sales and orders for summary (optional)
        cursor.execute("SELECT COALESCE(SUM(total_price), 0) FROM app_sale;")
        total_sales = float(cursor.fetchone()[0])
        
        cursor.execute("SELECT COUNT(*) FROM app_sale;")
        total_orders = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        # Return in the format expected by Django
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "sales_by_product": sales_by_product,
                "inventory_by_product": inventory_by_product,
                "monthly_sales": monthly_sales,
                "total_sales": total_sales,
                "total_orders": total_orders
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if connection:
            connection.rollback()
            connection.close()
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
        
        
        