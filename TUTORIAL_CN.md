#小红书笔记监控完整教程
2	 
3	##目录
4	-  [项目介绍]( # 项目介绍)
5	-  [环境准备]( #环境准备)
6	-  [获取需求信息]( #获取需求信息)
7	-  [基础使用]( #基础使用)
8	-  [监控功能详解]( #监控功能详解)
9	-  [实战案例]( #实战案例)
10	-  [疑难解答]( #疑难解答)
11	 
12	---
13	 
14	##项目介绍
15	 
16	### xhs是什么？
17	 
18	`xhs`是一个用于小红书数据抓取的Python工具包，可以：
19	 
20	- 📝 获取笔记详细信息
21	- 👤获取用户信息
22	- 🔍 搜索笔记和用户
23	- 📥 下载图片和视频
24	- 💬获取​​评论信息
25	- ⭐点赞、收藏、关注等互动操作
26	 
27	###监控功能介绍
28	 
29	基于xhs包，我们开发了自动监控工具，可以：
30	 
31	1.  **定时检查**：按设定的时间间隔检查用户是否发布新笔记
32	2.  **自动下载**：发现新笔记后自动下载图片/视频到本地
33	3.  **元数据保存**：保存笔记标题、描述、标签、互动数据等信息
34	4.  **智能去重**：自动记录已下载的笔记，避免重复下载
35	5.  **持续运行**：可以作为后台服务持续运行
36	 
37	---
38	 
39	##环境准备
40	 
41	### 1.系统要求
42	 
43	- Python 3.7 或更高版本
44	-支持Windows、macOS、Linux
45	 
46	### 2.安装Python包
47	 
48	``` bash
49	# 方式一：从PyPI安装（推荐）
50	pip安装xhs
51	
52	# 方式二：从源码安装（开发版）
53	git clone https://github.com/ReaJason/xhs.git
54	cd xhs
55	pip安装-e 。
56	```
57	 
58	### 3.安装Playwright
59	 
60	Playwriter用于生成请求签名：
61	 
62	``` bash
63	pip install playwright
64	剧作家安装Chromium
65	```
66	 
67	如果下载失败，可以在国内使用：
68	 
69	``` bash
70	#设置环境指标
71	export PLAYWRIGHT_DOWNLOAD_HOST = https://npmmirror.com/mirrors/playwright/ 
72	
73	# 然后安装
74	剧作家安装Chromium
75	```
76	 
77	### 4.验证安装
78	 
79	``` bash
80	python -c "import xhs; print('xhs安装成功')"
81	python -c "from playwright.sync_api importsync_playwright; print('playwright安装成功')"
82	```
83	 
84	---
85	 
86	##获取需求信息
87	 
88	###步骤1：获取Cookie
89	 
90	Cookie是访问小红书的权限，需要从浏览器中获取。
91	 
92	####方法一：Chrome浏览器
93	 
94	1.打开Chrome浏览器
95	2.访问https://www.xiaohongshu.com
96	3.登录你的小红书账号
97	4.按`F12`打开开发者工具
98	5.点击顶部的`Network`（网络）标签
99	6.按`F5`刷新页面
100	7.在左侧列表中点击任意请求（通常点击第一个）
101	8.在右侧找到`Request Headers`（请求标头）
102	9.升级找到`Cookie`字段
103	10.右键点击Cookie值，选择`复制值`（复制值）
104	 
105	####方法二：Firefox浏览器
106	 
107	1.打开Firefox浏览器
108	2.访问https://www.xiaohongshu.com
109	3.登录你的小红书账号
110	4.按`F12`打开开发者工具
111	5.点击`网络`标签
112	6.刷新页面
113	7.点击任意请求
114	8.在右侧`标头`中找到`Cookie`
115	9.复制完整的Cookie值
116	 
117	#### Cookie 示例
118	 
119	Cookie类似这样（很长的一串）：
120	 
121	```
122	a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043; webId=ba57f42593b9e55840a289fa0b755374； gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy; ...
123	```
124	 
125	**重要提示：**
126	- Cookie 包含您的登录信息，请填写
127	-不要在公开场合分享您的Cookie
128	- Cookie会过期，需要定期更新
129	 
130	###步骤2：用户获取ID
131	 
132	UserID是用户的唯一标识。
133	 
134	####获取方法
135	 
136	1.访问您想要监控的用户主页
137	2.查看浏览器地址栏的URL
138	3. URL格式为：`https://www.xiaohongshu.com/user/profile/用户ID`
139	 
140	**示例：**
141	 
142	```
143	网址：https://www.xiaoghongshu.com/user/profile/5b3f8c8e0000000001000a1b
144	                                                   └──────┬──────┘
145	                                                       用户ID
146	```
147	 
148	用户ID就是：`5b3f8c8e0000000001000a1b`
149	 
150	####其他获取方式
151	 
152	**从链接分享：**
153	1.在小红书App中打开用户主页
154	2.点击右上角分享
155	3.复制链接
156	4.在浏览器中打开链接
157	5.从URL中提取用户ID
158	 
159	###步骤3：（可选）下载stealth.js
160	 
161	Stealth.js 可以防止被检测为自动化工具。
162	 
163	**下载地址：**
164	https://github.com/requireCool/stealth.min.js/blob/main/stealth.min.js
165	 
166	下载后放在项目目录下。
167	 
168	**注意：**即使不下载此文件，程序也能正常运行，只是可能更容易被检测到。
169	 
170	---
171	 
172	##基础使用
173	 
174	###方式一：使用完整监控工具（推荐）
175	 
176	#### 1.进入示例目录
177	 
178	``` bash
179	CD示例
180	```
181	 
182	#### 2.首次运行生成配置文件
183	 
184	``` bash
185	python monitor_user_notes.py
186	```
187	 
188	会自动生成`monitor_config.json`文件：
189	 
190	``` json
191	{
192	    "cookie" : "your_cookie_here" , 
193	    "user_id" : "target_user_id_here" , 
194	    "download_dir" : "./downloads" , 
195	    "check_interval" : 300 , 
196	    "stealth_js_path" : "./stealth.min.js" , 
197	    "use_headless" : true , 
198	    “max_retries” ：3 ， 
199	    "retry_delay" : 2 , 
200	    "downloaded_notes_file" : "downloaded_notes.json" 
201	}
202	```
203	 
204	#### 3.编辑配置文件
205	 
206	使用文本编辑器打开`monitor_config.json`，修改：
207	 
208	``` json
209	{
210	    "cookie" : "你的cookie" , 
211	    "user_id" : "要监控的用户ID" , 
212	    "download_dir" : "./downloads" , 
213	    "check_interval" : 300 , 
214	    "stealth_js_path" : "./stealth.min.js" , 
215	    "use_headless" : true , 
216	    “max_retries” ：3 ， 
217	    "retry_delay" : 2 , 
218	    "downloaded_notes_file" : "downloaded_notes.json" 
219	}
220	```
221	 
222	**配置说明：**
223	 
224	|配置项|说明|推荐值|
225	| -------- | ------ | -------- |
226	| cookie |你的小红书cookie |必填|
227	| user_id |要监控的用户ID |必填|
228	| download_dir |下载保存目录| ./下载|
229	| check_interval |检查间隔（秒）| 300（5分钟）|
230	|隐身js路径| Stealth.js路径| ./stealth.min.js |
231	| use_headless |是否无头模式|真实|
232	| max_retries |最大重试次数| 3 |
233	| retry_delay |重试延迟（秒）| 2 |
234	
235	#### 4.启动监控
236	 
237	``` bash
238	python monitor_user_notes.py
239	```
240	 
241	**输出示例：**
242	 
243	```
244	==============================================================
245	🚀小红书笔记监控器启动
246	==============================================================
247	配置文件：monitor_config.json
248	监控用户：5b3f8c8e0000000001000a1b
249	检查间隔：300秒
250	下载目录: ./downloads
251	已下载笔记数: 0
252	==============================================================
253	
254	✅ 小红书客户端初始化成功
255	
256	==============================================================
257	🔍检查新笔记 - 2024-01-15 10:30:00
258	==============================================================
259	
260	📋 正在获取用户 5b3f8c8e0000000001000a1b 的笔记列表...
261	   获取 30 条笔记已...
262	✅ 共获取 30 条笔记
263	
264	🎉发现3条新笔记！
265	
266	[1/3]
267	📥开始下载笔记: 6505318c000000001f03c5a6
268	   标题: 冬日穿搭分享
269	   类型： 正常
270	   正在下载3张图片...
271	   ✅ 图片 1/3 已保存
272	   ✅ 图片 2/3 已保存
273	   ✅ 图片 3/3 已保存
274	✅ 笔记 6505318c000000001f03c5a6 下载完成
275	
276	[2/3]
277	...
278	
279	✅ 成功下载 3/3 条新笔记
280	
281	⏰ 下次检查时间：2024-01-15 10:35:00
282	💤等待300秒...
283	```
284	 
285	#### 5. 停止监控
286	 
287	按`Ctrl+C`停止程序。
288	 
289	###方式二：使用快速示例
290	 
291	如果你想快速上手或学习代码，可以使用简化版：
292	 
293	#### 1. 编辑快速示例文件
294	 
295	打开`example/quick_monitor_example.py`，找到配置部分：
296	 
297	``` python
298	# ============ 在这里修改配置 ============
299	
300	#1.你的小红书cookie（必填）
301	COOKIE = "your_cookie_here" 
302	
303	# 2.需要监控的用户ID（必填）
304	USER_ID = "此处填写目标用户ID" 
305	
306	# 3.下载保存目录（任选）
307	下载目录= "./downloads" 
308	
309	# 4.检查间隔秒数（可选，建议显示于300秒）
310	CHECK_INTERVAL = 300 # 5分钟   
311	
312	# ========================================
313	```
314	 
315	修改为你的实际值：
316	 
317	``` python
318	COOKIE = "a1=187d2defea8dz1fg..." 
319	USER_ID = "5b3f8c8e0000000001000a1b" 
320	下载目录= "./downloads" 
321	检查间隔= 300 
322	```
323	 
324	#### 2. 运行
325	 
326	``` bash
327	CD示例
328	蟒蛇quick_monitor_example.py
329	```
330	 
331	###方式三：自己编写的剧本
332	 
333	你也可以基于xhs包编写自己的监控脚本：
334	 
335	``` python
336	from xhs import XhsClient
337	from playwright.sync_api import sync_playwright​​
338	
339	# 定义签名函数
340	def sign ( uri , data = None , a1 = "" , web_session = "" ) : 
341	    with sync_playwright ( ) as playwright : 
342	        browser = playwright.chromium.launch ( headless = True )​​​​
343	        context = browser.new_context ( )​​
344	        page = context.new_page ( )​​
345	        page.goto ( " https://www.xiaoghongshu.com " )
346	        # ...签名逻辑
347	        返回{ "xs" : "..." , "xt" : "..." }    
348	
349	# 初始化客户端
350	客户端= XhsClient ( cookie = "你的cookie" ,符号=符号)
351	
352	#获取用户笔记
353	result = client.get_user_notes ( user_id = "用户ID " )
354	notes = result.get ( " notes " , [ ] ) 
355	
356	#穿越笔记
357	对于笔记中的笔记：
358	    note_id = note.get ( " note_id " )
359	    #获取笔记详情
360	    detail = client.get_note_by_id ( note_id , note.get ( " xsec_token " ) )​​
361	    # 处理笔记...
362	```
363	 
364	---
365	 
366	##监控功能详解
367	 
368	###配置文件详解
369	 
370	＃＃＃＃曲奇饼
371	 
372	**说明：**你的小红书登录记录
373	 
374	**获取方法：**了解“获取必要信息”部分
375	 
376	**示例：**
377	``` json
378	"cookie" : "a1=187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043; webId=ba57f42593b9e55840a289fa0b755374; ..." 
379	```
380	 
381	**注意事项：**
382	- Cookie会过期，通常1-2周需要更新一次
383	-如果遇到登录错误，首先尝试更新Cookie
384	-不同账号的Cookie不同
385	 
386	＃＃＃＃用户身份
387	 
388	**说明：**要监控的用户的唯一标识
389	 
390	**获取方式：**从用户主页URL获取
391	 
392	**示例：**
393	``` json
394	"user_id" : "5b3f8c8e0000000001000a1b" 
395	```
396	 
397	**注意事项：**
398	-用户ID是固定的，不会变化
399	-可以监控任何公开账号
400	-公开账号需要你已关注才能获取笔记
401	 
402	####下载目录
403	 
404	**说明：**笔记下载保存的目录
405	 
406	**默认值：**  `"./downloads"`
407	 
408	**示例：**
409	``` json
410	"download_dir" : "/Users/username/Downloads/xhs_notes" 
411	```
412	 
413	**目录结构：**
414	```
415	下载/
416	├── 笔记标题1_笔记ID1_计时器/
417	│ ├── metadata.json
418	│ ├── 笔记标题1_1.png
419	│ └── 笔记标题1_2.png
420	├── 笔记标题2_笔记ID2_计时器/
421	│ ├── metadata.json
422	│ └── 笔记标题2.mp4
423	└── ...
424	```
425	 
426	####检查间隔
427	 
428	**说明：**检查新笔记的时间间隔（秒）
429	 
430	**默认值：**  `300` (5分钟)
431	 
432	**建议值：**
433	-日常监控：300-600秒（5-10分钟）
434	-重要监控：180-300秒（3-5分钟）
435	-不建议低于60秒，容易被限制
436	 
437	**示例：**
438	``` json
439	"check_interval" : 300 
440	```
441	 
442	####使用无头模式
443	 
444	**说明：**是否使用无头浏览器模式
445	 
446	**默认值：**  `true`
447	 
448	**说明：**
449	-  `true` : 后台运行，不显示浏览器窗口（推荐）
450	-  `false` : 显示浏览器窗口，可以看到签名过程
451	 
452	**何时设为假：**
453	-调试签名问题时
454	-想了解签名过程时
455	-签名经常失败时
456	 
457	**示例：**
458	``` json
459	"use_headless" : true 
460	```
461	 
462	####最大重试次数
463	 
464	**说明：**请求失败时的最大重试次数
465	 
466	**默认值：**  `3`
467	 
468	**建议值：** 2-5
469	 
470	**示例：**
471	``` json
472	“max_retries” ：3 
473	```
474	 
475	####重试延迟
476	 
477	**说明：**重试之间的延迟时间（秒）
478	 
479	**默认值：**  `2`
480	 
481	**建议值：** 1-5
482	 
483	**示例：**
484	``` json
485	"retry_delay" ：2 
486	```
487	 
488	###下载的文件说明
489	 
490	#### metadata.json
491	 
492	每个笔记都会保存一个metadata.json文件，包含：
493	 
494	``` json
495	{
496	    "note_id" : "6505318c000000001f03c5a6" , 
497	    "title" : "冬日穿搭分享" , 
498	    "desc" : "今天分享一套简约的冬日穿搭..." , 
499	    "type" : "normal" , 
500	    "用户" : { 
501	        "user_id" : "5b3f8c8e0000000001000a1b" , 
502	        "昵称" : "时尚博主" , 
503	        "avatar" : "https://..." 
504	    } ，
505	    "标签" : [ 
506	        { "name" : "穿搭" , "type" : "topic" } ,   
507	        { "name" : "冬日" , "type" : "主题" }   
508	    ] ，
509	    "interact_info" : { 
510	        "liked_count" : "1234" , 
511	        "collected_count" : "567" , 
512	        "comment_count" : "89" , 
513	        "share_count" : "12" 
514	    } ，
515	    "download_time" : "2024-01-15T10:30:00.123456" , 
516	    "xsec_token" : "..." 
517	}
518	```
519	 
520	**用途：**
521	-记录笔记的详细信息
522	-用于数据分析
523	-关于搜索和管理
524	-可导入数据库
525	 
526	####图片文件
527	 
528	-格式：PNG
529	-命名：`笔记标题_序号.png`
530	-按原图质量保存
531	 
532	####视频文件
533	 
534	-格式：MP4
535	-命名：`笔记标题.mp4`
536	-原始流程图
537	 
538	###已下载笔记记录
539	 
540	####下载的笔记.json
541	 
542	记录已下载的笔记，避免重复下载：
543	 
544	``` json
545	{
546	    "note_ids" : [ 
547	        "6505318c000000001f03c5a6" ,
548	        "6505318d000000001f03c5b7" ,
549	        "6505318e000000001f03c5c8"
550	    ] ，
551	    "notes_metadata" : { 
552	        "6505318c000000001f03c5a6" : { 
553	            "title" : "冬日穿搭分享" , 
554	            "download_time" : "2024-01-15T10:30:00.123456" , 
555	            "download_path" : "./downloads/冬日穿搭分享_6505318c000000001f03c5a6_20240115_103000" , 
556	            "type" : "normal" 
557	        } ，
558	        ...
559	    }
560	}
561	```
562	 
563	**重要说明：**
564	-删除此文件会重新下载所有笔记
565	-可以手动编辑跳过某些笔记
566	-定期备份此文件
567	 
568	---
569	 
570	##实战案例
571	 
572	###案例1：监控时尚博主的每日穿搭
573	 
574	**需求：**每天早上9点检查博主是否发布新搭搭
575	 
576	**配置：**
577	``` json
578	{
579	    "cookie" : "你的cookie" , 
580	    "user_id" : "博主的user_id" , 
581	    "download_dir" : "./fashion_daily" , 
582	    "check_interval" : 3600 , 
583	    "use_headless" : true , 
584	    “max_retries” ：3 ， 
585	    "retry_delay" : 2 , 
586	    "downloaded_notes_file" : "fashion_downloaded.json" 
587	}
588	```
589	 
590	**运行方式：**
591	 
592	使用Cron定时任务：
593	``` bash
594	# 编辑crontab
595	crontab -e
596	
597	#添加任务：每天早上9点执行
598	0 9 * * * cd /path/to/xhs/example && python monitor_user_notes.py --once --config fashion_config.json 
599	```
600	 
601	###案例2：监控多个美食博主
602	 
603	**需求：**同时监控5个美食博主，发现新笔记就下载
604	 
605	**方案：**创建多个配置文件，使用进程管理工具运行
606	 
607	**步骤：**
608	 
609	1.创建配置文件：
610	   -  `food_blogger1.json`
611	   -  `food_blogger2.json`
612	   -  `food_blogger3.json`
613	   -  `food_blogger4.json`
614	   -  `food_blogger5.json`
615	 
616	2.创建启动脚本`start_multi_monitor.sh`：
617	 
618	``` bash
619	/bin/bash
620	
621	# 后台运行多个监控实例
622	python monitor_user_notes.py --config food_blogger1.json > logs/blogger1.log 2 > &1 & 
623	python monitor_user_notes.py --config food_blogger2.json > logs/blogger2.log 2 > &1 & 
624	python monitor_user_notes.py --config food_blogger3.json > logs/blogger3.log 2 > &1 & 
625	python monitor_user_notes.py --config food_blogger4.json > logs/blogger4.log 2 > &1 & 
626	python monitor_user_notes.py --config food_blogger5.json > logs/blogger5.log 2 > &1 & 
627	
628	echo "所有监控已启动" 
629	```
630	 
631	3.创建停止脚本`stop_multi_monitor.sh`：
632	 
633	``` bash
634	/bin/bash
635	
636	#停止所有监控进程
637	pkill -f "monitor_user_notes.py"
638	
639	echo "所有监控已停止" 
640	```
641	 
642	4.运行：
643	 
644	``` bash
645	chmod +x start_multi_monitor.sh
646	chmod +x stop_multi_monitor.sh
647	
648	./start_multi_monitor.sh
649	```
650	 
651	###案例3：构建个人笔记数据库
652	 
653	**需求：**定期备份喜欢的博主的所有笔记，用于个人收藏
654	 
655	**方案：**使用单次检查模式 + 数据库存储
656	 
657	**代码示例：**
658	 
659	``` python
660	导入sqlite3
661	导入json
662	from monitor_user_notes import NoteMonitor
663	
664	# 初始化数据库
665	conn = sqlite3.connect ( ' notes.db ' )
666	cursor = conn.cursor ( )​​
667	
668	cursor.execute ( ' ' '
669	CREATE TABLE IF NOT EXISTS notes (
670	    note_id 文本主键，
671	    标题文本，
672	    描述文本，
673	    输入文本，
674	    用户 ID 文本，
675	    昵称文本，
676	    liked_count 整数，
677	    collected_count 整数，
678	    comment_count 整数，
679	    下载时间文本，
680	    文件路径文本
681	）
682	''' ）
683	
684	# 运行监控
685	monitor = NoteMonitor ( 'config.json' )
686	monitor.run_once ( )​​
687	
688	# 将下载的笔记信息存入数据库
689	with open ( 'downloaded_notes.json' , 'r' ) as f :   
690	    data = json.load ( f )​​
691	
692	对于data [ 'notes_metadata' ] . items ( )中的每个 note_id和metadata ：
693	    cursor.execute ( ' ' '
694	    INSERT OR REPLACE INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
695	    ''' ，（ 
696	        note_id ，
697	        metadata.get ( ' title ' ) ,
698	        # ...其他字段
699	    ））
700	
701	conn.commit ( )​​
702	conn.close ( )​​
703	```
704	 
705	###案例4：实时通知新笔记
706	 
707	**需求：**博主发布新笔记时，立即发送微信/邮件通知
708	 
709	**方案：**在监控脚本中添加通知功能
710	 
711	**修改monitor_user_notes.py：**
712	 
713	在`check_new_notes`方法中添加：
714	 
715	``` python
716	def send_notification ( self , new_notes ) : 
717	    """发送通知"""
718	    message = f"发现{ len ( new_notes ) }条新笔记！\n\n" 
719	    
720	    new_notes中的注释[ : 5 ] : # 只显示前 5 条  
721	        message += f"- { note .get ( 'display_title' , '无标题' ) } \n"  
722	    
723	    # 方式1：发送邮件
724	    self.send_email ( message )​​
725	    
726	    #方式2：发送到服务器酱（微信通知）
727	    self.send_serverchan ( message )​​
728	    
729	    # 方式3：发送到Telegram
730	    self.send_telegram ( message )​​
731	
732	def send_email ( self , message ) : 
733	    导入smtplib
734	    从电子邮件.mime.text导入MIMEText​​​
735	    
736	    msg = MIMEText ( message )
737	    msg [ 'Subject' ] = '小红书新笔记通知'  
738	    msg [ 'From' ] = 'your@email.com'  
739	    msg [ 'To' ] = 'to@email.com'  
740	    
741	    smtp = smtplib.SMTP ( ' smtp.gmail.com ' , 587 ) 
742	    smtp.starttls ( )​​
743	    smtp.login ( 'your@email.com' , ' password ' ) 
744	    smtp.send_message ( msg )​​
745	    smtp.quit ( )​​
746	
747	def send_serverchan ( self , message ) : 
748	    导入请求
749	    
750	    sckey = "你的ServerChan钥匙" 
751	    url = f"https://sctapi.ftqq.com/ { sckey } .send" 
752	    
753	    requests.post ( url , data = {​​
754	        "title" : "小红书新笔记" , 
755	        “desp” ：消息
756	    } )
757	```
758	 
759	然后在`check_new_notes`中调用：
760	 
761	``` python
762	如果new_notes ：
763	    print ( f"\n🎉 发现{ len ( new_notes ) }条新笔记！" )
764	    自己。 send_notification ( new_notes ) # 发送通知  
765	    # ... 下载笔记
766	```
767	 
768	---
769	 
770	##疑难解答
771	 
772	###问题1：签名失败
773	 
774	**错误信息：**
775	```
776	window._webmsxyw 不是一个函数
777	```
778	 
779	**可能原因：**
780	1.剧作家未正确安装
781	2.网页加载太慢
782	3.网站更新了签名机制
783	 
784	**解决方法：**
785	 
786	**方法1：**增加等待时间
787	``` python
788	# 在符号函数中
789	sleep ( 3 ) #从1秒增加到3秒  
790	```
791	 
792	**方法2：**使用可见浏览器调试
793	``` json
794	{
795	    "use_headless" : false 
796	}
797	```
798	 
799	**方法3：**重新安装Playwright
800	``` bash
801	pip uninstall playwright
802	pip install playwright
803	剧作家安装Chromium
804	```
805	 
806	**方法4：**检查网络连接
807	``` bash
808	ping www.xiaohongshu.com
809	```
810	 
811	###问题2：Cookie失效
812	 
813	**错误信息：**
814	```
815	需要登录
816	未授权访问
817	```
818	 
819	**解决方法：**
820	 
821	1.重新获取Cookie
822	2.确保Cookie完整（包含a1、webId等）
823	3.检查账号是否被限制
824	 
825	**预防措施：**
826	-定期更新Cookie（建议每周一次）
827	-不要在多个设备同时使用相同账号
828	-避免腹部请求
829	 
830	###问题3：下载失败
831	 
832	**错误信息：**
833	```
834	下载文件失败
835	网络错误
836	```
837	 
838	**可能原因：**
839	1.网络不稳定
840	2.CDN访问设置
841	3.文件已被删除
842	 
843	**解决方法：**
844	 
845	**方法一：**使用代理
846	``` python
847	xhs_client = XhsClient (
848	    cookie = cookie ，
849	    符号=符号，
850	    代理= {
851	        'http' : 'http://proxy:port' , 
852	        'https' : 'http://proxy:port' 
853	    }
854	）
855	```
856	 
857	**方法2：**增加重试
858	``` json
859	{
860	    “max_retries” ：5 ， 
861	    "retry_delay" ：5 
862	}
863	```
864	 
865	**方法3：**查看网络
866	``` bash
867	curl -I https://sns-img-qc.xhscdn.com
868	```
869	 
870	###问题4：内存占用过高
871	 
872	**现象：**长时间运行后内存占用越来越高
873	 
874	**原因：**浏览器实例正确未关闭
875	 
876	**解决方法：**
877	 
878	确定在符号函数中关闭浏览器：
879	 
880	``` python
881	def sign ( self , uri , data = None , a1 = "" , web_session = "" ) : 
882	    with sync_playwright ( ) as playwright : 
883	        browser = playwright.chromium.launch ( headless = True )​​​​
884	        尝试：
885	            # ...签名逻辑
886	            返回结果
887	        最后：
888	            浏览器。 close ( ) #确保关闭  
889	```
890	 
891	###问题5：磁盘空间不足
892	 
893	**原因：**下载的视频文件占用大量空间
894	 
895	**解决方法：**
896	 
897	**方法一：**定期清理
898	``` bash
899	#删除30天前的笔记
900	查找./downloads -type d -mtime +30 -exec rm -rf { } \ ; 
901	```
902	 
903	**方法2：**只下载图片
904	``` python
905	# 修改代码，跳过视频
906	如果note_type == "video" : 
907	    print ( "跳过视频笔记" )
908	    返回
909	```
910	 
911	**方法3：**使用压缩
912	``` bash
913	# 压缩下载的图片
914	查找./downloads -name "*.png" -exec convert { } -quality 85 { } \ ;  
915	```
916	 
917	###问题6：被检测为机器人
918	 
919	**错误信息：**
920	```
921	需要验证
922	滑动验证
923	```
924	 
925	**原因：**请求频率过高或行为异常
926	 
927	**解决方法：**
928	 
929	1.降低检查频率
930	``` json
931	{
932	    "check_interval" : 600   # 增加到10分钟 
933	}
934	```
935	 
936	2.使用stealth.js
937	``` json
938	{
939	    "stealth_js_path" : "./stealth.min.js" 
940	}
941	```
942	 
943	3.添加随机延迟
944	``` python
945	随机导入
946	time.sleep ( random.uniform ( 1 , 3 ) )​​​​ 
947	```
948	 
949	4.使用住宅代理IP
950	 
951	5.等待一段时间（24小时）后重试
952	 
953	###问题7：找不到用户笔记
954	 
955	**错误信息：**
956	```
957	用户笔记为空
958	未找到笔记
959	```
960	 
961	**可能原因：**
962	1.用户ID错误
963	2.用户设置了隐私
964	3.用户未发布笔记
965	 
966	**解决方法：**
967	 
968	1.验证用户ID
969	``` python
970	user_info = client.get_user_info ( user_id )​​
971	print ( user_info )
972	```
973	 
974	2.检查用户主页是否可访问
975	 
976	3.确认是否需要关注后才能看
977	 
978	###问题8：程序意外退出
979	 
980	**原因分析：**
981	-异常未捕获
982	-系统资源不足
983	-网络长时间中断
984	 
985	**解决方法：**
986	 
987	使用进程监控工具：
988	 
989	** Linux - systemd：**
990	 
991	创建`/etc/systemd/system/xhs-monitor.service`：
992	 
993	``` ini
994	[单元]
995	描述= XHS 音符监视器
996	之后=网络.目标
997	
998	[服务]
999	类型=简单
1000	用户=您的用户名
1001	工作目录= /path/to/xhs/example
1002	ExecStart = /usr/bin/python3 monitor_user_notes.py
1003	重启=始终
1004	重启秒数= 10
1005	
1006	[安装]
1007	WantedBy =多用户目标
1008	```
1009	 
1010	启动：
1011	``` bash
1012	sudo systemctl enable xhs-monitor
1013	sudo systemctl start xhs-monitor
1014	sudo systemctl status xhs-monitor
1015	```
1016	 
1017	** Linux - 管理员：**
1018	 
1019	``` ini
1020	[程序:xhs-monitor ]
1021	命令= python monitor_user_notes.py
1022	目录= /path/to/xhs/example
1023	自动启动=真
1024	自动重启= true
1025	```
1026	 
1027	** Windows - NSSM：**
1028	 
1029	``` bash
1030	nssm install xhs-monitor "C:\Python\python.exe" "C:\path \ to\monitor_user_notes.py" 
1031	nssm 启动 xhs-monitor
1032	```
1033	 
1034	---
1035	 
1036	##高级技巧
1037	 
1038	### 1.性能优化
1039	 
1040	**系数下载：**
1041	 
1042	``` python
1043	from concurrent.futures import ThreadPoolExecutor​​
1044	
1045	def download_notes_concurrent ( self , notes ) : 
1046	    使用ThreadPoolExecutor （ max_workers = 3 ）作为执行器： 
1047	        executor.map ( self.download_note , notes )​​​​
1048	```
1049	 
1050	**缓存机制：**
1051	 
1052	``` python
1053	从functools导入lru_cache
1054	
1055	@lru_cache （ maxsize = 1000 ）
1056	def get_note_cached ( self , note_id ) : 
1057	    返回self.xhs_client.get_note_by_id ( note_id )​​​​
1058	```
1059	 
1060	### 2.数据分析
1061	 
1062	**统计笔记数据：**
1063	 
1064	``` python
1065	将Pandas导入为pd
1066	导入json
1067	
1068	#读取元数据
1069	with open ( 'downloaded_notes.json' , 'r' ) as f :   
1070	    data = json.load ( f )​​
1071	
1072	# 转换为DataFrame
1073	df = pd.DataFrame ( data [ ' notes_metadata ' ] . values ( ) )
1074	
1075	# 分析
1076	print ( df [ 'type' ] . value_counts ( ) ) # 笔记类型分布  
1077	print ( df . groupby ( 'type' ) . size ( ) ) # 按类型统计  
1078	```
1079	 
1080	### 3.云端部署
1081	 
1082	**部署到云服务器：**
1083	 
1084	``` bash
1085	# 1.连接服务器
1086	ssh user@your-server.com
1087	
1088	# 2.安装依赖
1089	pip install xhs playwright
1090	剧作家安装Chromium
1091	
1092	# 3. 上传代码
1093	scp -r xhs user@your-server.com:~/
1094	
1095	# 4.后台运行
1096	nohup python monitor_user_notes.py > monitor.log 2 > &1 & 
1097	```
1098	 
1099	### 4.自动化运维
1100	 
1101	**日志监控：**
1102	 
1103	``` python
1104	导入日志
1105	
1106	日志记录.基本配置(
1107	    文件名= 'monitor.log' ,
1108	    级别=日志记录.信息,
1109	    format = '%(asctime)s - %(levelname)s - %(message)s'
1110	）
1111	
1112	logger = logging.getLogger ( __ name__ )​
1113	记录器。信息（“开始监控” ）
1114	```
1115	 
1116	**错误补充：**
1117	 
1118	``` python
1119	def alert_on_error ( func ) : 
1120	    def wrapper ( * args , ** kwargs ) :  
1121	        尝试：
1122	            返回func ( * args , ** kwargs ) 
1123	        异常处理e ：​
1124	            send_alert ( f" 错误: { e } " )
1125	            增加
1126	    返回包装器
1127	```
1128	 
1129	---
1130	 
1131	##总结
1132	 
1133	通过本教程，你应该能够：
1134	 
1135	✅ 理解xhs项目的基本原理  
1136	✅ 成功配置和运行笔记监控工具  
1137	✅ 解决常见问题  
1138	✅ 根据需求定制功能  
1139	 
1140	**下一步建议：**
1141	 
1142	1.阅读[ API文档]( https://reajason.github.io/xhs/ )了解更多功能
1143	2.查看[来源代码]( https://github.com/ReaJason/xhs )学习实现细节
1144	3.加入社区讨论和交流经验
1145	 
1146	**注意事项：**
1147	 
1148	⚠️请遵守法律法规和网站使用条款  
1149	⚠️ 合理的控制请求频率  
1150	⚠️ 尊重内容创作者版权  
1151	⚠️儿童学习和个人使用  
1152	 
1153	祝使用愉快！🎉
