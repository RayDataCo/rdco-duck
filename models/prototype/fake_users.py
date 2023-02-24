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
