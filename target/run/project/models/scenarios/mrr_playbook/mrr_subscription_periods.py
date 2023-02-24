
        
            delete from "dbt"."main"."mrr_subscription_periods"
            where (
                subscription_id) in (
                select (subscription_id)
                from "mrr_subscription_periods__dbt_tmp20230224232716773261"
            );

        
    

    insert into "dbt"."main"."mrr_subscription_periods" ("subscription_id", "customer_id", "start_date", "end_date", "monthly_amount")
    (
        select "subscription_id", "customer_id", "start_date", "end_date", "monthly_amount"
        from "mrr_subscription_periods__dbt_tmp20230224232716773261"
    )
  