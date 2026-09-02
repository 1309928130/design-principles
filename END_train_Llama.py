import os
import json
from transformers import LlamaTokenizer, LlamaForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset, Dataset

def load_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data.append(json.load(f))
    return data

def prepare_dataset(data):
    texts = [item['text'] for item in data]
    return Dataset.from_dict({"text": texts})

# Load the tokenizer and model
tokenizer = LlamaTokenizer.from_pretrained('facebook/llama-7b')
model = LlamaForCausalLM.from_pretrained('facebook/llama-7b')

# Load and prepare your dataset
data = load_json_files('/Users/enshanchen/Downloads/for_design_vocabulary_ principles/generated_json_files')
dataset = prepare_dataset(data)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
)

# Train the model
trainer.train()
