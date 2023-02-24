# MRR Dashboard

```orders_by_month
select
  date_month,
  change_category,
  sum(mrr) as mrr,
  sum(is_active::INT) as customer_count
from main.mrr_mrr
group by 1, 2
```

```total_mrr_by_month
select 
  date_month,
  sum(mrr) as mrr,
  sum(customer_count) as customer_count
from ${orders_by_month}
group by 1
```

```current_metrics
with prior_month as (
  select
    date_month + interval '1 month' as date_month,
    mrr as prior_mrr,
    customer_count as prior_customer_count
  from ${total_mrr_by_month}
  where date_month = date_trunc('month', current_date - interval '1 month')
), current_month as (
  select
    date_month,
    mrr,
    customer_count
  from ${total_mrr_by_month}
  where date_month = date_trunc('month', current_date)
)
select
  current_month.date_month,
  current_month.mrr,
  prior_month.prior_mrr,
  current_month.mrr - prior_month.prior_mrr as mrr_change,
  (current_month.mrr - prior_month.prior_mrr) / prior_month.prior_mrr as mrr_change_pct,
  current_month.customer_count,
  prior_month.prior_customer_count,
  current_month.customer_count - prior_month.prior_customer_count as customer_count_change,
  (current_month.customer_count - prior_month.prior_customer_count) / prior_month.prior_customer_count as customer_count_change_pct
from current_month
left join prior_month
  on current_month.date_month = prior_month.date_month
```

<LineChart 
    data={total_mrr_by_month}  
    x='date_month'
    y='mrr_usd'
/>

<BigValue 
  data={current_metrics} 
  title='Current MRR'
  value='mrr_usd' 
  comparison='mrr_change_pct'
  comparisonTitle='Month over Month'
/>

<BigValue 
  data={current_metrics} 
  title='Current Customers'
  value='customer_count' 
  comparison='customer_count_change_pct'
  comparisonTitle='Month over Month'
/>
