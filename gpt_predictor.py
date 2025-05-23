from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class GPTNextWordPredictor:
    def __init__(self):
        print("Loading GPT-2 model...")
        self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
        self.model = GPT2LMHeadModel.from_pretrained("distilgpt2")
        self.model.eval()

    def predict_next(self, text, max_length=1):
        if not text.strip():
            return ""
        inputs = self.tokenizer.encode(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + max_length,
                num_return_sequences=1,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id  # avoid warnings
            )
        generated_text = self.tokenizer.decode(outputs[0])
        gen_words = generated_text.strip().split()
        input_words = text.strip().split()
        if len(gen_words) > len(input_words):
            return gen_words[len(input_words)]
        return ""
