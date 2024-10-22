from fastapi import APIRouter, HTTPException, Depends
from psycopg2.extensions import connection
import shortuuid

from . import config
from . import schemas
from . import services
from .error import ErrorResponse


router = APIRouter()


# ランダムなユーザーIDを8桁で生成
def generate_user_id():
    return shortuuid.ShortUUID().random(length=8)


# --------------------------------------
# 新規ユーザーを作成
# --------------------------------------
@router.post("/api/admin/create_user")
def create_user(
    request: schemas.UserCreate,
    db_conn: connection = Depends(services.get_conn),
) -> schemas.UserData:

    # パスワード認証
    if not services.verify_password(request.password):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.PASSWORD_INCORRECT
        )

    user_handle = services.UserService(db_conn)

    # ランダムなユーザーIDを生成
    user_id = generate_user_id()

    user_handle.create_user(user_id, config.INITIAL_BALANCE)

    response = user_handle.get_data(user_id)

    # ユーザーIDが存在しなければエラー
    if response is None:
        raise HTTPException(
            status_code=400, detail=ErrorResponse.USER_CREATION_FAILED
        )

    return response


# --------------------------------------
# ユーザーを削除
# --------------------------------------
@router.post("/api/admin/delete_user")
def delete_user(
    request: schemas.UserDelete,
    db_conn: connection = Depends(services.get_conn),
):

    # パスワード認証
    if not services.verify_password(request.password):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.PASSWORD_INCORRECT
        )

    user_handle = services.UserService(db_conn)

    # ユーザーIDが存在しなければエラー
    if not user_handle.is_user_exists(request.user_id):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.USER_NOT_FOUND
        )

    user_handle.delete_user(request.user_id)


# --------------------------------------
# 残高を取得
# --------------------------------------
@router.post("/api/admin/get_balance")
def get_balance(
    request: schemas.GetBalance,
    db_conn: connection = Depends(services.get_conn),
):

    # パスワード認証
    if not services.verify_password(request.password):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.PASSWORD_INCORRECT
        )

    user_handle = services.UserService(db_conn)

    response = user_handle.get_data(request.user_id)

    # ユーザーIDが存在しなければエラー
    if response is None:
        raise HTTPException(
            status_code=400, detail=ErrorResponse.USER_NOT_FOUND
        )

    return response


# --------------------------------------
# 残高を設定
# --------------------------------------
@router.post("/api/admin/set_balance")
def set_balance(
    request: schemas.SetBalance,
    db_conn: connection = Depends(services.get_conn),
):

    # パスワード認証
    if not services.verify_password(request.password):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.PASSWORD_INCORRECT
        )

    user_handle = services.UserService(db_conn)

    # ユーザーIDが存在しなければエラー
    if not user_handle.is_user_exists(request.user_id):
        raise HTTPException(
            status_code=400, detail=ErrorResponse.USER_NOT_FOUND
        )

    user_handle.set_balance(request.user_id, request.balance)

    return user_handle.get_data(request.user_id)


# --------------------------------------
# 管理者パスワードを認証
# --------------------------------------
@router.post("/api/admin/verify_password")
def verify_password(request: schemas.VerifyPassword):

    if services.verify_password(request.password):
        return {"success": True}
    else:
        return {"success": False}


# --------------------------------------
# 残高を同期
# --------------------------------------
@router.get("/api/user/sync/{user_id}")
def sync_data(
    user_id: str,
    db_conn: connection = Depends(services.get_conn),
):
    user_handle = services.UserService(db_conn)

    response = user_handle.get_data(user_id)

    # ユーザーIDが存在しなければエラー
    if response is None:
        raise HTTPException(
            status_code=400, detail=ErrorResponse.USER_NOT_FOUND
        )

    return response
