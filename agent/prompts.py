def aspiration_prompt(aspirations):
    return f"""
    Based on the aspirations: {', '.join(aspirations)}
    Classify intent as one of: startup_tech, ai_learning, career_growth, creative_inspo, explore
    Return only one category name.
    """
