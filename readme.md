## 项目介绍
本项目是一个用于容量管理和动态阈值报警的可视化界面(Capacity management and dynamic threshold alarm visualization interface)。

## 项目成员
宋雨健
李嘉乐
刘勇兵

## 项目部署
```

$ cd template-django-vue
$ cd template-django-vue-main
```


$ npm install

$ python -m venv venv


# On windows
$ .\venv\Scripts\Activate.ps1

# On linux
$ source venv/bin/activate

$ pip install -r requirements.txt

$ python manage.py migrate

## 运行
$ npm run dev

$ python manage.py runserver
```

## urls
http://localhost:5173/#/ for vue frontend
http://localhost:8000/api/ for django rest framework api
http://localhost:8000/api/admin/ for django admin




