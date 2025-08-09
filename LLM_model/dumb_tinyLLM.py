from transformers import logging, AutoModelForCausalLM, AutoTokenizer

# Set the logging level to suppress warnings and information messages
logging.set_verbosity_error()

MODEL_DIRECTORY = "./LLM_model/tiny_llm_weight"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIRECTORY)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIRECTORY)
model.eval()

def tinyLLM_infer(prompt, max_new_tokens=2, temperature=1, top_k=50, top_p=0.95):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True
    )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text