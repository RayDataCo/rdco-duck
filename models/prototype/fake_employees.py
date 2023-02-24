import pandas as pd
from pydantic import BaseModel
import factory


def model(dbt, session):
    dbt.config(
        materialized="incremental",
        packages=["pandas", "pydantic", "factory_boy"],
        unique_key=["company_id", "user_id"],
    )

    class Employee(BaseModel):
        company_id: str
        user_id: int
        start_date: str

    # TODO - Can you DRY up this code?
    user_df = dbt.ref("fake_users")
    if dbt.config.get("target_type") == "duckdb":
        user_df = user_df.df()
    else:
        user_df = user_df.to_pandas()

    company_df = dbt.ref("fake_companies")
    if dbt.config.get("target_type") == "duckdb":
        company_df = company_df.df()
    else:
        company_df = company_df.to_pandas()

    ################################
    ## Lay Out Factory Floor Plan ##
    ################################
    EmpFactory = factory.make_factory(
        Employee,
        id=factory.LazyAttribute(lambda e: hash(f"{e.company_id}{e.user_id}".encode())),
        company_id=factory.Iterator(company_df.id),
        user_id=factory.Iterator(user_df.id),
        start_date=factory.Faker("date_between", start_date="-2y"),
    )

    #################
    ## Run a Shift ##
    #################
    data = factory.build_batch(dict, 5, FACTORY_CLASS=EmpFactory)

    #############################
    ## Package & Ship to table ##
    #############################
    df = pd.DataFrame(data)

    return df
