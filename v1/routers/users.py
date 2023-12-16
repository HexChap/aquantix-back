import json
from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, responses, Body
from google.cloud.firestore_v1 import DocumentReference
from google.cloud.firestore_v1.field_path import FieldPath
from pydantic import BaseModel

from v1.core import settings

__tags__ = ["users"]
__prefix__ = "/users"

from v1.core.firebase import client

router = APIRouter()


@dataclass
class Animal:
    name: str
    image_url: str


class UserPayload(BaseModel):
    email: str
    is_organizer: bool


@router.get("/")
async def get_all():
    return {user.id: user.to_dict() for user in client.collection("users").limit(10).get()}


@router.post("/")
async def create_user(payload: Annotated[UserPayload, Body()]):
    _, user = client.collection("users").add(payload.model_dump())

    return {
        user.id: user.get().to_dict()
    }


@router.get("/{user_id}")
async def get_user(user_id: str):
    user = client.collection("users").document(user_id).get()

    return {
        user.id: user.to_dict()
    }


@router.get("/{user_id}/animals", response_model=list[Animal])
async def get_user_animals(user_id: str):
    animals: list[Animal] = []
    animal_ids = client.collection("users").document(user_id).get().to_dict().get("animal_ids")

    for animal_id in animal_ids:
        animals.append(
            Animal(
                    name=animal_id,
                    image_url=client.collection("animals").document(animal_id).get().to_dict().get("image_url")
            )
        )

    return animals
