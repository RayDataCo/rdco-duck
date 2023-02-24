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
        unique_key=["company_id", "user_id"],
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
        price=factory.Faker("random_decimal", min=1, max=100, right_digits=2),
        total=factory.LazyAttribute(lambda o: o.quantity * o.price),
    )

    # 5 - Run a shift
    data = factory.build_batch(dict, 5, FACTORY_CLASS=data_factory)

    # 6 - Package & ship the product
    return pd.DataFrame(data)


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args,dbt_load_df_function):
    refs = {"su_customers": "dbt.main.su_customers"}
    key = ".".join(args)
    return dbt_load_df_function(refs[key])


def source(*args, dbt_load_df_function):
    sources = {}
    key = ".".join(args)
    return dbt_load_df_function(sources[key])


config_dict = {}


class config:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get(key, default=None):
        return config_dict.get(key, default)

class this:
    """dbt.this() or dbt.this.identifier"""
    database = 'dbt'
    schema = 'main'
    identifier = 'su_orders'
    def __repr__(self):
        return 'dbt.main.su_orders'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args: ref(*args, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------


