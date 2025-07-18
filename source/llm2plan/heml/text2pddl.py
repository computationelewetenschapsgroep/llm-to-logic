import l2p
from l2p import DomainBuilder, TaskBuilder, PromptBuilder, FeedbackBuilder
from l2p.utils import format_expression, load_file
from l2p.llm.huggingface import HUGGING_FACE
from l2p.utils import format_types
import os

domain_builder = DomainBuilder()

llama_3b = HUGGING_FACE(
    model="Llama-3.2-1B-Instruct",
    model_path="meta-llama/Llama-3.2-1B-Instruct",
    config_path="/usr/local/lib/python3.10/site-packages/l2p/llm/utils/llm.yaml",
    #api_key= os.environ["API_KEY"]
)

domain_builder = DomainBuilder()

types_prompt = PromptBuilder(
    role="You are a PDDL assistant that is helping me design :types.",
    format=load_file("/Users/aniket.mitra/Documents/l2p/templates/domain_templates/formalize_type.txt"),
    task="{domain_desc}"
)

domain_desc = "The AI agent here is a mechanical robot arm that can pick and " \
    "place the blocks. Only one block may be moved at a time: it may either " \
    "be placed on the table or placed atop another block. Because of this, " \
    "any blocks that are, at a given time, under another block cannot be moved."


# extract types via LLM
types, llm_output, validation_info = domain_builder.formalize_types(
    model=llama_3b,
    domain_desc=domain_desc,
    prompt_template=types_prompt.generate_prompt()
    )

# print out types
print(format_types(types=types))