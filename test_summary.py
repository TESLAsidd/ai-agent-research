from modules.ai_summarizer import AISummarizer

# Test the summarize_content method
summarizer = AISummarizer()

test_content = """
Artificial intelligence has made significant advances in 2024 with new developments in machine learning and natural language processing. 
Companies are investing heavily in AI research and development. New AI models show improved accuracy and efficiency.
The market for AI technologies is expected to grow substantially in the coming years.
"""

result = summarizer.summarize_content(test_content, "AI trends 2024")

print("Testing summarize_content method:")
print(f"Success: {result.get('success')}")
print(f"Provider: {result.get('provider')}")
if result.get('error'):
    print(f"Error: {result.get('error')}")
print(f"Summary: {result.get('summary', 'N/A')[:300]}...")