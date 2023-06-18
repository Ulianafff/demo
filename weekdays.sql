CREATE FUNCTION weekdays(d1 date, d2 date) RETURNS int as
$BODY$
declare 
   counter date := LEAST($1,$2);
   enddate date := GREATEST($1,$2);
   cnt integer := 0;
begin
   while counter <= enddate loop
	  if extract(dow from counter) not in (0,6) 
	then cnt := cnt + 1;
	end if;
	counter := counter + INTERVAL '1 day';
   end loop;
   --RETURN QUERY SELECT cnt::text || ' working days between ' || $1::text || ' and ' || $2::text;
	RETURN cnt;
end;
$BODY$
LANGUAGE plpgsql;

select * from weekdays('2023-05-08'::date, '2023-06-30'::date);