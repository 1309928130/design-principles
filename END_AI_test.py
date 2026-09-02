import ollama

stream = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'based on the previous answer, does blue sky mean sunny day?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)





# import ollama
# response = ollama.chat(model='llama3.1', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])