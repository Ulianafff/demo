with tot as (
select 
	count(*) as tamt, 
	fc.category_id as catid
from film f left join film_category fc
	on f.film_id = fc.film_id
group by fc.category_id)

select
	c.name as category_name,
	f.rating as film_rating,
	round( count(*)::numeric*100.0/max(tot.tamt)::numeric ,3) as percentage
from film f left join film_category fc
	on f.film_id = fc.film_id
left join category c 
	on fc.category_id = c.category_id
left join tot
	on fc.category_id = tot.catid
group by c.name, f.rating
order by c.name asc, 3 desc, 2 asc