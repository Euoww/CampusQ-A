

# 项目结构

```cssharp
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
│   │   └── templates/user/
│   │       └── login.html 等
│   │
│   ├── question/
│   ├── answer/
│   ├── comment/
│   ├── tag/
│   └── notification/
│
├── templates/                # 全局模板
│   └── base.html
│
├── static/                   # 静态资源目录
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── media/                    # 用户上传文件，如头像
│
├── manage.py
└── requirements.txt          # 项目依赖（可选）
```# CampusQ-A
