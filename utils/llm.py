from dotenv import load_dotenv
import os
import time

from google import genai


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# Gemini Client
# ---------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ---------------------------------------------------
# Model
# ---------------------------------------------------

MODEL_NAME = "gemini-3.5-flash-lite"


# ---------------------------------------------------
# Generate Answer
# ---------------------------------------------------

def generate_answer(prompt, max_retries=3):
    """
    Generate an answer using Gemini.

    Automatically retries temporary API failures
    such as 503 UNAVAILABLE.
    """

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text


        except Exception as e:

            error_message = str(e)

            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/{max_retries}): "
                f"{error_message}"
            )


            # ---------------------------------------
            # Retry temporary service errors
            # ---------------------------------------

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue


            # ---------------------------------------
            # Non-retryable error
            # ---------------------------------------

            raise


    raise RuntimeError(
        "Gemini failed after multiple attempts."
    )