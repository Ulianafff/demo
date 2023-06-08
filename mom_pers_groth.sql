select 
date,
count,
case when prev is null then NULL
else round(cast(100*(count-prev)::float/prev::float as numeric), 1)::text || '%' 
end as percent_growth
from (
      select
      date_trunc('month',created_at)::date as date,
      count(*) as count,
      LAG(count(*)) over(order by date_trunc('month',created_at)::date) as prev
      from posts
      group by 1
      order by 1) x;