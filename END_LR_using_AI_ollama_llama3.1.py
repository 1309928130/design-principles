# import os
# import json
# import sh
#
# # Define the directory containing your JSON articles and where to save the summaries
# articles_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/generated_json_files"
# summaries_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/ai_results"
#
# # Ensure the summaries directory exists
# os.makedirs(summaries_directory, exist_ok=True)
#
# # Define the prompt to use with the content
# prompt = "For the above text (it is part of an article), please help me color different contents in " \
#          "different colors (see the following) in latex format. Do NOT change the original text of the " \
#          "article, and only give me the content between \begin{document} and \end{document}. - Red: research " \
#          "questions/problems/issues - Purple: Objectives/aims/intentions/motivations - Green: Research methods " \
#          "- Cyan: Assess* + framework/matrix/... - Blue: Design concepts/vocabulary/principles/guidelines/patterns..."
#
#
# # Function to summarize an article using the Llama model locally
# def summarize_article(content):
#     full_input = f"{prompt}{content}"
#     try:
#         # Using sh to run the command and capture output
#         result = sh.ollama("run", "llama3.1", _in=full_input)
#         return result.strip()  # `result` is a string
#     except sh.ErrorReturnCode as e:
#         print(f"Error summarizing content: {e.stderr.decode()}")
#         return "Error in summarization"
#
# # Function to chunk text to respect token limits
# def chunk_text(text, chunk_size=6000):
#     if text is None:
#         return []
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield ' '.join(words[i:i + chunk_size])
#
# # Summarize an article with respect to token limits
# def summarize_article_with_chunks(content):
#     summaries = []
#     for chunk in chunk_text(content):
#         print(f"Processing chunk of size {len(chunk)}")
#         summary = summarize_article(chunk)
#         summaries.append(summary)
#     return ' '.join(summaries)
#
# # Iterate through each JSON file in the directory
# for filename in os.listdir(articles_directory):
#     if filename.endswith('.json'):
#         try:
#             with open(os.path.join(articles_directory, filename), 'r') as file:
#                 article = json.load(file)
#                 title = article.get("title", "Untitled")
#                 content = article.get("text")  # Adjusted to use "text" key
#                 if content is None:
#                     print(f"Skipping article {title} as it has no content.")
#                     continue
#
#                 print(f"Summarizing article: {title}")
#
#                 # Summarize the article content
#                 summary = summarize_article_with_chunks(content)
#                 print(f"Summary: {summary}")
#                 print('-' * 80)
#
#                 # Save the summary to a new JSON file
#                 summary_filename = os.path.join(summaries_directory, f"summary_{filename}")
#                 with open(summary_filename, 'w') as summary_file:
#                     json.dump({"title": title, "summary": summary}, summary_file, indent=4)
#         except json.JSONDecodeError as e:
#             print(f"Error reading JSON file {filename}: {e}")
#         except Exception as e:
#             print(f"An unexpected error occurred while processing {filename}: {e}")
# #

#







import os
import csv
import ollama

# Define the directory containing your CSV articles and where to save the summaries
articles_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/csv_test"
summaries_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/ai_results"

# Ensure the summaries directory exists
os.makedirs(summaries_directory, exist_ok=True)

# Define the prompt to use with the content
prompt = (""" 
!!! For the above text, which is (part of) an article), please help me color different contents in 
different colors (see the following) in Latex format. Do NOT change the original text of the 
article, and only give me the content between \\begin{document} and \\end{document} (exclude them).!!!

- Red: research questions/problems/issues 
- Purple: Objectives/aims/intentions/motivations 
- Green: Research methods 
- Cyan: Assess* + framework/matrix/... 
- Blue: Design concepts/vocabulary/principles/guidelines/patterns...
"""
)

# Function to summarize an article using the Llama model locally
def summarize_article(content): # input 6th
    full_input = f"{prompt}\n\n{content}"
    try:
        response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'user',
                'content': full_input,
            },
        ])

        result = response['message']['content']
        print(result)

        return result

    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Error in summarization"

# Function to chunk text to respect token limits
def chunk_text(text, chunk_size=1000):  # input 5th #这是1000单词的数目
    if text is None:
        return []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

# Summarize an article with respect to token limits
def summarize_article_with_chunks(content):  # input 4th
    summaries = []
    for chunk in chunk_text(content):
        print(f"Processing chunk of size {len(chunk)}") #这是字母的数目
        summary = summarize_article(chunk)
        print(summary)
        summaries.append(summary)
    return ' '.join(summaries)

# Iterate through each CSV file in the directory
for filename in os.listdir(articles_directory): # input - 1st step
    if filename.endswith('.csv'):
        try:
            with open(os.path.join(articles_directory, filename), 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    content = row[0] if len(row) > 0 else None # Adjust to match the CSV column name # input - 2nd
                    if content is None:
                        print("Skipping article as it has no content.")
                        continue

                    print(f"Summarizing article {i + 1} in file: {filename}")

                    # Summarize the article content
                    summary = summarize_article_with_chunks(content)  # input -3rd
                    print(f"Summary: {summary}")
                    print('-' * 80)

                    # Write the summary to a separate file
                    summary_file_path = os.path.join(summaries_directory, f"{os.path.splitext(filename)[0]}_summary_{i + 1}.txt")
                    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                        summary_file.write(summary)

        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")

print(f"Summaries have been saved to {summaries_directory}")


















# import os
# import json
# import sh
#
# # Define the directory containing your JSON articles and where to save the summaries
# articles_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/generated_json_files"
# summaries_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/ai_results"
#
# # Ensure the summaries directory exists
# os.makedirs(summaries_directory, exist_ok=True)
#
# # Define the prompt to use with the content
# prompt = "Please summarize the following content's problems, methods, results, implications:"
#
# # Function to summarize an article using the Llama model locally
# def summarize_article(content):
#     full_input = f"{prompt}{content}"
#     try:
#         # Using sh to run the command and capture output
#         result = sh.ollama("run", "llama3.1", _in=full_input)
#         return result.strip()  # `result` is a string
#     except sh.ErrorReturnCode as e:
#         print(f"Error summarizing content: {e.stderr.decode()}")
#         return "Error in summarization"
#
# # Function to chunk text to respect token limits
# def chunk_text(text, chunk_size=6000):
#     if text is None:
#         return []
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield ' '.join(words[i:i + chunk_size])
#
# # Summarize an article with respect to token limits
# def summarize_article_with_chunks(content):
#     summaries = []
#     for chunk in chunk_text(content):
#         print(f"Processing chunk of size {len(chunk)}")
#         summary = summarize_article(chunk)
#         summaries.append(summary)
#     return ' '.join(summaries)
#
# # Prepare the Markdown file
# markdown_file_path = os.path.join(summaries_directory, 'summaries.md')
# with open(markdown_file_path, 'w', encoding='utf-8') as markdownfile:
#     markdownfile.write('# Summaries\n\n')  # Write the header of the Markdown file
#
#     # Iterate through each JSON file in the directory
#     for filename in os.listdir(articles_directory):
#         if filename.endswith('.json'):
#             try:
#                 with open(os.path.join(articles_directory, filename), 'r') as file:
#                     article = json.load(file)
#                     title = article.get("title", "Untitled")
#                     content = article.get("text")  # Adjusted to use "text" key
#                     if content is None:
#                         print(f"Skipping article {title} as it has no content.")
#                         continue
#
#                     print(f"Summarizing article: {title}")
#
#                     # Summarize the article content
#                     summary = summarize_article_with_chunks(content)
#                     print(f"Summary: {summary}")
#                     print('-' * 80)
#
#                     # Write the summary to the Markdown file
#                     markdownfile.write(f'## {title}\n\n')  # Title in Markdown
#                     markdownfile.write(f'{summary}\n\n')  # Summary content
#             except json.JSONDecodeError as e:
#                 print(f"Error reading JSON file {filename}: {e}")
#             except Exception as e:
#                 print(f"An unexpected error occurred while processing {filename}: {e}")
#
# print(f"Summaries have been saved to {markdown_file_path}")









#
#
# import os
# import json
# import sh
#
# # Define the directory containing your JSON articles and where to save the summaries
# articles_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/generated_json_files"
# summaries_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/ai_results"
#
# # Ensure the summaries directory exists
# os.makedirs(summaries_directory, exist_ok=True)
#
# # Define the prompt for summarizing individual articles and for analyzing combined summaries
# summary_prompt = "Please summarize the following content's problems, methods, results, implications:"
# analysis_prompt = "Please analyze the following summaries and identify key themes, patterns, and insights:"
#
#
# # Function to summarize an article using the Llama model locally
# def summarize_article(content):
#     full_input = f"{summary_prompt}{content}"
#     try:
#         result = sh.ollama("run", "llama3.1", _in=full_input)
#         return result.strip()  # `result` is a string
#     except sh.ErrorReturnCode as e:
#         print(f"Error summarizing content: {e.stderr.decode()}")
#         return "Error in summarization"
#
#
# # Function to chunk text to respect token limits
# def chunk_text(text, chunk_size=6000):
#     if text is None:
#         return []
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield ' '.join(words[i:i + chunk_size])
#
#
# # Summarize an article with respect to token limits
# def summarize_article_with_chunks(content):
#     summaries = []
#     for chunk in chunk_text(content):
#         print(f"Processing chunk of size {len(chunk)}")
#         summary = summarize_article(chunk)
#         summaries.append(summary)
#     return ' '.join(summaries)
#
#
# # Prepare the Markdown file
# markdown_file_path = os.path.join(summaries_directory, 'summaries.md')
# with open(markdown_file_path, 'w', encoding='utf-8') as markdownfile:
#     markdownfile.write('# Summaries\n\n')  # Write the header of the Markdown file
#
#     summaries = []
#
#     # Iterate through each JSON file in the directory
#     for filename in os.listdir(articles_directory):
#         if filename.endswith('.json'):
#             try:
#                 with open(os.path.join(articles_directory, filename), 'r') as file:
#                     article = json.load(file)
#                     title = article.get("title", "Untitled")
#                     content = article.get("text")  # Adjusted to use "text" key
#                     if content is None:
#                         print(f"Skipping article {title} as it has no content.")
#                         continue
#
#                     print(f"Summarizing article: {title}")
#
#                     # Summarize the article content
#                     summary = summarize_article_with_chunks(content)
#                     print(f"Summary: {summary}")
#                     print('-' * 80)
#
#                     # Write the summary to the Markdown file
#                     markdownfile.write(f'## {title}\n\n')  # Title in Markdown
#                     markdownfile.write(f'{summary}\n\n')  # Summary content
#
#                     summaries.append(summary)
#             except json.JSONDecodeError as e:
#                 print(f"Error reading JSON file {filename}: {e}")
#             except Exception as e:
#                 print(f"An unexpected error occurred while processing {filename}: {e}")
#
# print(f"Summaries have been saved to {markdown_file_path}")
#
# # Combine all summaries into a single text
# combined_summaries = "\n\n".join(summaries)
#
#
# # Function to analyze the combined summaries using Llama
# def analyze_summaries(content):
#     full_input = f"{analysis_prompt}{content}"
#     try:
#         result = sh.ollama("run", "llama3.1", _in=full_input)
#         return result.strip()  # `result` is a string
#     except sh.ErrorReturnCode as e:
#         print(f"Error analyzing summaries: {e.stderr.decode()}")
#         return "Error in analysis"
#
#
# # Analyze the combined summaries
# analysis = analyze_summaries(combined_summaries)
#
# # Save the analysis to a Markdown file
# analysis_file_path = os.path.join(summaries_directory, 'analysis.md')
# with open(analysis_file_path, 'w', encoding='utf-8') as analysis_file:
#     analysis_file.write('# Analysis of Summaries\n\n')  # Write the header of the Markdown file
#     analysis_file.write(f'{analysis}\n')  # Analysis content
#
# print(f"Analysis has been saved to {analysis_file_path}")
