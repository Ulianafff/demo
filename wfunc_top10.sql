select 
  category_id,
  category,
  title,
  views,
  post_id
   from
   (select
      c.id as category_id,
      category,
      p.title,
      p.id as post_id,
      views,
      rank() over (partition by c.id, category order by views desc, p.id asc) as pos
    from posts p right join categories c
    on c.id = p.category_id) sq
    where pos < 3
    order by 2,4 desc,5 asc;