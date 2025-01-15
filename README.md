# cambridge-education-interview

- [前言](#前言)
- [使用工具](#使用工具)
- [使用方式](#使用方式)
- [透過Swagger操作API](#透過Swagger操作API)
- [Kibana登入](#Kibana登入)
- [停止容器](#停止容器)

## 前言
```
    針對需求，建立了一個專案，使用Django實作了帳號系統及配對系統。並使用Elasticsearch實作聊天室系統。 因時間有限並未對程式碼及DB設計進行優化。
```
## 使用工具
```
    Python 3.8
    Django 3.2
    Elasticsearch 7.13.4
    Kibana 7.13.4
    MySQL 8.0
    Docker 20.10.12
```

## 使用方式 :

#### 1. 下載專案
```
> git clone https://github.com/Neil0406/cambridge-education-interview.git
```
#### 2. 移動至專案資料夾內
```
> cd cambridge-education-interview
```

#### 3. 新增.env檔案
```
> vi .env (可參考.env.example)
```

#### 4. 執行docker-compose （請確保本機端83 port未被使用）
```
> docker-compose up --build
```

#### 5. 開啟瀏覽器
```
http://localhost:83/__hiddenswagger/
```

## 透過Swagger操作API:
```
＊＊＊第一次啟動後已建立第一組帳號＊＊＊ 
帳號：DJANGO_SUPERUSER_PHONE (.env)
密碼：DJANGO_SUPERUSER_PASSWORD (.env)

1. 取得Access Token
    POST /token/
    {
        "phone": "0912-345-678", 
        "password": "123456"
    }
2. 在介面上找到 Authorize
    －  點擊 Authorize
    －  輸入取得Access Token
        >  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

3. 由swagger建立假資料
    POST /account/es_mapping/
    POST /account/fakeuser/

4. 可開始更改帳號資料及使用API
    PUT /account/user/
    ＊＊＊已將預設值寫入JSON範例＊＊＊
    請勿變更： latitude / longitude / hobby / interest，否則可能導致配對找不到資料。
```

## Kibana登入
```
    1. 可透過Kibana來觀看及統計相關數據。
    2. URL : http://localhost:5601
        - 帳號 ELASTICSEARCH_USERNAME  (.env)
        - 密碼 ELASTICSEARCH_PASSWORD  (.env)
    3. 須先建立 Index Patterns 
```

## 停止容器
```
> docker-compose down
```



