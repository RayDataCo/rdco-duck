# 1 - contact your vendors
import datetime  # standard library
import factory
import pandas as pd
from pydantic import BaseModel


def model(dbt, session):
    dbt.config(
        materialized="incremental",
        packages=["pandas", "pydantic", "factory_boy"],
        unique_key="customer_id",
    )

    # 2 - Set the mold
    class DataMold(BaseModel):
        customer_id: int
        email: str
        first_name: str
        last_name: str
        full_name: str
        state: str
        created_at: datetime.datetime

    # 3 - Load the hopper
    # Not needed here
    # 4 - Assemble the machine
    data_factory = factory.make_factory(
        DataMold,
        customer_id=factory.Faker("random_int", min=1, max=1000000),
        email=factory.Faker("email"),
        first_name=factory.Faker("first_name"),
        last_name=factory.Faker("last_name"),
        full_name=factory.LazyAttribute(lambda o: f"{o.first_name} {o.last_name}"),
        state=factory.Faker("state"),
        created_at=factory.Faker(
            "date_time_between_dates",
            datetime_start=datetime.datetime(2020, 1, 1),
            datetime_end=datetime.datetime.now(),
        ),
    )

    # 5 - Run a shift
    data = factory.build_batch(dict, 1000, FACTORY_CLASS=data_factory)

    # 6 - Package & ship the product
    return pd.DataFrame(data)
