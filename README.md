# cambridge-education-interview

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
> touch .env (可參考.env.example)
```

#### 4. 執行docker-compose （請確保本機端83 port未被使用）
```
> docker-compose up -d
```

#### 5. 開啟瀏覽器
```
http://localhost:83/__hiddenswagger/
```

## 透過Swagger操作API:
```
1. 透過Swagger可直接對API進行操作。
    －  新增帳號（已有帳號可略過） POST /account/ -> 取得 Access Token

2. 在介面上找到 Authorize
    －  點擊 Authorize
    －  輸入取得Access Token
        >  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
3. 可開始更改帳號資料
```

## 取得Access Token (登入)
```
    1. 透過Swagger輸入符合格式的電話及密碼。
        POST /token/
        {
            "phone": "0912-345-678", 
            "password": "123456"
        }
```
## 
```

```

