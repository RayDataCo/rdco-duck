
  
    ## FAKING PROCESS ##
# 1 - Contact your vendors
# 2 - Set the mold
# 3 - Load the hopper
# 4 - Assemble the machine
# 5 - Run a shift
# 6 - Package & ship the product

# 1 - contact your vendors
import datetime  # standard library
import decimal  # standard library
from enum import Enum  # standard library
import factory
import typing  # standard library
import pandas as pd
from pydantic import BaseModel, condecimal, conint, confloat, constr, conbytes, condate


def model(dbt, session):
    dbt.config(
        materialized="table",
        packages=["pandas", "pydantic", "factory_boy"],
        unique_key=["company_id", "user_id"],
    )

    # -- PYNDANTIC -- add `| None` to make a field NULLABLE
    # 2 - Set the mold
    class DataMold(BaseModel):
        number: decimal.Decimal
        number_fixed: condecimal(max_digits=2, decimal_places=2)
        # int: int
        # int_fixed: conint()
        # float: float
        # float_fixed: confloat()
        # varchar: str
        # varchar_long: constr()
        # binary: bytes
        # binary_fixed: conbytes()
        # enum: Enum
        # boolean: bool
        # boolean_and_null: bool | None
        # date: datetime.date
        # date_fixed: condate()
        # datetime: datetime.datetime
        # time: datetime.time
        # timestamp_tz: datetime.datetime
        # variant: typing.Dict
        # object: typing.Dict
        final: str

    # 3 - Load the hopper
    # Not needed here
    # 4 - Assemble the machine
    data_factory = factory.make_factory(
        DataMold,
        number=factory.Faker("random_number"),
        number_fixed=factory.Faker("random_number"),
        # int = factory.Faker("random_int"),
        # int_fixed = factory.Faker("random_int"),
        # float = factory.Faker("random_number"),
        # float_fixed = factory.Faker("random_number"),
        # varchar = factory.Faker("name"),
        # varchar_long = factory.Faker("paragrahs"),
        # binary = factory.Faker("binary"),
        # binary_fixed = factory.Faker("binary"),
        # enum = factory.Faker("random_choices"),
        # boolean = factory.Faker("boolean"),
        # boolean_and_null = factory.Faker("null_boolean"),
        # date = factory.Faker("date"),
        # date_fixed = factory.Faker("date_between"),
        # datetime = factory.Faker("date_time"),
        # time = factory.Faker("time"),
        # timestamp_tz = factory.Faker("date_time_between_dates"),
        # variant = factory.Faker("json"),
        # object = factory.Faker("json"),
        final=factory.Faker("company"),
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
    identifier = 'fake_kitchen_sink'
    def __repr__(self):
        return 'dbt.main.fake_kitchen_sink'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args: ref(*args, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------




def materialize(df, con):
    # For the DuckDBPyRelation checks
    import duckdb

    # make sure pandas exists before using it
    try:
        import pandas
        pandas_available = True
    except ImportError:
        pandas_available = False

    # make sure pyarrow exists before using it
    try:
        import pyarrow
        pyarrow_available = True
    except ImportError:
        pyarrow_available = False

    if isinstance(df, duckdb.DuckDBPyRelation):
        if pyarrow_available:
            df = df.arrow()
        elif pandas_available:
            df = df.df()
        else:
            raise Exception("No pandas or pyarrow available to materialize DuckDBPyRelation")
    elif not (
      (pandas_available and isinstance(df, pandas.DataFrame))
      or (pyarrow_available and isinstance(df, pyarrow.Table))
    ):
        raise Exception( str(type(df)) + " is not a supported type for dbt Python materialization")

    con.execute('create table "dbt"."main"."fake_kitchen_sink__dbt_tmp" as select * from df')

  