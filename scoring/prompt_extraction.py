import logging


from config import AI_BACKEND
if AI_BACKEND == "openai":
    from .oa_models import check_search_prompt, extract_reqs 
elif AI_BACKEND == "ollama":
    from .ollama_models import check_search_prompt, extract_reqs 
else:
    raise ValueError(f"Unknown AI_BACKEND: {AI_BACKEND}. Must be 'ollama' or 'openai'.")
from datamodels.models import WorkflowReqs


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def check_and_extract(prompt: str) -> WorkflowReqs:

    is_search_request = check_search_prompt(prompt)
    print(is_search_request)
    if not is_search_request.is_valid or is_search_request.confidence < 0.7:
        logger.warning(f"Gate check failed, this is not a valid request. {is_search_request.model_dump()}. Exiting")
        exit(1)
    search_data = extract_reqs(prompt)
    return search_data