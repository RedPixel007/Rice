select c_id,initials,segment,s_id,etnumber,cur_balance,replenishment_time
from client
join subscriber using(c_id) where c_id=%s