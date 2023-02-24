
        
            delete from "dbt"."main"."fake_employees"
            using "fake_employees__dbt_tmp20230224232717392558"
            where (
                
                    "fake_employees__dbt_tmp20230224232717392558".company_id = "dbt"."main"."fake_employees".company_id
                    and 
                
                    "fake_employees__dbt_tmp20230224232717392558".user_id = "dbt"."main"."fake_employees".user_id
                    
                
                
            );
        
    

    insert into "dbt"."main"."fake_employees" ("id", "company_id", "user_id", "start_date")
    (
        select "id", "company_id", "user_id", "start_date"
        from "fake_employees__dbt_tmp20230224232717392558"
    )
  