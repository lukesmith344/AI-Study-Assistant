import tkinter as tk
from tkinter import ttk
from tkinter import *
import google.generativeai as genai

genai.configure(api_key='AIzaSyCeG_8Uf75LztZJtSekhdBL1pjwH0P4yFc')
model = genai.GenerativeModel('gemini-1.5-flash')



class AIStudyApp:
    """
    A GUI application which acts as an AI study assistant.

    This application allows the user to input notes, specify the number of flashcards, and generate AI powered flashcards
    with explanations when needed by using the Gemini AI model.
    """
    def __init__(self, root):
        """
        Initializes the AIStudyApp with its main window and components.

        Args:
            root: tk.Tk
                The root window of the application
        """
        self.root = root
        self.root.title("AI Study Assistant")
        self.root.geometry('1200x1000')

        # Store generated flashcards
        self.flashcards = []

        # Create main frames
        self.input_frame = ttk.Frame(root)
        self.flashcard_frame = ttk.Frame(root)

        # Set up the screens
        self.setup_input_screen()
        self.setup_flashcard_screen()

        # Show initial screens
        self.show_input_screen()

    def setup_input_screen(self):
        """
        Sets up the input screen where the user can input their notes and select the number of flashcards.

        Creates:
            - Text area for input
            - Spinbox for number of flashcards wanted
            - Button to generate flashcards
        """
        input_label = ttk.Label(self.input_frame, text="Paste your notes here:", font=("Arial", 16))
        input_label.pack(pady=20)

        # Creates text input box
        self.text_input = tk.Text(self.input_frame, width=175, height=50)
        self.text_input.pack(pady=10)

        # Creates frame for flashcard number selection
        number_frame = ttk.Frame(self.input_frame)
        number_frame.pack(pady=5)

        number_label = ttk.Label(number_frame, text='Choose number of flashcards:', font=('Arial', 12))
        number_label.pack(side=tk.LEFT, padx=5)

        # Creates spinbox for flashcard number selection
        self.num_cards = ttk.Spinbox(
            number_frame,
            from_=1,
            to=20,
            width=5,
            state='readonly'
        )
        self.num_cards.set(10)
        self.num_cards.pack(side=tk.LEFT, padx=5)

        # Creates button to switch to the flashcard screen
        notes_button = ttk.Button(self.input_frame, text="Create Flashcards", command=self.show_flashcard_screen)
        notes_button.pack(pady=10)

    def setup_flashcard_screen(self):
        """
        Sets up the flashcard screen where the flashcards will be presented along with a frame for explanation.

        Creates:
            - Frame where flashcards will be shown
            - Buttons for flipping cards, advancing, and going back to the previous card
            - Button for going back to the input screen
            - Frame where an explanation will be shown
            - Button for user to explain the flashcard they are being shown
        """
        # Creates frame for flashcards
        self.card_frame = ttk.Frame(self.flashcard_frame)
        self.card_frame.pack(pady=20, expand=True, fill='both')

        # Creates the text for the flashcards
        self.card_text = ttk.Label(
            self.card_frame,
            text='',
            font=('Arial', 14),
            wraplength=400,
            style='Custom.TLabel'
        )

        style = ttk.Style()
        style.configure(
            'Question.TLabel',
            font=('Arial', 12, 'bold')
        )
        style.configure(
            'Answer.TLabel',
            font=('Arial', 12),
        )
        self.card_text.pack(pady=20)

        # Creates frame for the next, previous, and flip buttons
        button_frame = ttk.Frame(self.flashcard_frame)
        button_frame.pack(pady=10)

        # Creates previous button to go back a card
        self.prev_button = ttk.Button(button_frame, text='Previous', command=self.prev_card)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        # Creates flip button to flip the flashcard
        self.flip_button = ttk.Button(button_frame, text='Flip', command=self.flip_card)
        self.flip_button.pack(side=tk.LEFT, padx=5)

        # Creates next button to advance cards
        self.next_button = ttk.Button(button_frame, text='Next', command=self.next_card)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Creates back button to go back to the input screen
        back_button = ttk.Button(self.flashcard_frame, text="Back", command=self.show_input_screen)
        back_button.pack(pady=10)

        # Creates frame for the explanation
        explain_frame = ttk.Frame(self.flashcard_frame)
        explain_frame.pack(pady=20, expand=True, fill='both')

        # Creates the explanation text
        self.explain_text = ttk.Label(explain_frame, text='')
        self.explain_text.pack(pady=20)

        # Creates button which will explain the current flashcard
        explain_button = ttk.Button(explain_frame, text='Explain', command=self.explain_flashcard)
        explain_button.pack(side=tk.LEFT, padx=5)

        self.current_card_index = 0
        self.showing_question = True

    def show_input_screen(self):
        """
        Shows the input screen to the user.
        """
        self.flashcard_frame.pack_forget()
        self.input_frame.pack()

    def show_flashcard_screen(self):
        """
        Shows the flashcard screen to the user if flashcards have been generated, gives an error if not.
        """
        if self.generate_flashcards():
            self.input_frame.pack_forget()
            self.flashcard_frame.pack()
            self.current_card_index = 0
            self.showing_question = True
            self.update_card_display()
        else:
            error_label = ttk.Label(
                self.input_frame,
                text='Please enter notes for flashcards!',
                font=('Arial', 12),
                foreground='red'
            )
            error_label.pack(pady=5)
            self.root.after(2000, error_label.destroy)
    
    def update_card_display(self):
        """
        Updates the flashcard display by showing the current state of the flashcard.
        """
        if self.flashcards:
            curr_card = self.flashcards[self.current_card_index]
            if self.showing_question:
                self.card_text.config(text=curr_card['question'], style='Question.TLabel')  # Shows question of the current flashcard
            else:
                self.card_text.config(text=curr_card['answer'], style='Answer.TLabel')  # Shows answer of the current flashcard
    
    def flip_card(self):
        """
        Flips the current card.
        """
        self.showing_question = not self.showing_question
        self.update_card_display()
    
    def next_card(self):
        """
        Advances the flashcards.
        """
        if self.flashcards:
            self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)  # Advances the card or wraps back to the beginning
            self.showing_question = True
            self.update_card_display()
        self.explain_text.config(text='')   # Reverts the explanation text to ''
    
    def prev_card(self):
        """
        Goes back to the previous flashcard.
        """
        if self.flashcards:
            self.current_card_index = (self.current_card_index - 1) % len(self.flashcards)  # Goes back to the previous card or wraps around to the end
            self.showing_question = True
            self.update_card_display()
        self.explain_text.config(text='')

    
    def generate_flashcards(self):
        """
        Generates flashcards from the text inputted by the user using the Gemini AI model.

        Returns:
            bool: True if flashcards were successfully generated, false otherwise.

        Note: 
            The generated flashcards are stored in self.flashcards as dictionaries with 'question' and 'answer' keys.
        """
        notes = self.text_input.get('1.0', 'end-1c')
        num_cards = int(self.num_cards.get())

        if notes.strip():
            try:
                # Creates the prompt for the Gemini AI model
                prompt = f"Create exactly {num_cards} of flashcards from these notes. Format each flashcard so it is 'Q: [question]' and 'A: [answer]'. Make the answers simple but still useful for a test. Make sure to spread out the information evenly. Here are the notes: \n\n{notes}"
                response = model.generate_content(prompt)

                # Parse the response into flashcards
                cards_text = response.text.split('\n')
                self.flashcards = []

                current_q = None
                for line in cards_text:
                    if line.startswith('Q:'):
                        current_q = line[2:].strip()
                    elif line.startswith('A:') and current_q:
                        self.flashcards.append({
                            'question': current_q,
                            'answer': line[2:].strip()
                        })
                        current_q = None
                return True
            except Exception as e:
                print(f'Error generating flashcards: {str(e)}')
                return False
        return False
                        
    def explain_flashcard(self):
        """
        Explains the current flashcard to the user.
        """
        if self.flashcards:
            curr_card = self.flashcards[self.current_card_index]
            content = curr_card['question'] + ' ' + curr_card['answer']
            # Creates the prompt for the Gemini AI model to explain the current flashcard
            try:
                prompt = f"Explain this in simple terms. Keep it to 1-3 sentences but make sure to keep it simple and understandable. Here it is: {content}"
                response = model.generate_content(prompt)
                self.explain_text.config(text=response.text)
            except Exception as e:
                self.explain_text.config(text='Error!')

root = tk.Tk()
app = AIStudyApp(root)
root.mainloop()


