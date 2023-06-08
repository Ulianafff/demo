select film_id, title, special_features from film
where special_features && ARRAY['Trailers'] 
and special_features && ARRAY['Deleted Scenes']
and cardinality(special_features) = 2
order by title, film_id asc;