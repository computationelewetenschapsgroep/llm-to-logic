import l2p
from l2p import DomainBuilder, TaskBuilder, PromptBuilder, FeedbackBuilder
from l2p.utils import format_expression, load_file
from l2p.llm.llama import LLAMA
from l2p.utils import format_types, format_actions, format_params
import os
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

domain_builder = DomainBuilder()

llama_3b = LLAMA(
    model="llama3.2:1b",
    config_path="/usr/local/lib/python3.10/site-packages/l2p/llm/utils/llm.yaml",
    #api_key= os.environ["API_KEY"]
)

domain_builder = DomainBuilder()

idx = 0
while True:
    if idx > 100:
        break
    idx += 1
    types_prompt = PromptBuilder(
        role="You are a PDDL assistant that is helping me design :types.",
        format=load_file("./prompts/template/formalize_type.txt"),
        task="{domain_desc}"
    )


    # domain_desc = "The AI agent here is a mechanical robot arm that can pick and " \
    #     "place the blocks. Only one block may be moved at a time: it may either " \
    #     "be placed on the table or placed atop another block. Because of this, " \
    #     "any blocks that are, at a given time, under another block cannot be moved."


    domain_desc = "The AI agent here is a transporter that can move " \
        "equipment from one location to another." 

    # extract types via LLM
    types, llm_output, validation_info = domain_builder.formalize_types(
        model=llama_3b,
        domain_desc=domain_desc,
        prompt_template=types_prompt.generate_prompt(),
        types={"Equipment": "Equipment to be moved", 
               "Pickup Location": "Location where equipment can be picked up",
               "Dropoff Location": "Location where equipment can be dropped off",
               "Transporter": "Transporter that moves equipment"}
        )

    # print out types
    logger.info(f"Iteration {idx} , Extracted Types: {format_types(types=types)}")

idx = 0 
while True:
    if idx > 100:
        break
    idx += 1 
    actions_prompt = PromptBuilder(
        role="You are a PDDL assistant that is helping me design :actions.",
        format=load_file("/Users/aniket.mitra/Documents/l2p/templates/domain_templates/formalize_parameters.txt"),
        task="{domain_desc}"
    )


    param, param_raw, llm_output, validation_info = domain_builder.formalize_parameters(
        model=llama_3b,
        domain_desc=domain_desc,
        prompt_template=actions_prompt.generate_prompt(),
        action_name=""
    )
    logger.info(f"Iteration {idx}, Extracted Parameters: {format_params(parameters=param)}")