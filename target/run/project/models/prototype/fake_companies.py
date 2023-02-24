

    insert into "dbt"."main"."fake_companies" ("id", "name")
    (
        select "id", "name"
        from "fake_companies__dbt_tmp20230224232716132766"
    )
  