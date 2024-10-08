import re
from typings import RedFlag

ID: int = 1

WAT_PATTERNS: dict[str, str] = {
    "what about...?": r"\bwhat about\b.*\?",
    "as for...": r"\bas for\b.*\ ",
    "how about...?": r"\bhow about\b.*\?",
    "why don’t (somebody) mention...?": r"\bwhy (don’t|didn’t|won’t) ((\w+)|(\w+)\s(\w+)) mention\b.*\?",
    "but (somebody) never mention...": r"\bbut ((\w+)|(\w+)\s(\w+)) never mention\b.* ",
    "what do (somebody) have to say about...?": r"\bwhat (do|does) ((\w+)|(\w+)\s(\w+)) (have|has) to say about\b.*\?",
    "why are (somebody) not talking about...?": r"\bwhy (are|is) ((\w+)|(\w+)\s(\w+)) not talking about\b.*\?",
    "how can (somebody) ignore...?": r"\bhow can ((\w+)|(\w+)\s(\w+)) ignore\b.*\?",
}


# Function to detect the phrase "What about...?" and return a warning
def whataboutism_service(tweet: str) -> list[RedFlag] | None:
    sentences = re.split(r"(?<=[.!?]) +", tweet)

    whataboutism_sentances: list[RedFlag] = []

    for sentance in sentences:
        for _, pattern in WAT_PATTERNS.items():
            if re.search(pattern, sentance, re.IGNORECASE):
                whataboutism_sentances.append(RedFlag(RedFlagId=ID, Phrase=sentance))

    return whataboutism_sentances if len(whataboutism_sentances) > 0 else None
