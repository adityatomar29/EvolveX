def generate_ml_recommendations(data):
    recommendations = []
    reduction = 0

    training_time = data.get("training_time", 0)
    energy = data.get("energy", 0)
    hardware = data.get("hardware", "").lower()
    model_name = data.get("model_name", "").lower()

    # RULE BASED AI 

    # General 
    recommendations.append("Use cloud regions powered by renewable energy.")
    reduction += energy * 0.05

    if training_time < 5 and energy < 10:
        recommendations.append("Good going, your model is energy efficient. Look for other potential improvements.")   
    # Training Time
    elif training_time > 5:
        recommendations.append("Reduce training time using early stopping.")
        reduction += energy * 0.15
    # Energy Consumption
    elif energy > 10:
        recommendations.append("Use smaller batch size or efficient architectures.")
        reduction += energy * 0.25

    # Hardware
    if "gpu" in hardware:
        recommendations.append("Use energy-efficient GPUs or switch to TPUs.")
        reduction += energy * 0.10
    elif "cpu" in hardware:
        recommendations.append("Use optimized GPU training instead of CPU.")
        reduction += energy * 0.20
    elif "tpu" in hardware:
        recommendations.append("Use optimized TPU training.")
        reduction += energy * 0.30

    # Model Type
    if "transformer" in model_name:
        recommendations.append("Use distilled models like DistilBERT to reduce emissions.")
        reduction += energy * 0.30

    if "cnn" in model_name:
        recommendations.append("Use lightweight CNNs like MobileNet.")
        reduction += energy * 0.15
    if "bert" in model_name:
        recommendations.append("Optimize the BERT model to save energy.")
        reduction += energy * 0.25

    
    return recommendations, round(reduction, 2)