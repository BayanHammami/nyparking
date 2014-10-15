CREATE OR REPLACE VIEW app_summary_vw AS 
 SELECT 
	0 as number_of_fines
	,0 as number_of_dates_with_fines
	,0 as number_of_possible_dates
	,0 as most_likely_probability
	,0 as probability_interval

;

CREATE OR REPLACE FUNCTION app_model_summary_sp(lat numeric, lng numeric, radius int) 
  RETURNS TABLE (
			number_of_fines integer
			,number_of_dates_with_fines integer
			,number_of_possible_dates integer
			,most_likely_probability integer
			,probability_interval integer
		) AS
$func$
   SELECT 
	$3 as number_of_fines -- replace this with actual values and select (params $1 - $3..)
	,0 as number_of_dates_with_fines
	,0 as number_of_possible_dates
	,0 as most_likely_probability
	,0 as probability_interval

$func$ LANGUAGE sql;


CREATE OR REPLACE FUNCTION app_model_summary_sp(lat numeric, lng numeric, radius int)  RETURNS SETOF app_summary_vw AS $$
SELECT * FROM app_summary_vw;
$$ LANGUAGE sql;
