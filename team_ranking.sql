with step1 as ( -- select members + score + teams
SELECT
  t.name   AS team_name,
  tm.id    AS member_id,
  tm.name  AS member_name,
  tm.score AS member_score,
  row_number() over (partition by t.name order by tm.score desc, tm.id asc) as rn
FROM teams t
JOIN team_members tm ON tm.team_id = t.id),

step2 as ( -- aggregating team results & filtering members with top 5 scores
  SELECT
  team_name,
  member_name,
  member_score,
  sum(member_score) over (partition by team_name) as team_score
FROM step1
  where rn < 6
),

step3 as ( -- ranking teams by score (needed for intermediary database check) + assembling top_members column
select
  dense_rank() over (order by team_score desc) as team_rank,
  team_name,
  team_score,
  string_agg(member_name || ' (' || member_score || '),', ' ') over (partition by team_name) as top_members
from step2
order by 1),

step4 as ( -- cutting top_members to final representation, grouping for intermediary database check
select 
  team_rank,
  team_name,
  team_score,
  left(top_members, length(top_members)-1) as top_members
from step3
group by 1,2,3,4
order by 1
limit 10)

select -- end-to-end numbering
  rank() over (order by team_score desc) as team_rank,
  team_name,
  team_score,
  top_members
from step4;
