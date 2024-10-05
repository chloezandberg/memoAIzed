import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError
import base64
# Initialize the Bedrock client
client = boto3.client(service_name='bedrock-runtime')

__TableName__ = "promptCache"
boto3.client('dynamodb')
dynamoClient = boto3.client(service_name="dynamodb", region_name="us-west-2")
db = boto3.resource('dynamodb')
promptTable = db.Table(__TableName__)

def generate_image(prompt):
    # Define the request payload

    payload = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": 0
        }
    })

    MODEL_ID = "amazon.titan-image-generator-v2:0"
    
    # Invoke the model
    response = client.invoke_model(
        body=payload,
        modelId=MODEL_ID,
        contentType='application/json',
        accept="application/json"
    )
    
    # Parse the response
    result = json.loads(response.get("body").read())
    base64_image = result.get("images")[0]
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)

    finish_reason = result.get("error")
    
    return base64_image

# Streamlit app
st.title("Amazon Titan Image Generator")
prompt = st.text_input("Enter your text prompt:")

if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        image_data = generate_image(prompt)
        image = base64.b64decode(image_data)
        st.image(image, caption="Generated Image")

# Set the model ID, e.g., Llama 3 70b Instruct.
llama_model_id = "meta.llama3-70b-instruct-v1:0"

# Embed the prompt in Llama 3's instruction format.
formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

# Format the request payload using the model's native structure.
native_request = {
    "prompt": formatted_prompt,
    "max_gen_len": 512,
    "temperature": 0.5,
}

# Convert the native request to JSON.
request = json.dumps(native_request)

try:
    # Invoke the model with the request.
    streaming_response = client.invoke_model_with_response_stream(
        modelId=llama_model_id, body=request
    )

    # Extract and print the response text in real-time.
    for event in streaming_response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])
        if "generation" in chunk:
            print(chunk["generation"], end="")

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{llama_model_id}'. Reason: {e}")
    exit(1)

def checkOrGenerate(prompt):    
    # Contact llm with this prompt
    # TODO existingPrompt = findExistingPrompt(prompt)
    if (False): #existingPrompt != "None"):
        return # TODO: get imagine from database using existingPrompt key
    else:
        # new_image = generate_image(prompt)
        # TODO: Add prompt and image to database
        test = promptTable.get_item(
            Key={
                'prompt': 'man with black hair smiling wearing suit and tie with beard and sunglasses'
            }
        )
        
        print(test["Item"])
        new_image_data = 0
        # TODO new_image = base64.b64decode(new_image_data)
        return new_image_data
    

def findExistingPrompt(prompt):
    cached_prompts_array = [] #get keys from db

    # turn cached prompt array file into one string separated by '|'
    for existingPrompt in (cached_prompts_array):
        cached_prompts = cached_prompts + " | " + existingPrompt
    # Adding one final "| and adding the rest of the prompt for LLM"
    cached_prompts = cached_prompts + " | Is there anything in this list of prompts (separated by the character '|') that is sufficiently and semantically the same to the prompt '" + prompt + "'? If there is, return it exactly without saying anything else. If not, return 'None'."

    try:
        return (contactLLM(cached_prompts))
    except:
        return "None"
    
def contactLLM(prompt):
    #TODO send prompt to LLM and get respose back
    #Parse response to get necessary shit
    return #TODO prompt


# def checkOrGenerate(prompt):    
#     # Contact llm with this prompt
#     existingPrompt = findExistingPrompt(prompt)
#     if (existingPrompt != "None"):
#         return # TODO: get imagine from database using existingPrompt key
#     else:
#         new_image = generate_image(prompt)
#         # TODO: Add prompt and image to database
#         return new_image
    

# def findExistingPrompt(prompt):
#     # cached_prompts_array = get keys from db

#     # turn cached prompt array file into one string separated by '|'
#     for existingPrompt in (cached_prompts_array):
#         cached_prompts = cached_prompts + " | " + existingPrompt
#     # Adding one final "| and adding the rest of the prompt for LLM"
#     cached_prompts = cached_prompts + " | Is there anything in this list of prompts (separated by the character '|') that is sufficiently and semantically the same to the prompt '" + prompt + "'? If there is, return it exactly without saying anything else. If not, return 'None'."

#     try:
#         return (contactLLM(cached_prompts))
#     except:
#         return "None"
    
# def contactLLM(prompt):
#     #TODO send prompt to LLM and get respose back
#     #Parse response to get necessary shit
#     return #TODO prompt


    
