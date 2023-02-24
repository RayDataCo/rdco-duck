import requests
import pandas as pd
import io

# Does not work on Snowflake - blocked from making external API requests


def model(dbt, session):
    dbt.config(materialized="table", packages=["pandas", "requests"])

    response = requests.get(
        "https://my.api.mockaroo.com/users.csv", params={"key": "306e8c00"}
    )

    data = pd.read_csv(io.StringIO(response.text), ",")

    print(data)

    return data


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args,dbt_load_df_function):
    refs = {}
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
    database = 'main'
    schema = 'main'
    identifier = 'mock_api_from_schema'
    def __repr__(self):
        return 'main.main.mock_api_from_schema'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args: ref(*args, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------


