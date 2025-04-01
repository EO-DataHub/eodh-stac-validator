from fastapi import FastAPI

from pydantic import BaseModel

from stac_check.lint import Linter


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Payload(BaseModel):
    content: object

@app.post("/validate-stac")
def validate_stac(payload: Payload):
    data = payload.content

    try:
        linter = Linter(data, assets=True)
        best_practices = linter.create_best_practices_dict()

        errors = [i for j, i in best_practices.items() if i]
        if errors:
            return { 
                "status": "error", 
                "message": "Errors found when validating STAC",
                "content": errors }, 400
        else:
            return { "status": "success", "message": "Valid STAC" }, 200
    except Exception as e:
        return { "status": "error", "message": str(e) }, 500
