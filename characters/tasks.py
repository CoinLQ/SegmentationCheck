from celery import task
from django.db import connection

@task()
def add(x, y):
        return x + y

@task
def update_char_stastics():
    cursor = connection.cursor()
    raw_sql = '''
    INSERT INTO public.segmentation_characterstatistics (char,total_cnt, uncheck_cnt,err_cnt,uncertainty_cnt)
    SELECT
        char,
        count(segmentation_character."char") as total_cnt,
        sum(case when is_correct= 0 then 1 else 0 end) as uncheck_cnt,
        sum(case when is_correct<0 then 1 else 0 end) as err_cnt,
        0
    FROM
      public.segmentation_character
      group by char
    ON CONFLICT (char)
    DO UPDATE SET
    total_cnt=EXCLUDED.total_cnt,
    uncheck_cnt=EXCLUDED.uncheck_cnt,
    err_cnt =EXCLUDED.err_cnt;
    '''
    cursor.execute(raw_sql)
    return 'update CharacterStatistics'

