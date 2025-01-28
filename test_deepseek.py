from llm_integration.deepseek_api import DeepSeekWrapper
from payloads.payload_generator import PayloadEngine

def test_payload_generation():
    test_vector = {
        "name": "search",
        "type": "URL parameter",
        "context": "Reflected in <div> with basic HTML encoding"
    }
    
    ds = DeepSeekWrapper()
    response = ds.generate_payloads(test_vector)
    print("Raw DeepSeek Response:\n", response)
    
    engine = PayloadEngine()
    payloads = engine._parse_llm_response(response)
    print("\nExtracted Payloads:\n", payloads)

if __name__ == "__main__":
    test_payload_generation()