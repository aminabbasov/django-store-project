# Generated by Django 4.2 on 2023-07-12 05:34

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_review_rating"),
    ]

    operations = [
        migrations.CreateModel(
            name="SingleProductView",
            fields=[
                ("product_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("public_id", models.UUIDField()),
                ("available", models.BooleanField()),
                ("created", models.DateTimeField()),
                ("modified", models.DateTimeField()),
                ("name", models.CharField(max_length=255)),
                ("short_description", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("information", models.TextField()),
                ("views", models.PositiveIntegerField()),
                ("min_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("max_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("min_discounted_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("max_discounted_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("min_discount", models.IntegerField()),
                ("max_discount", models.IntegerField()),
                ("quantity", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "products_singleproductview",
                "managed": False,
            },
        ),
        
        # custom SQL
        
        # create materialized view
        migrations.RunSQL(
            """
            -- Yes, I could make a request without CTE, but it is just more convinient.
            CREATE MATERIALIZED VIEW IF NOT EXISTS
            	products_singleproductview AS
            WITH only_available AS (
                SELECT
                    *
                FROM
                    products_productview
                WHERE
                    product_available = true
                    AND
                    variant_available = true
                )

            SELECT DISTINCT
                product_id,
                public_id,
                product_available AS available,
                product_created AS created,
                product_modified AS modified,
                name,
                short_description,
                description,
                information,
                views,
                MIN(price) AS min_price,
                MAX(price) AS max_price,
                MIN(discount) AS min_discount,
                MAX(discount) AS max_discount,
                ROUND(MIN(price * (1 - discount::numeric / 100)), 2) AS min_discounted_price,
                ROUND(MAX(price * (1 - discount::numeric / 100)), 2) AS max_discounted_price,
                SUM(quantity) AS quantity
            FROM
                only_available
            GROUP BY
                product_id,
                public_id,
                product_available,
                product_created,
                product_modified,
                name,
                short_description,
                description,
                information,
                views;
            """
        ),
        
        # create refresh function
        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION
            	refresh_products_singleproductview()
            RETURNS TRIGGER LANGUAGE
            	plpgsql
            AS $$
            BEGIN
                REFRESH MATERIALIZED VIEW
            		products_singleproductview;
                RETURN
            		null;
            END $$;
            """
        ),
        
        # create trigger on Product model
        migrations.RunSQL(
            """
            CREATE TRIGGER
            	refresh_products_singleproductview
            AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE
            	ON products_product FOR EACH STATEMENT
            EXECUTE PROCEDURE
            	refresh_products_singleproductview();
            """
        ),
        
        # create trigger on ProductVariant model 
        migrations.RunSQL(
            """
            CREATE TRIGGER
            	refresh_products_singleproductview
            AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE
            	ON products_productvariant FOR EACH STATEMENT
            EXECUTE PROCEDURE
            	refresh_products_singleproductview();
            """
        ),
    ]
