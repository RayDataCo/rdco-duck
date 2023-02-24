
        
            delete from "dbt"."main"."su_customers"
            where (
                customer_id) in (
                select (customer_id)
                from "su_customers__dbt_tmp20230224232717078644"
            );

        
    

    insert into "dbt"."main"."su_customers" ("customer_id", "email", "first_name", "last_name", "full_name", "state", "created_at")
    (
        select "customer_id", "email", "first_name", "last_name", "full_name", "state", "created_at"
        from "su_customers__dbt_tmp20230224232717078644"
    )
  