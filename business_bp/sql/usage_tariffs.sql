select tp_id, plan_name, cost_p_minute_day, cost_p_minute_night,min_volume, max_volume, step_volume, have_unlimit, have_stepped_volume, count(*) as usage from tariff_plans tp
join subscriber s using(tp_id)
group by tp_id;