# 需求分析

## 一、功能需求

本系统主要面向在校师生，提供在线提问、回答、互动交流的平台。主要功能包括：

1. **用户模块**
   - 用户注册、登录、登出（支持邮箱或学号注册）
   - 用户个人资料管理（头像、昵称、简介、专业年级等）
   - 忘记密码与密码修改功能
2. **问题管理模块**
   - 用户发布问题（标题、正文、添加标签）
   - 用户浏览问题列表，支持按时间、热度、标签筛选
   - 查看问题详情，包含回答、评论列表
   - 编辑、删除自己发布的问题
   - 支持问题匿名发布
3. **回答管理模块**
   - 用户对问题进行回答
   - 支持回答的点赞、评论
   - 问题发布者可以采纳最佳回答
   - 用户可以删除自己的回答
4. **标签管理模块**
   - 提问时可选择已有标签或新建标签
   - 支持按标签分类浏览问题
5. **互动与通知模块**
   - 点赞提醒、回答通知、评论通知
   - 我的提问/我的回答列表页
6. **搜索功能模块**
   - 支持关键词搜索问题标题与正文
   - 支持根据标签筛选问题
7. **积分与等级系统（可选）**
   - 用户通过提问、回答、被点赞等获得积分
   - 根据积分提升等级，激励活跃度
8. **后台管理模块**
   - 管理员可以管理用户、问题、回答、举报信息
   - 支持审核、删除违规内容


## 二、非功能需求

- **系统可用性**
  - 系统应支持至少 500 名同时在线用户的基本访问需求。
- **响应速度**
  - 页面加载时间控制在 3 秒以内，常用操作响应时间小于 1 秒。
- **安全性**
  - 防止 SQL 注入、XSS 攻击，密码加密存储。
  - 用户数据保护，匿名提问时隐藏用户身份信息。
- **扩展性**
  - 系统模块设计应具备良好的可扩展性，以支持未来增加如课程答疑、资料共享等新功能。
- **兼容性**
  - 支持主流浏览器访问，兼容移动端显示（响应式布局）。

# 核心数据表设计

1. **用户表（User）**
    （可以用 Django 自带的 `AbstractUser` 扩展）

- id（主键）
- username（用户名）
- email（邮箱）
- password（密码）
- avatar（头像）
- bio（个人简介）
- major（专业）
- grade（年级）
- is_active（是否激活）
- date_joined（注册时间）
- score（积分，用于积分系统，可选）

1. **问题表（Question）**

- id（主键）
- author（外键 -> User）
- title（标题）
- content（正文，支持富文本）
- is_anonymous（是否匿名发布）
- created_at（创建时间）
- updated_at（更新时间）
- view_count（浏览次数）
- like_count（点赞数量）

1. **回答表（Answer）**

- id（主键）
- question（外键 -> Question）
- author（外键 -> User）
- content（回答正文）
- is_accepted（是否被采纳）
- created_at（创建时间）
- updated_at（更新时间）
- like_count（点赞数量）

1. **评论表（Comment）**
    （问题和回答都可以有评论，所以需要一个通用的 Comment）

- id（主键）
- content_type（指向是评论的问题还是回答，用 Django 的 ContentType）
- object_id（对应问题ID或回答ID）
- author（外键 -> User）
- content（评论内容）
- created_at（创建时间）

1. **标签表（Tag）**

- id（主键）
- name（标签名）
- created_at（创建时间）

1. **问题与标签的关联表（QuestionTag）**

- id（主键）
- question（外键 -> Question）
- tag（外键 -> Tag）

1. **通知表（Notification）**

- id（主键）
- receiver（外键 -> User）
- sender（外键 -> User，谁触发的）
- content（通知内容，比如：“你的问题有了新回答”）
- is_read（是否已读）
- created_at（创建时间）

------

# 实体关系（ER关系）

- 一个用户可以发布多个问题（User — 1:N — Question）
- 一个问题可以有多个回答（Question — 1:N — Answer）
- 一个问题可以有多个标签（Question — N:M — Tag）
- 一个回答只能属于一个问题
- 一个用户可以给问题或回答点赞（这个可以额外加一个 Like 表）
- 一个用户可以收到多条通知



在咱们这个校园问答系统中，ER图核心是围绕着：**用户**、**问题**、**回答**、**标签**、**评论**、**通知**展开的。

------

```
[User] ——<发布>—— [Question] ——<关联>—— [Tag]
   |                    |
   |                    └——<拥有>—— [Answer]
   |                                   |
   |                                   └——<拥有>—— [Comment]
   |
   └——<发布>—— [Comment]

[User] ——<触发>—— [Notification]
```

### 1. User 用户表

| 字段        | 类型   | 说明         |
| ----------- | ------ | ------------ |
| id          | 主键   | 自动生成     |
| username    | 字符串 | 用户名       |
| email       | 字符串 | 邮箱         |
| password    | 字符串 | 密码（哈希） |
| avatar      | 图片   | 头像         |
| bio         | 文本   | 简介         |
| major       | 字符串 | 专业         |
| grade       | 字符串 | 年级         |
| score       | 整数   | 积分         |
| date_joined | 时间   | 注册时间     |

### 2. Question 问题表

| 字段         | 类型         | 说明     |
| ------------ | ------------ | -------- |
| id           | 主键         |          |
| title        | 字符串       | 问题标题 |
| content      | 富文本       | 问题内容 |
| is_anonymous | 布尔         | 是否匿名 |
| author_id    | 外键 -> User | 提问者   |
| created_at   | 时间         | 创建时间 |
| updated_at   | 时间         | 更新时间 |
| view_count   | 整数         | 浏览次数 |
| like_count   | 整数         | 点赞数   |

### 3. Answer 回答表

| 字段        | 类型             | 说明       |
| ----------- | ---------------- | ---------- |
| id          | 主键             |            |
| question_id | 外键 -> Question | 所属问题   |
| author_id   | 外键 -> User     | 回答者     |
| content     | 富文本           | 回答内容   |
| is_accepted | 布尔             | 是否被采纳 |
| created_at  | 时间             | 创建时间   |
| updated_at  | 时间             | 更新时间   |
| like_count  | 整数             | 点赞数     |

### 4. Tag 标签表

| 字段       | 类型   | 说明     |
| ---------- | ------ | -------- |
| id         | 主键   |          |
| name       | 字符串 | 标签名   |
| created_at | 时间   | 创建时间 |

### 5. QuestionTag 问题与标签关联表

| 字段        | 类型             | 说明 |
| ----------- | ---------------- | ---- |
| id          | 主键             |      |
| question_id | 外键 -> Question |      |
| tag_id      | 外键 -> Tag      |      |

### 6. Comment 评论表

| 字段         | 类型         | 说明             |
| ------------ | ------------ | ---------------- |
| id           | 主键         |                  |
| content_type | ContentType  | 关联到问题或回答 |
| object_id    | 整数         | 关联ID           |
| author_id    | 外键 -> User | 评论者           |
| content      | 文本         | 评论内容         |
| created_at   | 时间         | 创建时间         |

### 7. Notification 通知表

| 字段        | 类型         | 说明       |
| ----------- | ------------ | ---------- |
| id          | 主键         |            |
| receiver_id | 外键 -> User | 通知接收者 |
| sender_id   | 外键 -> User | 通知发起者 |
| content     | 文本         | 通知内容   |
| is_read     | 布尔         | 是否已读   |
| created_at  | 时间         | 创建时间   |





# 项目结构

```csharp
campusqa/                      # PyCharm 创建的根目录
│
├── campusqa/                 # 主配置目录（settings.py / urls.py）
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                     # 所有子功能模块 app
│   ├── user/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── question/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── answer/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│   │
│   ├── comment/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
    
│   ├── tag/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
    
│   └── notification/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── apps.py
│
├── templates/                # 全局模板
│   └── base.html
│
├── static/                   # 静态资源目录
│   ├── css/
│   │   └── style.css
│   └── images/
│   │   └── default_avatar.png
│
├── media/                    # 用户上传文件，如头像
│   ├── avatars/
│
├── manage.py
└── requirements.txt          # 项目依赖

```

