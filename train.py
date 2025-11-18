"""
Training Script for Intent Classification Model
"""

import json
import os
from app.models.intent_classifier import IntentClassificationService
import random


def load_sample_data():
    """
    Load sample training data
    In production, load from a proper dataset
    """
    # Sample training data - replace with your actual dataset
    training_data = [
        # Greeting
        ("hello", "greeting"),
        ("hi there", "greeting"),
        ("good morning", "greeting"),
        ("hey", "greeting"),
        ("greetings", "greeting"),
        ("how are you", "greeting"),
        
        # Product Inquiry
        ("tell me about your products", "product_inquiry"),
        ("what products do you have", "product_inquiry"),
        ("show me your catalog", "product_inquiry"),
        ("I want to know about products", "product_inquiry"),
        ("product information", "product_inquiry"),
        ("what do you sell", "product_inquiry"),
        
        # Pricing
        ("how much does it cost", "pricing"),
        ("what's the price", "pricing"),
        ("pricing information", "pricing"),
        ("how much", "pricing"),
        ("what are your rates", "pricing"),
        ("cost", "pricing"),
        
        # Support
        ("I need help", "support"),
        ("can you help me", "support"),
        ("support please", "support"),
        ("I need assistance", "support"),
        ("help", "support"),
        
        # Complaint
        ("I'm not happy", "complaint"),
        ("this is terrible", "complaint"),
        ("I want to complain", "complaint"),
        ("this is unacceptable", "complaint"),
        ("I'm disappointed", "complaint"),
        
        # Order Status
        ("where is my order", "order_status"),
        ("order status", "order_status"),
        ("track my order", "order_status"),
        ("when will I receive my order", "order_status"),
        ("order tracking", "order_status"),
        
        # Account Management
        ("update my account", "account_management"),
        ("change my profile", "account_management"),
        ("account settings", "account_management"),
        ("manage account", "account_management"),
        
        # Technical Issue
        ("it's not working", "technical_issue"),
        ("there's a bug", "technical_issue"),
        ("technical problem", "technical_issue"),
        ("system error", "technical_issue"),
        ("something is broken", "technical_issue"),
        
        # Billing
        ("billing question", "billing"),
        ("invoice", "billing"),
        ("payment issue", "billing"),
        ("billing inquiry", "billing"),
        
        # Goodbye
        ("goodbye", "goodbye"),
        ("see you later", "goodbye"),
        ("bye", "goodbye"),
        ("thanks, that's all", "goodbye"),
        ("I'm done", "goodbye"),
    ]
    
    # Expand dataset with variations
    expanded_data = training_data.copy()
    
    # Add more variations
    variations = [
        ("I'd like to know", "product_inquiry"),
        ("can I get", "product_inquiry"),
        ("show me", "product_inquiry"),
        ("I need", "support"),
        ("please help", "support"),
        ("I have a problem", "support"),
        ("this doesn't work", "technical_issue"),
        ("I can't", "technical_issue"),
        ("error occurred", "technical_issue"),
    ]
    
    expanded_data.extend(variations)
    
    return expanded_data


def main():
    """Main training function"""
    print("Loading configuration...")
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    print("Initializing intent classification service...")
    intent_service = IntentClassificationService(config_path=config_path)
    
    print("Loading training data...")
    train_data = load_sample_data()
    
    # Split data (80% train, 20% validation would be ideal)
    random.shuffle(train_data)
    train_size = int(0.8 * len(train_data))
    train_set = train_data[:train_size]
    
    print(f"Training on {len(train_set)} samples...")
    print("This may take a while. Fine-tuning transformer model...")
    
    # Train the model
    intent_service.train(
        train_data=train_set,
        epochs=5,
        batch_size=8
    )
    
    # Save the model
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'intent_classifier.pth')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    print(f"Saving model to {model_path}...")
    intent_service.save_model(model_path)
    
    print("Training completed!")
    print(f"Model saved to: {model_path}")
    
    # Test the model
    print("\nTesting model...")
    test_samples = [
        "hello",
        "what products do you have",
        "how much does it cost",
        "I need help",
        "goodbye"
    ]
    
    for text in test_samples:
        result = intent_service.predict(text)
        print(f"Text: '{text}'")
        print(f"  Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        print()


if __name__ == '__main__':
    main()

