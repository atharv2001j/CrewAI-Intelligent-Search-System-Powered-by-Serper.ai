# from crewai import Crew,Process
# from tasks import research_task,write_task
# from agents import news_researcher,news_writer

# ## Forming the tech focused crew with some enhanced configuration
# crew=Crew(
#     agents=[news_researcher,news_writer],
#     tasks=[research_task,write_task],
#     process=Process.sequential,

# )

# ## starting the task execution process wiht enhanced feedback

# result=crew.kickoff(inputs={'topic':'AI in healthcare'})
# print(result)


import streamlit as st
from crewai import Crew, Process
from tasks import research_task, write_task
from agents import news_researcher, news_writer
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import google.api_core.exceptions

# Forming the tech-focused crew with some enhanced configuration
crew = Crew(
    agents=[news_researcher, news_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(10), retry=retry_if_exception_type(google.api_core.exceptions.ResourceExhausted))
def generate_news(topic):
    result = crew.kickoff(inputs={'topic': topic})
    return result

# Streamlit UI
st.title("Newsgenerator")

st.markdown("""
    ## Generate Custom News Articles
    Enter a topic of your choice to generate a news article focused on that topic.
""")

topic = st.text_input("Enter the topic")

if st.button("Generate News"):
    if topic:
        with st.spinner("Generating news..."):
            try:
                result = generate_news(topic)
                st.success("News generation completed!")
                st.write(result)
            except google.api_core.exceptions.ResourceExhausted:
                st.error("Resource limit reached. Please try again later.")
    else:
        st.error("Please enter a topic to generate news.")
