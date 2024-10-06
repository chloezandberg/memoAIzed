import streamlit as st
import boto3
import io
import json
from botocore.exceptions import ClientError
import base64
from PIL import Image
import time
# Initialize the Bedrock client
client = boto3.client(service_name='bedrock-runtime')

__TableName__ = "promptCache"
boto3.client('dynamodb')
dynamoClient = boto3.client(service_name="dynamodb", region_name="us-west-2")
db = boto3.resource('dynamodb')
promptTable = db.Table(__TableName__)

# Initialize the S3 client
s3_client = boto3.client('s3')
bucket_name = 'cichackathon2024'

def generate_image(prompt):
    # Define the request payload

    payload = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 512,
            "width": 512,
            "cfgScale": 8.0,
            "seed": 0
        }
    })
    
    # Initialize the Bedrock client
    client = boto3.client(service_name='bedrock-runtime')

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
    
    return image_bytes

def upload_image_to_s3(image_bytes, prompt):
    s3_key = f'images/{prompt}.png'  # Unique S3 key for each prompt
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=image_bytes, ContentType='image/png')
    # return f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'
    return s3_key

def generate_image_and_store(prompt):
    image_bytes = generate_image(prompt)  # Assuming generate_image returns binary data
    
    # Upload image to S3
    image_key = upload_image_to_s3(image_bytes, prompt)

    # Store prompt and S3 URL in DynamoDB
    promptTable.put_item(
        Item={
            'prompt': prompt,
            'image_url': image_key  # Storing S3 URL instead of Base64 data
        }
    )
    
    return image_key  # Return the URL for display in the app

def getOrGenerate(prompt):    
    # Contact llm with this prompt
    existingPrompt = findExistingPrompt(prompt)
    existingPrompt = existingPrompt.strip()
    if ("None" != existingPrompt):
        entry = promptTable.get_item(
            Key={
                'prompt': existingPrompt
            }
        )
        image_key = entry["Item"]["image_url"]
        return image_key
    else:
        new_image_key = generate_image_and_store(prompt)
        # promptTable.put_item(
        #     Item={
        #         'prompt': prompt,
        #         'image': new_image
        #     }
        # )
        
        return new_image_key
    
def extractPrompts(item):
    return item["prompt"]
def findExistingPrompt(prompt):
    listPrompts = promptTable.scan()['Items']
    prompts = map(extractPrompts, listPrompts)
    cached_prompts_array = list(prompts) #get keys from db

    cached_prompts = ""

    # turn cached prompt array file into one string separated by '|'
    for existingPrompt in cached_prompts_array:
        cached_prompts = cached_prompts + " | " + existingPrompt
    # Adding one final "| and adding the rest of the prompt for LLM"
    cached_prompts = cached_prompts + " | Is there anything in this list of prompts (separated by the character '|') that is sufficiently and semantically the same to the prompt '" + prompt + "'? If there is, return it exactly without saying anything else. If not, if there's even a bit of a difference, return 'None'."

    return contactLLM(cached_prompts)  
    
def contactLLM(prompt):
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-west-2")

    # Set the model ID, e.g., Llama 3 70b Instruct.
    model_id = "meta.llama3-70b-instruct-v1:0"

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

    out = ""

    try:
        # Invoke the model with the request.
        streaming_response = client.invoke_model_with_response_stream(
            modelId=model_id, body=request
        )

        # Extract and print the response text in real-time.
        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "generation" in chunk:
                # print(chunk["generation"], end="")
                out = out + chunk["generation"]

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    return out

#---------------------------------------------------------------------
# STREAMLIT APP
col1, col2, col3 = st.columns([1, 9, 1])

REMOVE_PADDING_FROM_SIDES="""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0rem;
    }   
</style>
"""

st.markdown(REMOVE_PADDING_FROM_SIDES, unsafe_allow_html=True)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
picture_rounded = """
    <style>
        .container1 {
            border-radius: 8px;
        }
        .container2 {
            /* Add styles for Container 2 if needed */
        }
    </style>
"""
st.markdown(hide_img_fs, unsafe_allow_html=True)
st.markdown(hide_img_fs, unsafe_allow_html=True)

with col2:  
    st.image("./media/logo.svg", width=557)

    
    




with col2:
    with st.container():
        col2_1, col2_2 = st.columns([3, 1])
        with col2_1:
            prompt = st.text_input(label="",placeholder="Enter your text prompt")

        with col2_2:
            st.markdown("<div style='margin-top: 27px;'></div>", unsafe_allow_html=True)
            gen_button_clicked = st.button("Generate Image")
    


if (gen_button_clicked & (prompt != "")):
            with col2:
                # Centering
                st.markdown("""
                <style>
                div {
                    text-align:center;
                    align-items: center;
                    justify-content: center;
                }
                </style>""", unsafe_allow_html=True)

                with st.spinner("Generating image..."):
                    start_time = time.time()
                    image_key = getOrGenerate(prompt)
                    print(image_key)
                    image_response = s3_client.get_object(Bucket=bucket_name, Key=image_key)
                    image_base64 = image_response['Body'].read()
                     # Convert image to base64 to embed in HTML
                    image_data = base64.b64encode(image_base64).decode('utf-8')
                    image_html = f'<img src="data:image/png;base64,{image_data}" style="border-radius: 10px; width: 557px;"/>'

                    # Use markdown to render the image with rounded corners
                    st.markdown(image_html, unsafe_allow_html=True)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    st.write(f"This image took {elapsed_time:.2f} seconds to generate!")