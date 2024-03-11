import json

def load_knowledge_base(file_path):
    """
    Load the knowledge base from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file containing the knowledge base.

    Returns:
    - dict: The loaded knowledge base represented as a dictionary.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def diagnose(symptoms, rules):
    """
    Diagnose the plant disease based on symptoms and rules.

    Parameters:
    - symptoms (dict): A dictionary containing symptoms and their severities.
    - rules (list): A list of rules representing conditions and conclusions.

    Returns:
    - list: A sorted list of tuples containing the diagnoses and their probabilities.
    """
    probabilities = {}

    # Iterate through each rule to calculate probabilities
    for rule in rules:
        severity_scores, correlated_scores = [], []
        # Calculate severity scores for each condition in the rule
        for condition, expected_severity in rule["conditions"].items():
            if condition in symptoms:
                severity_difference = abs(expected_severity - symptoms[condition])
                severity_scores.append(1 - severity_difference)  # Score based on closeness

        # Calculate correlated scores for each correlated symptom in the rule
        for correlated_symptom in rule.get("correlated_symptoms", []):
            if correlated_symptom in symptoms:
                correlated_scores.append(1)  # Full score if correlated symptom is present

        # Calculate final score for the rule
        if severity_scores:
            severity_score = sum(severity_scores) / len(rule["conditions"])
            correlated_score = sum(correlated_scores) / len(rule["correlated_symptoms"]) if rule["correlated_symptoms"] else 0
            final_score = (severity_score + correlated_score) / 2  # Averaging both scores
            probabilities[rule["conclusion"]] = probabilities.get(rule["conclusion"], 0) + final_score * rule["confidence"]

    # Normalize probabilities
    total_probability = sum(probabilities.values())
    for conclusion in probabilities:
        probabilities[conclusion] /= total_probability if total_probability else 1  # Avoid division by zero

    # Sort diagnoses based on probabilities
    return sorted(probabilities.items(), key=lambda item: item[1], reverse=True)

def main():
    knowledge_base_path = 'knowledge_base.json' 
    rules = load_knowledge_base(knowledge_base_path)
    
    print("Welcome to the Plant Disease Diagnosis Expert System")
    print("Enter your plant's symptoms and their severities separated by commas (e.g., yellow_leaves:0.7, stunted_growth:0.8):")
    symptoms_input = input()
    user_symptoms = {symptom.split(':')[0].strip(): float(symptom.split(':')[1].strip()) for symptom in symptoms_input.split(',')}
    
    conclusions = diagnose(user_symptoms, rules)
    if conclusions:
        most_likely_diagnosis = conclusions[0]  # Get the top conclusion
        print(f"Based on the symptoms, the most likely diagnosis is {most_likely_diagnosis[0]} (confidence: {most_likely_diagnosis[1] * 100:.2f}%)")
    else:
        print("No diagnosis could be made based on the provided symptoms.")

if __name__ == "__main__":
    main()
