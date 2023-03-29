# 1 - contact your vendors
from collections import OrderedDict  # standard library
import datetime  # standard library
import decimal  # standard library
from enum import Enum  # standard library
import typing  # standard library
import factory
import pandas as pd
from pydantic import BaseModel


def model(dbt, session):
    dbt.config(
        materialized="incremental",
        packages=["pandas", "pydantic", "factory_boy"],
        unique_key=["order_id"],
    )

    # 2 - Set the mold
    class DataMold(BaseModel):
        order_id: int
        order_date: datetime.datetime
        customer_id: int
        product: str
        quantity: int
        price: decimal.Decimal
        total: decimal.Decimal

    # 3 - Load the hopper
    customer_df = dbt.ref("su_customers").df()

    # 4 - Assemble the machine
    data_factory = factory.make_factory(
        DataMold,
        order_id=factory.Faker("random_int", min=1, max=1000000),
        order_date=factory.Faker("date_between", start_date="-1y", end_date="today"),
        customer_id=factory.Iterator(customer_df.customer_id),
        product=factory.Faker(
            "random_element", elements=OrderedDict([("A", 0.5), ("B", 0.3), ("C", 0.2)])
        ),
        quantity=factory.Faker("random_int", min=1, max=10),
        price=factory.Faker("pydecimal", min_value=1, max_value=100, right_digits=3),
        total=factory.LazyAttribute(lambda o: o.quantity * o.price),
    )

    # 5 - Run a shift
    data = factory.build_batch(dict, 5, FACTORY_CLASS=data_factory)

    # 6 - Package & ship the product
    return pd.DataFrame(data)
