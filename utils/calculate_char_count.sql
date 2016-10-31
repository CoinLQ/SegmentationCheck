SET SEARCH_PATH TO public;
INSERT INTO public.segmentation_characterstatistics (char,total_cnt, correct_cnt, err_cnt,uncheck_cnt, weight)
SELECT 
char,
  count(segmentation_character."char") as total_cnt,
  sum(case when is_correct= 1 then 1 else 0 end) as correct_cnt,
  sum(case when is_correct= -1 then 1 else 0 end) as err_cnt,
  sum(case when is_correct= 0 then 1 else 0 end) as uncheck_cnt,
  0
FROM
  public.segmentation_character
where is_correct = -1 or is_correct =1 or is_correct = 0
  group by char
ON CONFLICT (char)
DO UPDATE SET 
total_cnt=EXCLUDED.total_cnt,
correct_cnt =EXCLUDED.correct_cnt,
err_cnt =EXCLUDED.err_cnt,
uncheck_cnt=EXCLUDED.uncheck_cnt;
