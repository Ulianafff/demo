select
    name,
    max(bad) as bad,
    max(good) as good,
    max(ok) as ok
  from (
select
  name,
  case when detail = 'bad' then cnt end as bad,
  case when detail = 'good' then cnt end as good,
  case when detail = 'ok' then cnt end as ok
from(
      select
      name,
      detail,
      count(*) as cnt
      from products p inner join details d
      on p.id = d.product_id
      group by name, detail
      order by name, detail asc) sq1
      ) sq2
   group by name
      ;