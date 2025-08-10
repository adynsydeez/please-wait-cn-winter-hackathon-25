from transformers import logging, AutoModelForCausalLM, AutoTokenizer
import gc
from openai import OpenAI
import config

logging.set_verbosity_error()

TINY_LLM_MODEL_DIRECTORY = "./LLM_model/tiny_llm_weight"
QWEN_MODEL_DIRECTORY = "./LLM_model/qwen2_5_0_5B_instruct_weight"

tiny_llm_tokenizer = AutoTokenizer.from_pretrained(TINY_LLM_MODEL_DIRECTORY)
tiny_llm_model = AutoModelForCausalLM.from_pretrained(TINY_LLM_MODEL_DIRECTORY)
tiny_llm_model.eval()

qwen_tokenizer = AutoTokenizer.from_pretrained(QWEN_MODEL_DIRECTORY)
qwen_model = AutoModelForCausalLM.from_pretrained(
    QWEN_MODEL_DIRECTORY,
    torch_dtype="auto",
    device_map="auto"
)
qwen_model.eval()

client = OpenAI(api_key=config.OPENAI_API_KEY)

def infer(prompt, response, intelligence=1, **kwargs):
    """
    Run inference based on intelligence level:
    1 - tinyLLM
    2 - QWEN
    3 - ChatGPT API
    
    response: dict to store the generated text
    kwargs: additional generation parameters
    """
    if intelligence == 1:
        max_new_tokens = kwargs.get("max_new_tokens", 50)
        temperature = kwargs.get("temperature", 1)
        top_k = kwargs.get("top_k", 50)
        top_p = kwargs.get("top_p", 0.95)

        inputs = tiny_llm_tokenizer.encode(prompt, return_tensors="pt")
        outputs = tiny_llm_model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True
        )
        generated_text = tiny_llm_tokenizer.decode(outputs[0], skip_special_tokens=True)

        del inputs, outputs
        gc.collect()

    elif intelligence == 2:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = qwen_tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = qwen_tokenizer([text], return_tensors="pt").to(qwen_model.device)

        generated_ids = qwen_model.generate(
            **model_inputs,
            max_new_tokens=kwargs.get("max_new_tokens", 50)
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        generated_text = qwen_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        del model_inputs, generated_ids
        gc.collect()

    elif intelligence == 3:
        OpenAI_API_response = client.responses.create(
            model=kwargs.get("model", "gpt-5-nano"),
            instructions="You are an assistant.",
            input=prompt,
            )

        generated_text = OpenAI_API_response.output_text

    else:
        raise ValueError(f"Invalid intelligence level: {intelligence}")

    response["response"] = generated_text
    return generated_text