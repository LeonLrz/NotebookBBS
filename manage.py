from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from notebook_bbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_moedels
from apps.models import BannerModel,BoardModel,PostModel,HighlightPostModel,CommentModel


CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_moedels.FrontUser
LaptopInfo = front_moedels.LaptopInfo

app = create_app()

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command("db",MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


@manager.command
def create_role():
    # 1.访问者
    visitor = CMSRole(name='访问者',desc='只能访问相关数据，不能修改。')
    visitor.permissions = CMSPermission.VISITOR

    # 2.运营角色（可以修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc='管理帖子，管理评论，管理前台用户。')
    operator.permissions = (CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER)

    # 3.管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.CMSUSER|CMSPermission.BOARDER

    # 4.开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator,admin, developer])
    db.session.commit()


@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户角色添加成功！")
        else:
            print("没有这个角色：%s"%name)
    else:
        print("没有使用该邮箱%s的用户"%email)


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print("前台用户添加成功")


@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print("有访问者权限")
    else:
        print("无访问者权限")

@manager.command
def create_test_post():
    for x in range(1,24):
        name = "华为笔记本"
        title = name+str(x)
        content = name + str(x)
        board_id = BoardModel.query.filter_by(name=name).first().id
        board = BoardModel.query.filter_by(id=board_id).first()
        author = FrontUser.query.first()
        post = PostModel(title=title,content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print("恭喜测试帖子添加成功")

@manager.command
def test_laptop():
    notebooks = LaptopInfo.query.all()
    for notebook in notebooks:
        print(notebook.laptop_model)

if __name__ == "__main__":
    manager.run()
