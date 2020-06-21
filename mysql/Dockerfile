from mysql:5.7
#基础镜像
ENV MYSQL_ALLOW_EMPTY_PASSWORD no
#不允许空密码登录
ENV MYSQL_ROOT_PASSWORD=123456
#root密码
COPY setup.sh /mysql/setup.sh
COPY schema.sql /mysql/schema.sql
#所需文件
CMD ["sh", "/mysql/setup.sh"]
#启动命令