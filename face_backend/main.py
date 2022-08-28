from fastapi import FastAPI, File, UploadFile
import uuid
import os
from pydantic import BaseModel
import base64
from deepface import DeepFace
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Files(BaseModel):
    fileOne: str
    fileTwo: str

@app.post("/process")
def same_face_check(b64Files: Files):

    file_data = [b64Files.fileOne, b64Files.fileTwo]
    filenames = []

    print(len(file_data[0]), len(file_data[1]));

    for index, file in enumerate(file_data):
        try:
            print("trying")
            file_content = base64.b64decode(file.split(",")[1])
            print("WORKED UP TO HERE")
            with open(str(index) + ".jpg", "wb") as f:
                f.write(file_content)
        except Exception:
            return {"message": "error uploading"}

    result  = DeepFace.verify(img1_path="0.jpg", img2_path="1.jpg")
    print(result);

    os.system("rm " + filenames[0]);
    os.system("rm " + filenames[1]);

    return result