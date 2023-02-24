

    insert into "dbt"."main"."fake_users" ("id", "name")
    (
        select "id", "name"
        from "fake_users__dbt_tmp20230224232716679695"
    )
  