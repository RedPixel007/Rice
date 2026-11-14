insert into tariff_plans
values (
	default,
	%s,
	%s,
	%s,
	%s,
	%s,
	%s,
	%s,
	%s
)
returning tp_id;