from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from server.db_manager import db_manager
from server.models.user_model import User
from server.utils.auth_utils import AuthUtils
from server.utils.auth_middleware import get_db, get_current_user, oauth2_scheme
from server.utils.common_utils import log_operation

# 创建路由器
auth = APIRouter(prefix="/auth", tags=["authentication"])

# 请求和响应模型
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: str
    last_login: str | None = None

class InitializeAdmin(BaseModel):
    username: str
    password: str

# 路由：登录获取令牌
@auth.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()

    # 验证用户存在且密码正确
    if not user or not AuthUtils.verify_password(user.password_hash, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 更新最后登录时间
    user.last_login = datetime.now()
    db.commit()

    # 生成访问令牌
    token_data = {"sub": str(user.id)}
    access_token = AuthUtils.create_access_token(token_data)

    # 记录登录操作
    log_operation(db, user.id, "登录")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }

# 路由：校验是否需要初始化管理员
@auth.get("/check-first-run")
async def check_first_run():
    is_first_run = db_manager.check_first_run()
    return {"first_run": is_first_run}

# 路由：初始化管理员账户
@auth.post("/initialize", response_model=Token)
async def initialize_admin(
    admin_data: InitializeAdmin,
    db: Session = Depends(get_db)
):
    # 检查是否是首次运行
    if not db_manager.check_first_run():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="系统已经初始化，无法再次创建初始管理员",
        )

    # 创建管理员账户
    hashed_password = AuthUtils.hash_password(admin_data.password)

    new_admin = User(
        username=admin_data.username,
        password_hash=hashed_password,
        role="superadmin",
        last_login=datetime.now()
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    # 生成访问令牌
    token_data = {"sub": str(new_admin.id)}
    access_token = AuthUtils.create_access_token(token_data)

    # 记录操作
    log_operation(db, new_admin.id, "系统初始化", "创建超级管理员账户")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": new_admin.id,
        "username": new_admin.username,
        "role": new_admin.role
    }

# 路由：获取当前用户信息
@auth.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user.to_dict()
