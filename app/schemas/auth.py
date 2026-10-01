from pydantic import (
    AliasChoices,
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


def validate_bcrypt_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must not exceed 72 bytes")

    return password


class RegisterRequest(BaseModel):
    fullname: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str

    @field_validator("fullname")
    @classmethod
    def validate_fullname(cls, fullname: str) -> str:
        fullname = fullname.strip()

        if not fullname:
            raise ValueError("Full name must not be empty")

        return fullname

    _validate_password = field_validator("password")(
        validate_bcrypt_password
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    _validate_password = field_validator("password")(
        validate_bcrypt_password
    )


class UserResponse(BaseModel):
    id: int
    fullname: str | None = Field(
        default=None,
        validation_alias=AliasChoices("fullname", "full_name")
    )
    email: EmailStr

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
