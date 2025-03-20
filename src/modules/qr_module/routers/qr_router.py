import io
import base64

from fastapi import UploadFile, File, Response, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter

from PIL import Image

#QR creator
from ..utils.agent import Agent

router = APIRouter()


@router.post("/create_qr")
async def post(data: str = Form(...), img: UploadFile = File(...)): 

    try: 

        agent = Agent()

        image_bytes = await img.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_resize = image.resize((200, 200))

        image_buf = io.BytesIO()
        image_resize.save(image_buf, "png")

        image_buf.seek(0)

        image = Image.open(io.BytesIO(image_buf.getvalue()))

        response = agent.create_qr(data, image)

        image_data = base64.b64decode(response)

        return Response(image_data, media_type="image/jpeg")
    
    except HTTPException as http_e: 
        return JSONResponse(content=jsonable_encoder({ "Error": http_e.detail}), status_code = http_e.status_code)
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"message": "Error interno", "error": str(e.args),}), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    