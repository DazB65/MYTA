"""
Test script for Strategic Content Classifier
Run this to verify the classifier is working correctly
"""

from strategic_content_classifier import get_strategic_content_classifier, ContentType

def test_strategic_classifier():
    """Test the strategic content classifier with various examples"""
    
    classifier = get_strategic_content_classifier()
    
    # Test cases for strategic planning
    strategic_examples = [
        "What should my quarterly strategy be for Q2?",
        "I need help with long-term planning for my channel",
        "Can you help me create a strategic roadmap for next year?",
        "Let's plan our team strategy for the upcoming quarter",
        "I want to develop a comprehensive content strategy",
        "What are the strategic priorities for my channel growth?",
        "Help me with annual goal setting and planning",
        "I need a strategic review of my channel direction"
    ]
    
    # Test cases for everyday insights
    tactical_examples = [
        "How can I optimize this video's thumbnail?",
        "What should I do to improve my latest video performance?",
        "Can you analyze my current analytics?",
        "How do I fix my retention rate today?",
        "What's the best posting time for this week?",
        "Help me improve my video titles right now",
        "I need quick tips to boost engagement",
        "How can I optimize my recent upload?"
    ]
    
    # Test cases that might be ambiguous
    ambiguous_examples = [
        "How do I grow my channel?",
        "What content should I create?",
        "Help me with my strategy",
        "I need advice on my channel",
        "What are some good ideas for videos?"
    ]
    
    print("=== STRATEGIC CONTENT CLASSIFIER TEST ===\n")
    
    print("🎯 STRATEGIC PLANNING EXAMPLES:")
    print("-" * 50)
    for example in strategic_examples:
        classification, confidence, details = classifier.classify_content(example)
        should_redirect, analysis = classifier.should_redirect_to_strategic_planning(example)
        
        print(f"Message: '{example}'")
        print(f"Classification: {classification.value}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Should Redirect: {should_redirect}")
        print(f"Strategic Score: {details['strategic_score']:.2f}")
        print(f"Tactical Score: {details['tactical_score']:.2f}")
        print()
    
    print("\n💡 EVERYDAY INSIGHTS EXAMPLES:")
    print("-" * 50)
    for example in tactical_examples:
        classification, confidence, details = classifier.classify_content(example)
        should_redirect, analysis = classifier.should_redirect_to_strategic_planning(example)
        
        print(f"Message: '{example}'")
        print(f"Classification: {classification.value}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Should Redirect: {should_redirect}")
        print(f"Strategic Score: {details['strategic_score']:.2f}")
        print(f"Tactical Score: {details['tactical_score']:.2f}")
        print()
    
    print("\n❓ AMBIGUOUS EXAMPLES:")
    print("-" * 50)
    for example in ambiguous_examples:
        classification, confidence, details = classifier.classify_content(example)
        should_redirect, analysis = classifier.should_redirect_to_strategic_planning(example)
        
        print(f"Message: '{example}'")
        print(f"Classification: {classification.value}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Should Redirect: {should_redirect}")
        print(f"Strategic Score: {details['strategic_score']:.2f}")
        print(f"Tactical Score: {details['tactical_score']:.2f}")
        print()
    
    # Summary statistics
    strategic_correct = 0
    tactical_correct = 0
    
    for example in strategic_examples:
        should_redirect, _ = classifier.should_redirect_to_strategic_planning(example)
        if should_redirect:
            strategic_correct += 1
    
    for example in tactical_examples:
        should_redirect, _ = classifier.should_redirect_to_strategic_planning(example)
        if not should_redirect:
            tactical_correct += 1
    
    print("\n📊 CLASSIFICATION ACCURACY:")
    print("-" * 50)
    print(f"Strategic Examples Correctly Classified: {strategic_correct}/{len(strategic_examples)} ({strategic_correct/len(strategic_examples)*100:.1f}%)")
    print(f"Tactical Examples Correctly Classified: {tactical_correct}/{len(tactical_examples)} ({tactical_correct/len(tactical_examples)*100:.1f}%)")
    print(f"Overall Accuracy: {(strategic_correct + tactical_correct)/(len(strategic_examples) + len(tactical_examples))*100:.1f}%")

if __name__ == "__main__":
    test_strategic_classifier()
