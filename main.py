from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from stac_check.lint import Linter

app = FastAPI()


@app.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "healthy"}


class Payload(BaseModel):
    content: dict[str, Any]


@app.post("/validate-stac")
def validate_stac(payload: Payload) -> tuple[dict[str, Any], int]:
    data = payload.content

    try:
        linter = Linter(data, assets=True)
        best_practices = linter.create_best_practices_dict()

        error = linter.error_msg
        failed_schema = linter.failed_schema

        error_msg = f"Error: {error}"

        if failed_schema:
            error_msg = [[f"{error_msg}: Failed schema: {failed_schema}"]]

        warnings = [i for j, i in best_practices.items() if i]

        if not linter.valid_stac:
            return {
                "status": "error",
                "message": "Errors found when validating STAC",
                "content": error_msg,
            }, 400

        return {
            "status": "success",
            "message": "Valid STAC",
            "content": warnings,
            "type": linter.asset_type,
        }, 200

    except Exception as e:
        return {"status": "error", "message": str(e), "content": []}, 500
