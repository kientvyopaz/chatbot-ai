import random
import nltk
from tensorflow.keras.models import load_model
# import tensorflow as tf

# Load pre-trained model for text generation
model = load_model('model.h5')

# Load Vietnamese tokenizer
with open('tokenizer_vietnamese.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Define a function to generate a poem
def generate_poem(seed_text):
    generated = ''
    while True:
        # Tokenize the seed text
        encoded = tokenizer.texts_to_sequences([seed_text])[0]
        encoded = pad_sequences([encoded], maxlen=20, truncating='pre')

        # Predict the next word
        y_pred = model.predict_classes(encoded)

        # Convert predicted word to text
        predicted_word = ''
        for word, index in tokenizer.word_index.items():
            if index == y_pred:
                predicted_word = word
                break

        # Stop generating text if end-of-line token is generated
        if predicted_word == 'EOL':
            break

        # Add predicted word to the generated text
        generated += predicted_word + ' '

        # Update the seed text
        seed_text += ' ' + predicted_word

    return generated

# Define a function to handle user input and generate a response
def get_response(input_text):
    input_text = input_text.lower()

    # Check if user input is a question
    if input_text.endswith('?'):
        responses = ['Chắc vậy!', 'Tôi không chắc lắm.', 'Không chắc chắn.', 'Có lẽ đúng.', 'Có lẽ không.']
        return random.choice(responses)
    
    # Check if user input is a greeting
    if input_text.startswith('xin chào') or input_text.startswith('chào'):
        return 'Xin chào! Tôi là một chat bot, tôi có thể làm thơ cho bạn nếu bạn muốn.'

    # Generate a poem based on user input
    return generate_poem(input_text)

# Start the chat bot
print('Xin chào! Tôi là chat bot của bạn. Hãy gõ câu hỏi hoặc lời chào để bắt đầu.')
while True:
    user_input = input('> ')
    response = get_response(user_input)
    print(response)
