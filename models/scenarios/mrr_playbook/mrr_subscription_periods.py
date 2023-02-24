# 1 - contact your vendors
import datetime
import decimal
import factory
import pandas as pd
from pydantic import BaseModel


def model(dbt, session):
    dbt.config(
        materialized="incremental",
        packages=["pandas", "pydantic", "factory_boy"],
        unique_key="subscription_id",
    )

    # 2 - Set the mold
    class DataMold(BaseModel):
        subscription_id: int
        customer_id: int
        start_date: datetime.date
        end_date: datetime.date
        monthly_amount: decimal.Decimal

    # 3 - Load the hopper
    # Not needed here
    # 4 - Assemble the machine
    data_factory = factory.make_factory(
        DataMold,
        subscription_id=factory.Faker("random_int"),
        customer_id=factory.Faker("random_int"),
        start_date=factory.Faker(
            "date_between_dates",
            date_start=datetime.date(2020, 1, 1),
            date_end=(datetime.datetime.now()).date(),
        ),
        end_date=factory.LazyAttribute(
            lambda o: o.start_date + datetime.timedelta(weeks=52)
        ),
        monthly_amount=factory.Faker("random_int", min=10, max=100, step=5),
    )

    # 5 - Run a shift
    data = factory.build_batch(dict, 1000, FACTORY_CLASS=data_factory)

    # 6 - Package & ship the product
    return pd.DataFrame(data)
