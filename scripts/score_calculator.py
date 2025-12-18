def calculate_score(nova_group, ingredients_tags, labels_tags, additives_tags):
    """
    Calculates the Truth Label Score (0-100).
    Higher score = More sustainable/Healthy.
    """
    # Start with a neutral base
    score = 50.0

    # 1. Labels (High Priority - Official Certifications)
    # Organic and Fair Trade significantly increase the score
    if any(tag in labels_tags for tag in ['en:organic', 'en:eu-organic', 'en:fair-trade']):
        score += 30.0

    # 2. Ingredients Analysis (High Priority)
    # Palm oil is a heavy penalty for sustainability
    if 'en:palm-oil' in ingredients_tags:
        score -= 20.0
    # Vegan/Vegetarian status gives a small sustainability bonus
    if 'en:vegan' in ingredients_tags or 'en:vegetarian' in ingredients_tags:
        score += 5.0

    # 3. NOVA Group (Medium Priority - Industrial Processing)
    # Group 4 (Ultra-processed) is penalized; Group 1 (Unprocessed) is rewarded
    if nova_group == 4:
        score -= 15.0
    elif nova_group == 1:
        score += 10.0

    # 4. Additives (Medium Priority)
    # We count how many additives are present
    additives_list = [a for a in additives_tags.split(',') if a]
    if len(additives_list) > 5:
        score -= 10.0
    elif len(additives_list) > 0:
        score -= 5.0

    # Ensure result is between 0 and 100
    return max(0.0, min(100.0, score))
