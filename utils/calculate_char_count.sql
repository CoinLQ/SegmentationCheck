INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
SELECT 
char,
  count(segmentation_character."char") as total_cnt,
  sum(case when is_correct= 0 then 1 else 0 end) as uncheck_cnt,
  sum(case when is_correct=-1 then 1 else 0 end) as err_cnt,
  0
FROM 
  public.segmentation_character
  group by char;