# SegmentationCheck

##项目说明

  切分检查平台,对图片切分出的字形进行检查与人工调整

##安装向导

在以下步骤开始之前，假定你已经安装好了pip。

1. 安装virtualenv.

        pip install virtualenv

2. 设置virtualenv环境.

        $ virtualenv qiefenvenv
        $ . qiefenvenv/bin/activate

3. 安装项目依赖文件.

        $ pip install -r requirements.txt
        # 请稍等一段时间!

4. 假定你已经安装了postgres，下面进行初步的数据库设置

        $psql -d postgres

        CREATE DATABASE dzj_characters;
        CREATE USER dzj WITH PASSWORD 'dzjsql';
        ALTER ROLE dzj SET client_encoding TO 'utf8';
        ALTER ROLE dzj SET default_transaction_isolation TO 'read committed';
        ALTER ROLE dzj SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE dzj_characters TO dzj;
        \q

        **Note**: 如果psql执行报错，请参考postgres手册，使用正确的超级用户口令。

5. 为设置manage.py正确的执行权限，运行migration.

        $ chmod +x manage.py
        $ python manage.py migrate

6. 设置超级用户

        $ python manage.py createsuperuser

7. 准备本地测试数据

        $ python manage.py loaddata fixtures/page.json

8. 运行本地开发服务器.

        $ python manage.py createsuperuser


