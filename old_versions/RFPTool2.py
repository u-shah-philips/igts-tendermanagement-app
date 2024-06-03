import streamlit as st
import boto3
from botocore.exceptions import ClientError
import logging

# Page Decorations
st.set_page_config(
    page_title="RFP Tool", page_icon="images/ai-icon.png", layout="centered"
)

# Hardcoded values
AGENT_ID = "LO4PSB8ZVQ"
AGENT_ALIAS_ID = "YGV9XE6DRY"

# Load the transcripts
@st.cache_data  # 👈 Cached for speed
def write_header():
    st.markdown("*RFP Tool Q & A*")
    st.markdown("---")
    st.markdown("## Instructions")
    st.markdown(
        "Set the Session ID and write your question. Press go."
    )

def run_inference():
    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    agent = BedrockAgentRuntimeWrapper(client)

    session_id = st.session_state["session_id"]

    response, references = agent.invoke_agent(
        agent_id=AGENT_ID,
        agent_alias_id=AGENT_ALIAS_ID,
        session_id=session_id,
        prompt=st.session_state["input"],
    )
    print("ref" + str(references))
    
    summarized_references, citations = format_references(references)
    st.session_state["response_box"] = response
    st.session_state["summarized_references_box"] = summarized_references
    st.session_state["citations_links"] = citations

def format_references(references):
    summarized_references = ""
    citations = []
    for ref in references:
        for retrieved_ref in ref.get('retrievedReferences', []):
            text = retrieved_ref.get('content', {}).get('text', 'No text')
            uri = retrieved_ref.get('location', {}).get('s3Location', {}).get('uri', '#')
            summarized_references += f"{text}\n\n"
            citations.append(uri)
    return summarized_references, citations

def main():
    write_header()
    st.text_area("Agent ID", AGENT_ID, key="agent_id", disabled=True)
    st.text_area("Agent Alias ID", AGENT_ALIAS_ID, key="agent_alias_id", disabled=True)
    st.text_area("Session ID", key="session_id")
    st.text_area("Write your RFP Question", key="input")
    st.button("Go", on_click=run_inference)
    st.text_area("Response", key="response_box")
    st.text_area("Summarized References", key="summarized_references_box")
    
    # Display citations as hyperlinks
    if "citations_links" in st.session_state:
        st.markdown("## Citations")
        for i, citation in enumerate(st.session_state["citations_links"], 1):
            st.markdown(f"[Citation {i}]({citation})")

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

            for event in response.get("completion", []):
                chunk = event.get("chunk", {})
                completion += chunk.get("bytes", b"").decode()
                references.extend(chunk.get("attribution", {}).get("citations", []))

        except ClientError as e:
            logger.error(f"Couldn't invoke agent. {e}")
            raise

        return completion, references

if __name__ == "__main__":
    main()