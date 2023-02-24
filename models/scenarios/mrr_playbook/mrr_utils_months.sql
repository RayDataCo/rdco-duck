{{ dbt_utils.date_spine(
    datepart="month",
    start_date="'2019-01-01'::date",
    end_date="current_date + interval 365 DAY"
   )
}}