# urlsummarizer:
Automates fetching, summarizing, and categorizing content from a list of URLs. 

Have too many interesting articles to read? Copy and paste the URL into a Google Sheet to get a convenient summary, helping you decide if you want to dive deeper into the content.

![overview](https://github.com/Brock-Denton/urlsummarizer/blob/main/url.png)

### Description:

It uses a pre-trained transformer model from the Hugging Face library to summarize articles, dynamically categorizes articles based on predefined keywords, and stores the summarized content and its category in a Google Sheet for easy access and organization.

### Key Features:

- **Fetch Content:** Retrieves the raw text from each URL, handling potential request errors gracefully.
- **Summarization:** Utilizes the Hugging Face `transformers` library, specifically the `t5-small` model, to generate concise summaries of the fetched content. This model is trained on a diverse dataset, enabling it to create high-quality summaries across various topics.
- **Categorization:** Dynamically categorizes articles into relevant topics using keyword matching.
- **Google Sheets Integration:** Reads URLs from and writes summaries and categories back to a Google Sheet, ensuring persistent and organized data storage.

### Why Use a Pre-Trained Transformer Model?

The use of a pre-trained transformer model, such as `t5-small`, provides several advantages:

- **Efficiency:** Transformer models can process and summarize large volumes of text quickly and accurately.
- **Quality:** These models are trained on extensive datasets, allowing them to generate high-quality summaries that capture the essence of the original content.
- **Versatility:** The model can handle diverse topics, making it suitable for various articles and documents.

### Comparison to ChatGPT:

While ChatGPT and the `t5-small` model both belong to the family of transformer models developed by OpenAI and Hugging Face, respectively, they serve slightly different purposes:

- **ChatGPT:** Primarily designed for conversational tasks, ChatGPT generates human-like text and engages in dialogues. It can also be used for summarization, but its strength lies in understanding and generating conversational content.
- **t5-small:** Specifically trained for tasks like text summarization, translation, and more, `t5-small` is optimized for summarizing large texts into concise summaries. It is particularly well-suited for applications where brief and accurate content summarization is needed.

### Usage:

Add URLs to the first column of your Google Sheet, run the script, and watch as it fetches, summarizes, categorizes, and updates the sheet with the processed data.

This script is ideal for anyone looking to automate content summarization and categorization tasks, making managing large amounts of information from various sources easier. Its use of a pre-trained transformer model ensures high-quality summaries, making it a powerful tool for information management and analysis. Prospective employers will appreciate the integration of advanced machine learning techniques and practical application in a real-world scenario.

### Setup Instructions:

1. **Clone the Repository:** clone from GitHub.
2. **Install Dependencies:** `pip` install the required libraries.
3. **Configure Google API:** Enable the Google Sheets API, download the credentials, and save them in a file named `credentials.json`.
4. **Generate Token:** Run the script locally to generate a `token.json` file.
5. **Setup Google Sheet:** Replace the `spreadsheet_id` placeholder in the script with your spreadsheet ID.
6. **Run the Script:** Execute the script to process the URLs listed in your Google Sheet.

### Considerations:

- **Alternative APIs:** While this script uses the Hugging Face `t5-small` model for summarization, integrating the ChatGPT API is a straightforward alternative if you prefer using OpenAI's technology. ChatGPT provides robust conversational and summarization capabilities.

- **Automation:** Consider using tools like Zapier or Buildship for enhanced automation. These platforms can automate adding URLs to your Google Sheet and running the summarization script, streamlining your workflow and saving time. You can set up batch processing to handle multiple URLs efficiently.

I chose this setup as it was more cost-effective for the value, and the need for automation on these readings didn't fit my needs. Feel free to integrate these solutions based on your specific needs and preferences.

