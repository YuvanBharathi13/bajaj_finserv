from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

class RequestData(BaseModel):
    data: List[str] = Field(..., example=["A", "1", "334", "4", "R", "$"])

app = FastAPI(
    title="Bajaj Finserv Health Logic API",
    description="An API to process an array of data and return classified information.",
    version="1.0.0"
)

FULL_NAME = "Yuvan Bharathi"
DOB_DDMMYYYY = "25022003"
EMAIL_ID = "yuvanbharathi.s2022@vitstudent.ac.in"
ROLL_NUMBER = "22BDS0043"
USER_ID = f"{FULL_NAME.lower()}_{DOB_DDMMYYYY}"

# --- API Endpoint ---
@app.post("/bfhl")
async def process_data(request: RequestData):
    """
    Processes an array of mixed data types (as strings) and returns a structured response.
    """
    try:
        input_data = request.data
        
        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0
        alphabet_string = ""

        # Process each item in the input data array
        for item in input_data:
            if item.isalpha():
                alphabets.append(item.upper())
                alphabet_string += item
            elif item.isnumeric():
                num = int(item)
                total_sum += num
                if num % 2 == 0:
                    even_numbers.append(str(num)) # Store as string
                else:
                    odd_numbers.append(str(num)) # Store as string
            else:
                # Assuming any other character is a special character
                special_characters.append(item)

        # --- Logic for concatenated and reversed alternating caps string ---
        # 1. Concatenate all alphabets: Done in the loop (alphabet_string)
        # 2. Reverse the string
        reversed_alphabets = alphabet_string[::-1]
        
        # 3. Apply alternating caps
        alternating_caps_list = []
        for i, char in enumerate(reversed_alphabets):
            if i % 2 == 0:
                alternating_caps_list.append(char.upper()) # Even index -> Uppercase
            else:
                alternating_caps_list.append(char.lower()) # Odd index -> Lowercase
        
        concat_string = "".join(alternating_caps_list)

        # Construct the successful response payload
        response_payload = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL_ID,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string
        }
        
        return response_payload

    except Exception as e:
        # Graceful exception handling
        # In a real-world app, you might log the error `e`
        raise HTTPException(
            status_code=400, 
            detail={
                "is_success": False, 
                "user_id": USER_ID,
                "error_message": f"An error occurred: {str(e)}"
            }
        )

# --- Root endpoint for basic health check ---
@app.get("/")
def read_root():
    return {"status": "API is running. Use the /bfhl endpoint with a POST request."}

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)