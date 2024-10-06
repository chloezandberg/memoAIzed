# memoAIzed
A way to recycle AI images for the sake of sustainability! [Take a look at our presentation here.](https://github.com/user-attachments/files/17269129/memoAIzed.pdf)


## Demo
In the demo below, the first prompt is entered for the first time, and the application generates an image using generative AI. The second prompt entered is similar enough to the first, so the app outputs the memoized solution (the previously generated image from the other similar prompt).

https://github.com/user-attachments/assets/1eb59e34-16fa-4b5c-bd42-40872d349041

Note the following:
- The LLM will return the same image for two prompts that are worded differently, but mean the same thing (ie. "man riding a tiger with a cowboy hat" being recognized to be semantically identical to "person wearing a western hat riding a large striped cat"), optimizing sustainability while maintaining performance and user experience.
- The retrieval time for the memoized prompt is more than 12.5 times faster than for the non-memoized prompt (11.43 seconds vs. 0.91 seconds in the demo).
## Background
AI image generation is a highly energy-demanding process. Generating just 1 AI image using Stable Diffusion can cost up to 290 watt-hours of energy ([source](https://mcengkuru.medium.com/the-hidden-cost-of-ai-images-how-generating-one-could-power-your-fridge-for-hours-174c95c43db8)), roughly the energy required to fully charge a smartphone 6 times ([source](https://www.energysage.com/electricity/house-watts/how-many-watts-does-a-phone-charger-use/)). In addition, image-generation models have taken the world by storm over the last year, with over 30 million AI-generated images created per day ([source](https://techreport.com/statistics/software-web/ai-image-generator-market-statistics/#:~:text=As%20of%20August%202023%2C%20people,better%20than%20human%2Dcreated%20art.)). This led us to ask the question - how many of these images were unique? For example, surely more than one person generates an image of a cute dog, or a flying pig, every day... Do we really have to generate a new image for each duplicate prompt? This is where memoAIzed comes in.

## What memoAIzed does
memoAIzed is an image generator that uses memoization (as the name implies) to remember all previously generated images and reuse them if they fit the prompt (an LLM compares the prompt to previously seen prompts). This allows us to skip the process of AI image generation for previously seen inputs, instead costing a simple database lookup and an LLM call. Essentially, we've lowered the cost of image generation down to the cost of text generation (for most use cases, assuming the user base has scaled), which only costs around 1% of the energy ([source](https://lifestyle.livemint.com/news/big-story/ai-carbon-footprint-openai-chatgpt-water-google-microsoft-111697802189371.html)). You can imagine how the application would improve dramatically if the user base scaled and the database of previously seen images grew larger and larger. As a bonus, the latency for memoized images is 5 times faster on average than for non-memoized images!
\

*Fun fact: memoAIzed was in fact inspired by how memoization is used in Dynamic Programming problems to drastically improve efficiency. We wanted to apply the same principles to improve the efficiency of GenAI, and it so this project was born!*

## Tech Stack
We used Amazon Titan Image Generator G1 v2 for image generation, Llama 3.1 70B Instruct as the LLM, Amazon DyanoDB to map memoized prompts to images, and AWS S3 to store the image files. We then threw it all together using Streamlit for lightning-fast UI development (it was only a 9-hour hackathon)!

## Next Steps
- It'd be even more energy-efficient to use a semantic search algorithm to compare new prompts with previous prompts, instead of asking an LLM to do it for us.
- A toggle that allows the user to choose between our memoized image generator and a regular image generator would be nice since it would give users more flexibility with how accurate they want their results.
- A slider feature that allows users to balance sustainability with accuracy would give users even more flexibility.

## How to run it
1. Clone the repo into a local folder.
2. Assuming Python 3 has been downloaded, run "python -m venv venv" to create the virtual environment
3. Run "\venv\Scripts\Activate" to activate the virtual environment.
4. Run "pip install -r requirements.txt" to install all required packages.
5. Run "python app.py" to compile the script, then "streamlit run app.py" to run the front-end

