import pandas as pd
from pydantic import BaseModel
import factory


class User(BaseModel):
    id: int
    name = "Jane Doe"


class UserFactory(factory.Factory):
    # class Meta:
    #     model = User

    id = factory.Faker("random_int", min=0, max=100)
    name = factory.Faker("name")


def model(dbt, session):
    # "OrgAdmin" must first accept the Anacoda third-party package conditions
    # Find the package list in the Information Schema
    # ANALYTICS.INFORMATION_SCHEMA.PACKAGES where language = 'python'
    dbt.config(
        materialized="incremental", packages=["pandas", "pydantic", "factory_boy"]
    )

    data = factory.build_batch(dict, 5, FACTORY_CLASS=UserFactory)

    print(data)

    df = pd.DataFrame(data)

    return df


# What do I want to know about a dataset?
#
# - column name
# - data type
# - expected values
#   - cagtegorical
#   - numeric range
#   - distribution curve or probablity for a few categorical fields
#   - nullable?
#     - error rate nullable?
#   - date ranges
# - primary key
# - foreign keys / relationships


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
    database = 'dbt'
    schema = 'main'
    identifier = 'fake_users'
    def __repr__(self):
        return 'dbt.main.fake_users'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args: ref(*args, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = True

# COMMAND ----------


