
  
    

    create  table
      "dbt"."main"."mrr_utils_months__dbt_tmp"
    as (
      





with rawdata as (

    

    

    with p as (
        select 0 as generated_number union all select 1
    ), unioned as (

    select

    
    p0.generated_number * power(2, 0)
     + 
    
    p1.generated_number * power(2, 1)
     + 
    
    p2.generated_number * power(2, 2)
     + 
    
    p3.generated_number * power(2, 3)
     + 
    
    p4.generated_number * power(2, 4)
     + 
    
    p5.generated_number * power(2, 5)
    
    
    + 1
    as generated_number

    from

    
    p as p0
     cross join 
    
    p as p1
     cross join 
    
    p as p2
     cross join 
    
    p as p3
     cross join 
    
    p as p4
     cross join 
    
    p as p5
    
    

    )

    select *
    from unioned
    where generated_number <= 61
    order by generated_number



),

all_periods as (

    select (
        

    '2019-01-01'::date + ((interval '1 month') * (row_number() over (order by 1) - 1))


    ) as date_month
    from rawdata

),

filtered as (

    select *
    from all_periods
    where date_month <= current_date + interval 365 DAY

)

select * from filtered


    );
  