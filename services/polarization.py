import dotenv
from langchain_anthropic import Anthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from typings import RedFlag

ID: int = 4

# Load environment variables
dotenv.load_dotenv()

# LLM
llm: Anthropic = Anthropic(name="haiku")

# Prompt template
prompt = PromptTemplate(
    input_variables=["tweet"],
    template=(
        "You are given a tweet.\n"
        "Your task is to detect polarization and respond with a filled scheme.\n"
        "Here is the definition of polarization:\n\n"
        '"Polarization itself is typically understood as "a prominent division or '
        "conflict that forms between major groups in a society or political system "
        "and that is marked by the clustering and radicalisation of views and "
        'beliefs at two distant and antagonistic poles."\n\n'
        "Here are signs of polarization:\n\n"
        " - Changing consensus: While it can be difficult to recognize, a change "
        "in the collective opinion is a key sign of group polarization. In such cases, "
        "it can be helpful to track the general consensus of the group early in the "
        "process and then compare the end opinion to see how much attitudes have shifted.\n"
        " - Strong attitudes: The intensification of existing opinions is another common "
        "sign of group polarization. Attitudes that were initially more tentative become "
        "harsher as a result of interaction with the group.\n"
        " - Separation from other opinions: As groups become more polarized, they "
        "increasingly separate from others who hold differing points of view. In some "
        "cases, people will go so far as to other or dehumanize members of the outgroup "
        "who don’t share their beliefs or perspectives. As this divide increases, it "
        "becomes even more difficult for people not only to find common ground but "
        "also to empathize with one another.\n"
        " - Increased confirmation bias: As people become increasingly polarized in "
        "their views, they also become more likely to engage in confirmation bias. "
        "This is a type of cognitive bias that involves only giving credence to "
        "information to reinforce the things that they already believe. This means "
        "that people neglect important details that might contradict their views, "
        "leading to poor, biased decision-making.\n"
        " - Greater conflict: During discussions, group members may become more "
        "argumentative and less willing to entertain other ideas. The dominant opinion, "
        "particularly when expressed by persuasive group members, becomes the main "
        "position that other group members increasingly adhere to. As a result, people "
        "become more willing to defend the prevailing perspective, often by arguing "
        "with anyone who tried to introduce contradictory evidence.\n\n"
        "Tweet:\n\n"
        "{tweet}\n\n"
        "The scheme is as follows:\n\n"
        "Polarization: <True/False>\n"
        "Explanation: <Short explanation>"
    ),
)

# Chain
chain = prompt | llm | StrOutputParser()


# Service
def polarization_service(tweet: str) -> list[RedFlag] | None:
    invokation: str = chain.invoke({"tweet": tweet})
    _, polarization, explanation = invokation.split("\n")

    if polarization[14:] == "True":
        return [RedFlag(RedFlagId=ID, Phrase=tweet, Description=explanation[13:])]

    return None
