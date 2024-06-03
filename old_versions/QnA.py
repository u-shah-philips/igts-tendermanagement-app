import streamlit as st
import boto3
from botocore.exceptions import ClientError
import logging
import uuid

# Page Decorations
st.set_page_config(
    page_title="RFP Tool", page_icon="images/ai-icon.png", layout="centered"
)

# Load the transcripts
@st.cache_data  # 👈 Cached for speed
def write_header():
    st.markdown("*RFP Tool Q & A*")
    st.markdown("---")
    st.markdown("## Instructions")
    st.markdown(
        "Set the Agent ID, Agent Alias ID, and write your question. Press go to get a response."
    )

def run_inference():
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    agent = BedrockAgentRuntimeWrapper(client)

    agent_id = st.session_state["agent_id"]
    agent_alias_id = st.session_state["agent_alias_id"]
    session_id = st.session_state["session_id"]

    response, references = agent.invoke_agent(
        agent_id=agent_id,
        agent_alias_id=agent_alias_id,
        session_id=session_id,
        prompt=st.session_state["input"],
    )

    # Format the references
    formatted_references = format_references(references)

    st.session_state["response_box"] = response
    st.session_state["references_box"] = formatted_references

def format_references(references):
    formatted_references = ""
    for ref in references:
        for retrieved_ref in ref['retrievedReferences']:
            text = retrieved_ref['content']['text']
            uri = retrieved_ref['location']['s3Location']['uri']
            formatted_references += f"{text}\n\n[Link to reference]({uri})\n\n"
    return formatted_references

def main():
    write_header()
    
    # Generate or retrieve a session ID
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    
    st.text_area("Agent ID", key="agent_id")
    st.text_area("Agent Alias ID", key="agent_alias_id")
    st.text_area("Write your RFP Question", key="input")
    st.button("Go", on_click=run_inference)
    st.text_area("Response", key="response_box")
    st.text_area("References", key="references_box")

logger = logging.getLogger(__name__)

class BedrockAgentRuntimeWrapper:
    """Encapsulates Agents for Amazon Bedrock Runtime actions."""

    def __init__(self, runtime_client):
        """
        :param runtime_client: A low-level client representing the Agents for Amazon
                               Bedrock Runtime. Describes the API operations for running
                               inferences using Bedrock Agents.
        """
        self.agents_runtime_client = runtime_client

    def invoke_agent(self, agent_id, agent_alias_id, session_id, prompt):
        """
        Sends a prompt for the agent to process and respond to.

        :param agent_id: The unique identifier of the agent to use.
        :param agent_alias_id: The alias of the agent to use.
        :param session_id: The unique identifier of the session. Use the same value across requests
                           to continue the same conversation.
        :param prompt: The prompt that you want the agent to complete.
        :return: Inference response from the model.
        """
        try:
            response = self.agents_runtime_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
            )

            completion = ""
            references = []

            for event in response.get("completion"):
                chunk = event["chunk"]
                completion += chunk["bytes"].decode()
                references.append(chunk["attribution"]["citations"])

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise

        return completion, references

if __name__ == "__main__":
    main()