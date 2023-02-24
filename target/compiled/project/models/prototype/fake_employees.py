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


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args,dbt_load_df_function):
    refs = {"fake_companies": "dbt.main.fake_companies", "fake_users": "dbt.main.fake_users"}
    key = ".".join(args)
    return dbt_load_df_function(refs[key])


def source(*args, dbt_load_df_function):
    sources = {}
    key = ".".join(args)
    return dbt_load_df_function(sources[key])


config_dict = {'target_type': 'duckdb'}


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
    identifier = 'fake_employees'
    def __repr__(self):
        return 'dbt.main.fake_employees'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args: ref(*args, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = True

# COMMAND ----------


