import httpx

CHATGPT_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"  # Replace with the actual endpoint if different
CHATGPT_API_KEY = "YOUR_OPENAI_API_KEY"  # Store this in .env for security

async def get_college_ranking(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150  # Adjust as needed
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(CHATGPT_ENDPOINT, headers=headers, json=data)
    return response.json()["choices"][0]["text"].strip()
