import os 
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(api_key=os.environ["HF_TOKEN"], provider="auto",)

completion = client.chat.completions.create(
    model="Qwen/Qwen3-32B",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "Explain what an API is , in one sentence."}

    ],
)

print(completion.choices[0].message.content)
print("----")
print("usage:", completion.usage)

def summerize(text):
    completion = client.chat.completions.create(
        model="Qwen/Qwen3-32B",
        max_tokens=200,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "you are a consise summarizer. Reply in 1-2 clear sentence."},
            {"role": "user", "content": f"summarize the following:\n\n{text}"},
        ],
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    sample = """Django is a  highlevel python web framework that encourages
    rapid development and clean, pragmatic design.it handles much of the 
    hassle of web development, so you can focus on writing your app. """
    print(summerize(sample))

