import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typings import RedFlag

ID: int = 2

# Define a list of clickbait words/phrases
CLICKBAIT_PHRASES: list[str] = [
    "Amazing",
    "Unbelievable",
    "Shocking",
    "Incredible",
    "Mind-blowing",
    "Jaw-dropping",
    "Breathtaking",
    "Epic",
    "Insane",
    "Outrageous",
    "Unimaginable",
    "Miraculous",
    "Astonishing",
    "Unstoppable",
    "Phenomenal",
    "Life-changing",
    "Spectacular",
    "Ultimate",
    "Revolutionary",
    "Crazy",
    "Surprising",
    "Unthinkable",
    "Unprecedented",
    "Unreal",
    "Stunning",
    "Horrifying",
    "Heartbreaking",
    "Heartwarming",
    "Tear-jerking",
    "Fascinating",
    "Unforgettable",
    "Inspiring",
    "Heroic",
    "Unparalleled",
    "Groundbreaking",
    "Mind-boggling",
    "World-changing",
    "Exclusive",
    "Extraordinary",
    "Unstoppable",
    "Explosive",
    "Sensational",
    "Greatest",
    "Unbeatable",
    "Legendary",
    "Outrageous",
    "Must-see",
    "Unrivaled",
    "Furious",
    "Devastating",
    "Incomparable",
    "Flawless",
    "Unstoppable",
    "Skyrocketing",
    "Devastating",
    "Scary",
    "Fearless",
    "Infallible",
    "Game-changer",
    "Irresistible",
    "Life-saving",
    "Breakthrough",
    "Jaw-dropping",
    "Devastating",
    "Shocking",
    "Frightening",
    "Mind-bending",
    "Explosive",
    "Unprecedented",
    "Top",
    "Best",
    "Biggest",
    "Fastest",
    "Hottest",
    "Rarest",
    "Ultimate",
    "Secret",
    "Hidden",
    "Guaranteed",
    "Proven",
    "Limited",
    "Fast",
    "Now",
    "Instantly",
    "Hurry",
    "New",
    "Crazy",
    "Wild",
    "Powerful",
    "Urgent",
    "Free",
    "Exclusive",
    "Never",
    "Now",
    "Final",
    "Last",
    "Urgent",
    "Instant",
    "Bonus",
    "Free",
    "Best-selling",
    "Record-breaking",
    "!!!",
]


# Function to detect and flag clickbait words in a text
def detect_clickbait(text: str) -> list[tuple[str, str]]:
    flagged_info: list[tuple[str, str]] = []
    # Split the text into sentences
    sentences: list[str] = re.split(r"(?<=[.!?]) +", text)

    for sentence in sentences:
        # Check if any clickbait phrase is present in the sentence
        for phrase in CLICKBAIT_PHRASES:
            if re.search(r"\b" + re.escape(phrase) + r"\b", sentence, re.IGNORECASE):
                # Append the flagged sentence and the triggering word/phrase
                flagged_info.append((sentence, phrase))
                break  # Only append once per sentence

    return flagged_info


# Function to analyze sentiment using VADER
def analyze_sentiment(flagged_info: list[tuple[str, str]]) -> list[RedFlag]:
    """
    Marks sentance with 1 if the sentiment is positive, 0 if the sentiment is negative
    """

    analyzer = SentimentIntensityAnalyzer()
    sentiment_results: list[RedFlag] = []

    for sentence, phrase in flagged_info:
        sentiment: dict[str, float] = analyzer.polarity_scores(sentence)

        if sentiment["neg"] > 0.5 or sentiment["pos"] > 0.5:
            sentiment_results.append(RedFlag(RedFlagId=ID, Phrase=phrase))

    return list(set(sentiment_results))


def emotional_clickbait_service(tweet: str) -> list[RedFlag] | None:
    words: list[RedFlag] = analyze_sentiment(detect_clickbait(tweet))

    return words if len(words) > 0 else None
