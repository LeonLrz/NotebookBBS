# 1. 项目架构介绍
## 1.1 apps包
包含front前台/cms后台/common公共包，以及额外的模块
1.1.1 cms包
1. `decorators.py` 后台用装饰器
	1. `login_required` 登陆限制装饰器
	2. `permission_required` 后台管理权限限制装饰器
2. `forms.py` 后台使用表单
	1. `LoginForm`
	2. `ResetpwdForm`
	3. `ResetEmailForm`
	4. `AddBannerForm`
	5. `UpdateBannerForm`
	6. `AddBoardForm`
	7. `UpdateBoardForm`
3. `hooks.py`后台使用的钩子函数
	1. `before_request`
	2. `cms_context_processor`
4. `models.py`
	`CMSPermission`
	`CMSRole`
	`CMSUser`

5. `views.py` 视图函数或方法类视图，以url标识
	`/cms/`
	`/cms/login/`<-`LoginView`
	
	

### 1.1.2 common包

### 1.1.3 front包
decorators.py（前台常用装饰器），forms（前台常用表单）

### 1.1.4 ueditor包

### 1.1.5 其余py文件


#### 1.1.5.1 forms.py

#### 1.1.5.2 models.py

## 1.2 static文件

## 1.3 templates模板

## 1.4 utils包

# 2. 主要接口

