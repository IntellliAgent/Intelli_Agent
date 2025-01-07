from intelliagent import DecisionMaker


def main():
    # Initialize the agent
    agent = DecisionMaker(
        api_key="your-api-key",
        model="gpt-4",
        domain="financial advisor",
        continuous_learning=True
    )

    # Example usage
    user_id = "user456"
    situation = "The stock market has shown a significant drop today."

    # Get decision
    decision = agent.make_decision(user_id=user_id, input_data=situation)
    print(f"Decision: {decision}")

    # Provide feedback
    feedback = "The investment suggestion was great, I made a 10% profit."
    agent.update_model(user_id=user_id, feedback=feedback)


if __name__ == "__main__":
    main()
