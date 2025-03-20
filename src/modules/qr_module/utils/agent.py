from google import genai 
from google.genai import types
from src.setup.setup import settings
from fastapi import HTTPException

from PIL.ImageFile import ImageFile

from .qr_creater import QRcreater

model_name = "gemini-2.0-flash"


automatic_function_call = types.AutomaticFunctionCallingConfig(
    ignore_call_history=False, 
)


class Agent: 

    def create_qr(self, data: str, img: ImageFile): 

        client = genai.Client(api_key=settings.gemini_key)
        system_instructions = """You are an image processor specializing in QR code generation. 
                                    Your task is to extract the dominant color from an input image and convert it to HEX format. 
                                    The dominant color is the most frequently occurring color in the image.
                                    Once extracted, pass both the HEX color and the data to the function. 
                                    Do not ask for confirmation automatically use the most dominant color. 
                                    Do not response json.
                                    If the color is white change to other color or use black."""

        model = client.models.generate_content(
            contents=[img, f"""Generate a qr code for this content : {data}"""],
            model=model_name,
            config = types.GenerateContentConfig(
                tools=[QRcreater.generate_qr], 
                system_instruction = system_instructions, 
                automatic_function_calling=automatic_function_call,
            )
        )

        if len(model.automatic_function_calling_history) == 0: 
            raise HTTPException(detail="Error processing data", status_code=400) 
        
        return [i.function_response.response.get('result') for j in model.automatic_function_calling_history for i in j.parts if i.function_response != None][0]


