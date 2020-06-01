# 天眼查专业版 测试

### 说明
* 爬取企业基本信息
* 投资、被失信执行人等爬取思路 

###引导
* 使用前请自行更新headers中的cookies
* pip install -r requirements.txt 安装所需依赖 （python版本3.7）
* 执行get_json_data 获取所需的企业基本信息数据(格式为json 串) 
* parse_data 爬取时直接解析或解析爬取后存入数据库的数据 
* sczh get_company 获取一个企业投资的一级二级公司 其中async_get 为异步速度大概快3倍
* sql 中company_data.sql 用于存储爬下来的json 数据 另外两个表对应detail_info 中字段，表中有备注仅供参考。
### 投资、被失信执行人等爬取思路 
* "https://std.tianyancha.com/pagination/invest.xhtml?ps=50pn=1&id=" + id 其中invest 对应对外投资
可替换成其他字段，具体网页js 中找，如lawsuit 裁判文书，知道公司id 即可爬取  ps 时一页显示的数量，pn为第几页
