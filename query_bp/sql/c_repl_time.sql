select c.c_id, initials,s.s_id,replenishment_time,etnumber
from client c
join subscriber s on extract(month from replenishment_time )between %s and %s and s.c_id = c.c_id  and c.c_id = %s;