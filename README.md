# memoAIzed
We invented recycling but for AI-generated images. 

## Background
AI image generation is a highly energy-demanding process. Generating just 1 AI image using Stable Diffusion can cost up to 290 watt-hours of energy ([source](https://mcengkuru.medium.com/the-hidden-cost-of-ai-images-how-generating-one-could-power-your-fridge-for-hours-174c95c43db8)), roughly the energy required to fully charge a smartphone 6 times ([source](https://www.energysage.com/electricity/house-watts/how-many-watts-does-a-phone-charger-use/)). In addition, image-generation models have taken the world by storm over the last year, with over 30 million AI-generated images created per day ([source](https://techreport.com/statistics/software-web/ai-image-generator-market-statistics/#:~:text=As%20of%20August%202023%2C%20people,better%20than%20human%2Dcreated%20art.)). This led us to ask the question - how many of these images were unique? For example, surely more than one person generates an image of a cute dog, or a flying pig, every day... Do we really have to generate a new image for each duplicate prompt? 

## What memoAIzed does
This is where memoAIzed comes in. memoAIzed is an image generator that uses memoization (as the name implies) to remember all previously generated images and reuse them if they fit the prompt (an LLM compares the prompt to previously seen prompts). This allows us to skip the process of AI image generation for previously seen inputs, instead costing a simple database lookup and an LLM call. Essentially, we've lowered the cost of image generation down to the cost of text generation (for most use cases, assuming the user base has scaled), which only costs around 1% of the energy ([source](https://lifestyle.livemint.com/news/big-story/ai-carbon-footprint-openai-chatgpt-water-google-microsoft-111697802189371.html)). You can imagine how the application would improve dramatically if the user base scaled and the database of previously seen images grew larger and larger. As a bonus, the latency for memoized images is 5 times faster on average than for non-memoized images!


## Demo
In the demo below, the prompt "computer" is entered for the first time, and the application generates an image using generative AI. The second prompt, "desktop", is similar enough to "computer", so the app outputs the memoized solution. \
\
![memoaized-demo_6lKDFVUZ-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/178b00d9-4ce3-4369-bc66-76ed6d0608cd) \
\
Note the following:
- The LLM will return the same image for two prompts that are worded differently, but mean the same thing (ie. computer and desktop), optimizing sustainability while maintaining performance.
- The retrieval time for the memoized prompt is more than 5 times faster than for the non-memoized prompt (3 seconds vs. 16 seconds in the demo).

## Tech Stack
We used Amazon Titan Image Generator G1 v2 for image generation, Llama 3.1 70B Instruct as the LLM, Amazon DyanoDB to map memoized prompts to images, and AWS S3 to store the image files. We then threw it all together using Streamlit for lightning-fast UI development (it was only a 9-hour hackathon)!

## Next Steps
- It'd be even more energy-efficient to use a semantic search algorithm to compare new prompts with previous prompts, instead of asking an LLM to do it for us.
- We could incorporate a toggle feature that allows the user to choose between our memoized image generator and a regular image generator that creates an image from scratch for each request.

## How to run it
1. Clone the repo into a local folder.
2. Assuming Python 3 has been downloaded, run "python -m venv venv" to create the virtual environment
3. Run "\venv\Scripts\Activate" to activate the virtual environment.
4. Run "pip install -r requirements.txt" to install all required packages.
5. Run "python app.py" to compile the script, then "streamlit run app.py" to run the front-end

