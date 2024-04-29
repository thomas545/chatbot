from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from repositories.users import UserRepositories
from schemas.users import UserSignup, UserResponse, UserLogin, UserTokenFields
from core.auth import create_access_token, verify_password


load_dotenv()

auth = APIRouter(prefix="/users/auth", tags=["auth"])


@auth.post("/signup/", response_model=UserResponse)
async def signup(req: UserSignup):
    print("iam in signup")
    if UserRepositories().get_object(email=req.email):
        raise HTTPException(400, "User Already exists")

    # try:
    user_json = req.model_dump()
    print("user_id ->> ", user_json)
    
    user_obj = UserRepositories().create(**user_json)
    user_obj = user_obj.to_dict()
    

    user_obj["access_token"] = create_access_token(user_obj)
    # except Exception as exc:
    #     raise HTTPException(400, exc.args)

    return UserResponse(**user_obj)


@auth.post("/login/", response_model=UserResponse)
async def login(user: UserLogin):
    email = user.email
    password = user.password
    db_user = UserRepositories().get_object(email=email)

    if not db_user or not verify_password(password, db_user.get("password")):
        raise HTTPException(403, "Invalid User email / Password")

    if not db_user.get("is_active"):
        raise HTTPException(401, "Account is inactive")

    db_user["access_token"] = create_access_token(db_user)
    return UserResponse(**db_user)
