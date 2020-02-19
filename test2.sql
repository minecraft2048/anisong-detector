 select type,count(*) from anisong where artist in (
	select artist from anisong where anime="Bleach"
	intersect
	select artist from anisong where anime!="Bleach"
) and anime != "Bleach"
group by type 