import os
import json


from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator, model_validator, Field, EmailStr
from schwifty import IBAN
from typing_extensions import Self

app = FastAPI()


class Address(BaseModel):
    name: str
    second_line: str | None = None
    street_line: str | None = None
    city_line: str
    zip_code: str
    country: str | None = None


class Account(BaseModel):
    name: str
    iban: str
    agreement: bool

    @field_validator("iban")
    @classmethod
    def valide_iban(cls, v: str) -> str:
        if not IBAN(v, allow_invalid=True).is_valid:
            raise ValueError("Das ist keine gültige IBAN")
        return IBAN(v).formatted


class MembershipData(BaseModel):
    yearly_amount: int = Field(
        gt=24 * 100 - 1,
        description="Der jährliche Beitrag muss mindestens 24 Euro sein.",
    )
    paid_monthly: bool = False


class Info(BaseModel):
    name: str
    email: EmailStr
    newsletter: bool

    membershipData: MembershipData
    account: Account
    address: Address

    def create_filename(self):
        return f"{self.name}_{self.account.iban}.json"

    @model_validator(mode="before")
    def check_unique(self) -> Self:
        if self.create_filename() in os.listdir("./uploads"):
            raise ValueError(
                "Du scheinst schon Fördermitglied zu sein. Falls du Fragen hast, wende dich gerne an vorstand@queer-lexikon.net"
            )
        return self


goal: int = 100


def get_current() -> int:
    return len(os.listdir("./uploads/")) + 34


@app.get("/")
async def root():
    return RedirectResponse("static/index.html")


@app.get("/progress")
async def progress():
    return {"current": get_current()}


@app.post("/generate")
async def generate(info: Info):
    possible_filename = info.create_filename()
    if possible_filename not in os.listdir("./uploads"):
        serializable_info = jsonable_encoder(info)
        with open(f"./uploads/{possible_filename}", "x") as fp:
            json.dump(serializable_info, fp, indent=4)
        return {"success": True, "current": get_current(), "goal": goal}

    return {"success": False, "already_exists": True}


app.mount("/static", StaticFiles(directory="static"), name="static")
