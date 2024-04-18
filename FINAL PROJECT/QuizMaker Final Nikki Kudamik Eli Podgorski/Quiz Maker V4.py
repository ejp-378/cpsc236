#QUIZMAKER 
#MADE BY ELI PODGORSKI AND NIKKI KUDAMIK

import re
import csv
import random
import time

FILEPATH = "CPSC 236 TestBank - Sheet1.csv"

def get_ID():
    """Prompts the user to enter their ID number and validates it to follow a specific pattern. It allows up 
        to 3 attempts before exiting the program.
       Returns: id_num"""
    pattern = re.compile(r"A[1-9]{5}")
    attempt = 0
    while attempt < 3:
        id_num = input("ID Number: ").strip()
        if pattern.fullmatch(id_num):
            return id_num
        else:
            print("Invalid ID, Make sure your ID starts with 'A', followed by 5 digits [1-9]")
            attempt+=1
    exit("Too many failed attempts")
        
def read_TestBank():
    """Reads questions in from the CSV file, which is located at the variable FILEPATH. It then returns a list 
    of question rows where each row is a list itself, representing one question, its possible answers, and its correct answer
        Returns: a list of all questions"""
    questions = []
    with open(FILEPATH, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            questions.append(row)
    return questions 

def random_Question(questions, number):
    """Args: questions - the list of questions gathered in read_TestBank
             number - number of questions to select from the list questions and use for the quiz
        Selects questions at random, storing them in selected_questions
       Returns: selected_questions"""
    question_order = questions.copy()
    selected_questions = random.sample(question_order, k=number)
    return selected_questions
 
    
def list_Questions(questions, point_value, start_time, time_limit=600):
    """Args:questions - list of questions
            point_value - stores the weight of a question based on num_questions
            start_time - keeps track of the time when you start the quiz
            time_limit = 600 - sets the time limit for the quiz to 10 minutes
        This function runs through the selected questions one at a time, displaying them to the user and recording 
        the users answers. By default it lists two answer choices, but it checks for a third in case the question has 3 choices.
        It also keeps track of the time and calculates the total score. Finally, it gathers information 
        in question_details, to use in a later step
        Returns: total_score, quiz_terminated(True or false value depending on the time of quiz), elapsed_time, and question_details"""
    print()
    index = 1
    total_score = 0
    quiz_terminated = False
    question_details = []
    for question in questions:
        current_time = time.time()
        elapsed_time = round(current_time - start_time, 2)
        if elapsed_time > time_limit:
            quiz_terminated = True
            break
        
        print(f"\n{index}. {question[0]} A. {question[1]}\tB. {question[2]}", end="")
        if len(question) > 3 and question[3]:  
            print(f"\tC. {question[3]}", end="")
        print("\n")
        ans, correct, score = get_Answers(question, point_value)
        total_score += score
        question_details.append((question[0], question[-1], ans))
        index += 1 
    print(f"Your total score is: {total_score}/{len(questions)*point_value}")
    print(f"Elapsed time: {elapsed_time} seconds")
    return total_score, quiz_terminated, elapsed_time, question_details
    


def get_Answers(question, point_value):
    """ Args:question - question from the selected list
             point_value - stores the weight of a quesiton based on num_questions
        This function prompts the user for an answer to a question and ensures the answer is a valid option. It takes the 
        users answer and compares it to the correct answer.It then calculates the score for the quesiton.
        Returns: ans, correct_answer, point_value (1 or .5 if correct, 0 if wrong.) """
    correct_answer = question[-1].upper()
    valid_choices = ['A' , 'B']
    if len(question) > 3 and question[3]:
        valid_choices.append('C')
    
    while True:
        ans = input("Answer: ").upper()
        if ans in valid_choices:
            correct = ans == correct_answer
            return ans, correct_answer, point_value if correct else 0
        else:
            print("Invalid Choice, Please enter one of the listed options.")


def give_Quiz(FILEPATH):
    """Args: FILEPATH
       This is the main function that delivers the quiz. In this function, first_name, last_name, and id is gathered.
       The user is then prompted to select 10 or 20 questions for the quiz. The csv file is then read through, selecting 
       the random questions, and the quiz is then conducted. Quiz timing is handled in this function, including enforcing the time limit. 
       The quiz results are saved to a file, along with information like name, id, score, time elapsed, and the questions. Finally the function 
       gives the option to take another quiz or exit the program"""
    start_time = time.time()
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    student_ID = get_ID()

    num_questions = int(input("Choose the number of questions (10/20): "))
    while num_questions not in [10,20]:
        print("Invalid Choice. Choose 10 or 20 questions. ")
        num_questions = int(input("Choose the number of questions (10/20): "))

    if num_questions == 10:
        point_value = 1
    else: 
        point_value = 0.5
        
    
    questions = read_TestBank()  
    questions = random_Question(questions, num_questions)
    
    total_score, terminated, elapsed_time, question_details = list_Questions(questions, point_value, start_time, time_limit=600)
 
    if terminated:
        print("Quiz terminated. Time limit reached. ")
    else:
        print("Quiz Completed. ")
    
    filename = (f"{student_ID}_{firstName}_{lastName}.txt")
    with open(filename, 'w') as file:
        file.write(f"Student ID: {student_ID}, First Name: {firstName}, Last Name: {lastName}\n")
        file.write(f"Score: {total_score}/{len(questions)*point_value}\n")
        file.write(f"Elapsed Time: {elapsed_time} seconds\n")
        for question, correct_answer, ans, in question_details:
            file.write(f"Question: {question}, Correct Answer: {correct_answer}, Students Answer: {ans}\n")
    
    
    command = input("Enter Q to exit program, or S to start a new quiz: ")
    while True:
        if command.upper() == 'Q':
            print("Exiting Program")
            break
        elif command.upper() == 'S':
            give_Quiz(FILEPATH)
        else:
            print("Invalid Choice, exiting")
            break

if __name__ == "__main__":
    give_Quiz(FILEPATH)