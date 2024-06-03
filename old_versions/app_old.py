import streamlit as st
import boto3
from botocore.exceptions import ClientError
import logging

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
        "Set the Agent ID, Agent Alias ID, and Session ID. Write your question and press go."
    )

def run_inference():
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    agent = BedrockAgentRuntimeWrapper(client)

    agent_id = st.session_state.get("agent_id", "")
    agent_alias_id = st.session_state.get("agent_alias_id", "")
    session_id = st.session_state.get("session_id", "")

    if not agent_id or not agent_alias_id or not session_id:
        st.error("Please provide all the required IDs.")
        return

    response, references = agent.invoke_agent(
        agent_id=agent_id,
        agent_alias_id=agent_alias_id,
        session_id=session_id,
        prompt=st.session_state.get("input", ""),
    )

    st.session_state["response_box"] = response
    st.session_state["references_box"] = format_references(references)

def format_references(references):
    formatted_references = ""
    for ref in references:
        for retrieved_ref in ref.get('retrievedReferences', []):
            text = retrieved_ref.get('content', {}).get('text', 'No text')
            uri = retrieved_ref.get('location', {}).get('s3Location', {}).get('uri', '#')
            formatted_references += f"[{text}]({uri})\n\n"
    return formatted_references

def main():
    write_header()
    st.text_area("Agent ID", key="agent_id")
    st.text_area("Agent Alias ID", key="agent_alias_id")
    st.text_area("Session ID", key="session_id")
    st.text_area("Write your RFP Question", key="input")
    st.button("Go", on_click=run_inference)
    st.text_area("Response", key="response_box", height=200)
    st.text_area("References", key="references_box", height=200)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

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

            logging.debug(f"Full response: {response}")

            completion = response.get("trace", {}).get("failureTrace", {}).get("failureReason", "No response")
            references = response.get("trace", {}).get("retrievedReferences", [])

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise

        return completion, references

if __name__ == "__main__":
    main()
