from cement import Controller, ex, shell
from cement.utils.version import get_version_banner
from halo import Halo
from rich import print

from ..core.version import get_version
from questions import get_algorithms, QuestionList
from quiz import algorithm_quiz_chain
from problem_solving import problem_solving_chain

from rich.console import Console
from rich.markdown import Markdown

console = Console()


VERSION_BANNER = """
A collection of tools for practicing data structures and algorithms toy problems. %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


def get_tutor_message(message):
    return f"Tutor 🤖 > {message}"


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "A collection of tools for practicing data structures and algorithms toy problems."

        # text displayed at the bottom of --help output
        epilog = "Usage: toy_problems command1 --foo bar"

        # controller level arguments. ex: 'toy_problems --version'
        arguments = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help="get quizzed about algorithms or data structures",
        # sub-command level arguments. ex: 'toy_problems command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            (
                ["-n", "--num-questions"],
                {
                    "help": "number of questions to ask about the algorithm",
                    "action": "store",
                    "dest": "num_questions",
                },
            ),
        ],
    )
    def quiz(self):
        """Get quizzed about toy problems."""
        n_questions = (
            int(self.app.pargs.num_questions) if self.app.pargs.num_questions else 5
        )
        algos = list(get_algorithms(self.app.db)["name"])
        p = shell.Prompt(
            "What do you want to study?",
            options=algos,
            numbered=True,
        )
        res = p.prompt()

        spinner = Halo(text="Loading your 🤖 tutor...", spinner="dots")

        chain = algorithm_quiz_chain(algo_name=res, n_questions=n_questions)
        # spinner.start()

        # with spinner:
        first_question = chain.predict(human_input="")
        next_question = first_question
        # self.app.log.info("Your tutor: %s" % first_question)
        # print("Your tutor: %s" % first_question)
        # spinner.stop()
        print(get_tutor_message(first_question))

        while n_questions > 0:
            p = shell.Prompt("Your answer > ")
            res = p.prompt()
            next_question = chain.predict(human_input=res)
            self.app.log.info("Your tutor: %s" % next_question)
            n_questions -= 1

        score = chain.predict(human_input="I am done")
        self.app.log.info("Your tutor: %s" % score)

    @ex(
        help="practice solving leetcode problems",
        arguments=[
            (
                ["-d", "--difficulty"],
                {
                    "help": "difficulty of the questions to practice",
                    "action": "store",
                    "dest": "difficulty",
                },
            ),
        ],
    )
    def problem_solving(self):
        """Practice solving a toy problem"""
        questions = QuestionList(self.app.db)
        question = next(questions)
        md = Markdown(question.md)
        console.print(md)

        steps = [
            """
            Step 1. Listen to the problem. Are there any hints in the problem statement?
            """,
            """
            Step 2. Make an example that's large and generic. 
            """,
            """
            Step 3. State the brute force solution.
            """,
            """
            Step 4. Optimize
            """,
            """
            Step 5. Walk through algorithm
            """,
            """
            Step 6. Translate the algorithm into code.
            """,
            """
            Step 7. Verify the correctness of the code.
            """,
        ]

        question_chain = problem_solving_chain(question)

        for step in steps:
            p = shell.Prompt(step)
            step_input = p.prompt()
            tutor_message = question_chain.predict(human_input=step_input)
            print(get_tutor_message(tutor_message))

        # print(next(questions))


### simple user response prompt

# p = shell.Prompt("Press Enter To Continue", default="ENTER")
# res = p.prompt()

# ### provide a numbered list for longer selections


# ### Create a more complex prompt, and process the input


# class MyPrompt(shell.Prompt):
#     class Meta:
#         text = "Do you agree to the terms?"
#         options = ["Yes", "no", "maybe-so"]
#         options_separator = "|"
#         default = "no"
#         clear = True
#         max_attempts = 99

#     def process_input(self):
#         if self.input.lower() == "yes":
#             # do something crazy
#             pass
#         else:
#             # don't do anything... maybe exit?
#             print("User doesn't agree! I'm outa here")


# p = MyPrompt()
