# 1、創建虛擬環境 & 安裝依賴

```shell
# 創建虛擬環境
python -m venv venv

# 激活虛擬環境（Windows 用 venv\Scripts\activate）
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 如果有導入新的包，執行以下命令進行依賴更新
pip freeze > requirements.txt
```

# 2、數據庫遷移 & 初始化

```shell
# authentication是app名稱
python manage.py makemigrations authentication

python manage.py migrate
```

# 3、啓動服務

```shell
# 默认是8000
DJANGO_ENV=prod python manage.py runserver 8088
```

# 4、Pycharm中啓動調試

![image-20250514100736551](D:\company\project\his\surgery\assets\image-20250514100736551.png)

# 5、整體調用流程

瀏覽器請求 /auth/login
         ↓
主路由（surgery/urls.py）
         ↓
子路由 include('authentication.urls')
         ↓
匹配 path('login', views.LoginView.as_view())
         ↓
執行 LoginView 的 post 方法
         ↓
返回 HttpResponse 或 JsonResponse
         ↓
瀏覽器收到響應

# 6、注意點

- 類試圖必須用`.as_view()`
- 函数视图不能用 `.as_view()`，直接函数名
- path()函數會自動忽略開頭的`/`，会精确匹配末尾是否带 `/`
- `name='xxx'` 用于 URL 反向解析，例如：`reverse('login')`

# 7、权限验证

```python
@method_decorator(permission_required('user:list'), name='dispatch')
class UserListView(APIView):
    # 不让 DRF 管，自己用装饰器判断，不要和 DRF 默认的 permission_classes 混用
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return success_response(user_serializer.data)
```

