import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]


def chatbot_response(chat_input, placeholder_response):
    # Append user input
    st.session_state.conversation_history.append({"role": "user", "content": chat_input})

    # get list of retrieved text
    contexts = ["content"]

    # concatenate contexts and user message to generate augmented query
    augmented_query = " --- ".join(contexts) + " --- " + chat_input
    st.session_state.conversation_history.append({"role": "user", "content": augmented_query})

    # Generate the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=st.session_state.conversation_history,
        stream=True
    )

    # Display the response
    assistant_response = ""
    for chunk in response:
        if "role" in chunk["choices"][0]["delta"]:
            continue
        elif "content" in chunk["choices"][0]["delta"]:
            r_text = chunk["choices"][0]["delta"]["content"]
            assistant_response += r_text
            placeholder_response.markdown(assistant_response, unsafe_allow_html=True)

    # Display the response along with the sources
    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_response})


def api_call_generator(user_message, api_call_placeholder):
    st.session_state.conversation_history.append({"role": "user", "content": user_message})

    embed_model = "text-embedding-ada-002"
    system_msg = """I want you to convert natural language into an API call based on the examples below. You should match up the user's input with the following tags/filters. 
                    Use the context to find the relevant tag, industry, sub-industry, and so on. Show the response in code markdown format.

                    Example query:

                    {
                    "must": {
                        "filters": {
                        "has_website_url": {
                            "values": ["yes"],
                            "execution": "or"
                        },
                        "hq_country": {
                            "values": ["United States"],
                            "execution": "or"
                        },
                        "industries": {
                            "values": ["software"],
                            "execution": "or"
                        }
                        },
                        "execution": "and"
                    },
                    "must_not": {
                        "company_status": ["closed"],
                        "company_type": ["service provider", "government nonprofit"]
                    },
                    "should": {
                        "filters": {}
                    }
                    }
                    ** Note: Series should be in all caps i.e. SERIES A.

                    Now, use this context to write a new query based sole on the input. 
                    Also write a summary of the the API options that you've chosen i.e. the tags, industries, sub-industries, HQ region, and so on, before showing the API query. Write like a VC analyst.

                    Lastly, can you create a URL based on the API query, here's an example of a final URL: https://site.com/companies.startups/f/company_status/not_closed/company_type/not_service%20provider_government%20nonprofit/growth_stages/not_mature/has_website_url/anyof_yes/slug_locations/anyof_~united_states~/tags/not_outside%20tech/technologies/anyof_artificial%20intelligence/total_funding_max/anyof_10000000

                    User input:
                    """
    messages = [{"role": "system", "content": system_msg}]
    messages += st.session_state.conversation_history
    # Get list of retrieved text
    contexts = ['matches']

    # Concatenate contexts and user message to generate augmented query
    augmented_query = " --- ".join(contexts) + " --- " + user_message
    messages.append({"role": "user", "content": augmented_query})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        stream=True
    )

    assistant_message = ""
    for chunk in chat:
        if "role" in chunk["choices"][0]["delta"]:
            continue
        elif "content" in chunk["choices"][0]["delta"]:
            assistant_message += chunk["choices"][0]["delta"]["content"]
            api_call_placeholder.markdown(assistant_message, unsafe_allow_html=True)

    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_message})


# Streamlit app

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# # Add sidebar with dropdown
# assistant_options = ["API Call Generator", "AI Startups"]
# selected_option = st.sidebar.selectbox("Choose an assistant:", assistant_options)

# # Handle AI Startups option
# if selected_option == "AI Startups":
#
#     # Setup conversation history with session state
#     if "conservation_history" not in st.session_state:
#         st.session_state.conversation_history = [
#             {"role": "system", "content": """You are a helpul assistant that helps investors find relevant startups based solely on data (the context provided),
#             if the context is available, provide with each response provide a summary of the startup like an analyst, including what they do,
#             where they're located, and what series of VC funding they've raised, and other relevant details an investor would care about.
#             Start each list with company name with the profile URL wrapped around it.
#             If context isn't available, say 'Sorry I don't have that data. Right now I'm only trained on 5k AI startups.'.
#             """}
#         ]
#     st.title("SQL Assistant")
#     st.write(
#         "SQL Assistant is a GPT-4-enabled startup research assistant. Ask it for a list of startups, and it will retrieve relevant sources from site.")
#
#     # Add chatbot
#     chat_input = st.text_input("You:")
#     response_button = st.button("Send")
#     placeholder_response = st.empty()
#
#     if response_button:
#         chatbot_response(chat_input, placeholder_response)
#
# ...

# Handle API Call Generator option
# elif selected_option == "API Call Generator":
# Handle API Call Generator option
st.title("GPT SQL Builder")
st.write("Welcome to the GPT SQL Builder. This assistant will help you create SQL queries based on natural language.")

# Replace the print and input statements with Streamlit functions
st.write("Type your query and press the button to get the SQL.")
user_message = st.text_input("Query:")
generate_button = st.button("Generate SQL")
api_call_placeholder = st.empty()

if generate_button:
    api_call_generator(user_message, api_call_placeholder)



