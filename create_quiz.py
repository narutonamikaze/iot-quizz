import PyPDF2
import random
import re

# Extract text from PDF
pdf_path = r"Merged IIOT Assignments.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
except Exception as e:
    print(f"Error reading PDF: {e}")
    exit(1)

# Parse questions - look for common patterns
# Split by common question indicators
questions = []

# Pattern 1: Questions starting with numbers followed by period (1. 2. etc.)
pattern1 = re.findall(r'\d+\.\s+[A-Z][^?]*\?', text)

# Pattern 2: Questions marked with "Q:" or "Question:"
pattern2 = re.findall(r'[Qq](?:uestion)?:?\s+([^?]+\?)', text)

# Pattern 3: General sentence ending with question mark
pattern3 = re.findall(r'[A-Z][^.!?]*\?', text)

# Combine all found patterns
all_questions = pattern1 + pattern2 + pattern3

# Clean up questions
cleaned_questions = []
for q in all_questions:
    q = q.strip()
    if len(q) > 10 and len(q) < 500:  # Filter out too short or too long entries
        if q not in cleaned_questions:  # Remove duplicates
            cleaned_questions.append(q)

print(f"Found {len(cleaned_questions)} questions")

# If we don't have enough questions, generate them from key terms
if len(cleaned_questions) < 50:
    # Extract key terms and concepts
    words = text.split()
    
    # Find sentences with technical terms
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and len(sentence) < 300:
            # Convert to question format
            if not sentence.endswith('?'):
                # Try to make it a question
                if any(keyword in sentence.lower() for keyword in ['what', 'how', 'why', 'when', 'where', 'which']):
                    if sentence not in cleaned_questions:
                        cleaned_questions.append(sentence + "?")
            else:
                if sentence not in cleaned_questions:
                    cleaned_questions.append(sentence)

print(f"After processing: {len(cleaned_questions)} questions")

# Ensure we have at least 50 questions
if len(cleaned_questions) < 50:
    print(f"Only found {len(cleaned_questions)} unique questions. Creating a quiz with available questions.")
    quiz_questions = cleaned_questions
else:
    # Select 50 random questions
    quiz_questions = random.sample(cleaned_questions, 50)

# Sort for consistency
quiz_questions.sort()

# Create quiz file
output_file = "IoT_Quiz_50_Questions.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("IoT ASSIGNMENT QUIZ - 50 RANDOM QUESTIONS\n")
    f.write("=" * 80 + "\n\n")
    
    for i, question in enumerate(quiz_questions, 1):
        f.write(f"{i}. {question}\n")
        f.write("\n")
        f.write("Your Answer: _" + "_" * 70 + "\n\n")

print(f"\nQuiz created successfully!")
print(f"Total questions in quiz: {len(quiz_questions)}")
print(f"Quiz saved to: {output_file}")
