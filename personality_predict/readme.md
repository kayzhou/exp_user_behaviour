## 大五性格预测器

- 程序环境：python>=3.5
- 依赖：pip install -r requirements.txt


- 输入：用户微博特征文件

- 输出：外倾性分类（ext_label）

       -1，0，1，-1 > 内向，0 > 中性，1 > 外向；

       及大五人格分数（0-60，分数越高在该性格倾向上表现更强烈），分别为neuroticism，extraversion，openness，agreeableness，conscientiousness

---

user_data.txt 输入文件：用户微博特征文件

一行一条微博，json格式

- 输入示例：

{

    "nickname": "刘丽", // 昵称

    "followers_count": 34972.0, // 粉丝数

    "text": "我在#秒拍#等你，来看我直播吧，别让我等太久。http://t.cn/R4oxCoT", // 具体微博内容

    "publish_dt": "2016-01-07T17:46:49", // 发布时间

    "gender": "f" // 性别，f为女，m为男

}

- 输出示例：{'ext_label': -1, 'neu_score': 34, 'ext_score': 30, 'ope_score': 38, 'agr_score': 33, 'con_score': 35}


---
requirements.txt    请先安装必要的工具

test.py             使用示例

psy_predict.py      预测器

feature_handler.py  特征提取工具


data/               数据

    | user_data.txt 数据实例，可使用psy_predict直接进行预测

    | keywords.txt  文本关键词特征

model/              模型文件