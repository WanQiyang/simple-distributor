# api.py by Ribo
# version 2024.03.23.1

import hashlib
import json
import os

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.http import HTTPBearer
from pydantic import BaseModel, UUID4

HOST = "127.0.0.1"
PORT = 8080


class ConversationItem(BaseModel):
    conversation: UUID4


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# init
with open("users.json", encoding="utf-8") as fp:
    users = json.load(fp)

users = {user["username"]: hashlib.md5(
    user["password"].encode()).hexdigest() for user in users}

with open("session_token.txt", encoding="utf-8") as fp:
    session_token = fp.read().strip()


def auth(credentials=Depends(security)):
    try:
        assert credentials.scheme == "Bearer"
        username, pwmd5 = credentials.credentials.split(":")
        assert pwmd5 == users[username]

    except:
        raise HTTPException(status_code=401)

    return {"username": username}


@app.get("/session")
async def GetSessionToken(user=Depends(auth)):
    return {"session_token": session_token}


@app.get("/conversation")
async def GetConversation(user=Depends(auth)):
    username = user["username"]
    conversation_path = os.path.join("conversations", f"{username}.txt")

    if not os.path.exists(conversation_path):
        return {"conversation": []}

    with open(conversation_path, encoding="utf-8") as fp:
        conversation = [line.strip() for line in fp if not line.strip() == ""]

    return {"conversation": conversation}


@app.post("/conversation")
async def PostConversation(item: ConversationItem, user=Depends(auth)):
    username = user["username"]
    conversation_path = os.path.join("conversations", f"{username}.txt")

    with open(conversation_path, "a", encoding="utf-8") as fp:
        fp.write(f"{str(item.conversation)}\n")

    return {}


if __name__ == "__main__":
    import uvicorn as uvicorn
    uvicorn.run(app=app, host=HOST, port=PORT)
