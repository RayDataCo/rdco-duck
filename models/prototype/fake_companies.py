import pandas as pd
import factory


class CompanyFactory(factory.Factory):
    id = factory.Faker("uuid4")
    name = factory.Faker("company")


def model(dbt, session):
    # "OrgAdmin" must first accept the Anacoda third-party package conditions
    # Find the package list in the Information Schema
    # ANALYTICS.INFORMATION_SCHEMA.PACKAGES where language = 'python'
    dbt.config(materialized="incremental", packages=["pandas", "factory_boy"])

    data = factory.build_batch(dict, 5, FACTORY_CLASS=CompanyFactory)

    print(data)

    return pd.DataFrame(data)


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
