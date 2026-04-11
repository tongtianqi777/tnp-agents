Build agent

in the dir xjqq-download-agent, create the code and documentation for an AI agent built with langchain.

The agent is a worker that executes the following workflow:
- use a picture of a book as an input (the picture is provided as a local absolute path)
- use OpenAI API to recognize the title of the book (the book title can be in both Chinese and English). use the proper OpenAI model for this task.
- return the recognized title of the book as text. do not return any other text.

Write all the prompts (including system prompt) and tools as necessary.
Use placeholders for API keys.
