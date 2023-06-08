select
f.film_id as film_id,
f.title || (case when i.cnt <=5 then ' is not popular'
             when i.cnt > 5 and i.cnt <=15 then ' is slightly popular'
             when i.cnt > 15 and i.cnt <=30 then ' is moderately popular'
             when i.cnt > 30 then ' is very popular' end) as popularity,
i.cnt as rental_count
from film f join film_category using(film_id)
join category c using(category_id)
join (select film_id, count(distinct customer_id) as cnt
      from inventory join rental using(inventory_id) group by 1) i
using(film_id)
where c.name = 'Children'
order by 3 desc, f.title asc