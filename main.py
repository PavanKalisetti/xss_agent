from automation.crawler import LiveCrawler  
from llm_integration.deepseek_api import DeepSeekWrapper  
from payloads.payload_generator import PayloadEngine
from automation.visible_browser import VisibleBrowser
from automation.visible_browser import VisibleBrowser
# from payloads.payload_generator import PayloadEngine
# from llm_integration.deepseek_api import DeepSeekWrapper
import json

def ensure_dict(input_vector):
    """
    Ensure that the input vector is in dictionary format.
    If it's a string, attempt to parse it as JSON.
    """
    try:
        parsed_response = json.loads(input_vector)
        print(parsed_response)  # Now it's a Python dictionary
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

def stage1_live_analysis(target_url):  
    # Launch visible browser and crawl  
    crawler = LiveCrawler(target_url)  
    inputs = crawler.crawl_visible_site()  
    print("\n\n")
    print(inputs)
    print("\n")
    print(type(str(inputs)))
    print("\n\n")
    
    # Prioritize inputs with LLM  
    deepseek = DeepSeekWrapper()
    prioritized = deepseek.analyze_inputs(str(inputs))  
    print("\ntype of data generated\n")
    print(type(prioritized))
    print("\n\n")
    print("\n[+] LLM-Prioritized Inputs:\n")
    print(prioritized)
    print("\n")  
    
    return prioritized

def stage2_payload_injection(target_url, input_vector):
    # Initialize components
    browser = VisibleBrowser(target_url)
    payload_engine = PayloadEngine()
    
    print(f"\n[*] Testing input: {input_vector['name']} ({input_vector['vector_type']})")
    
    # Generate payloads
    payloads = payload_engine.generate(input_vector)
    print(f"[+] Generated {len(payloads)} payloads")
    
    # Test each payload
    for payload in payloads:
        print(f"\n[→] Testing payload: {payload[:30]}...")
        browser.inject_payload(input_vector["name"], payload)
        
        # Check for reflection
        if payload in browser.page_source:
            print("[!] Reflection detected")
            # TODO: Add execution check (Stage 3)
        else:
            print("[×] No reflection")
    
    browser.keep_alive()


def stage3_payload_injection(target_url, input_vector):
    # Initialize components
    browser = VisibleBrowser(target_url)
    payload_engine = PayloadEngine()
    
    # print(f"\n[*] Testing input: {input_vector['name']} ({input_vector['vector_type']})")
    
    # Generate payloads
    payloads = payload_engine.generate(input_vector)
    print(f"[+] Generated {len(payloads)} payloads")

    print("\n\n")
    print(payloads)
    print("\n\n")
    
    # Test each payload
    for payload in payloads:
        print(f"\n[→] Testing payload: {payload}")
        browser.inject_payload(input_vector["name"], payload)
        
        # Check for reflection and execution
        browser.check_reflection(payload)
    
    browser.keep_alive()

if __name__ == "__main__":  
    target = "http://testphp.vulnweb.com/search.php?searchFor=test"
    
    # Example input vector from Stage 1
    test_vector = {
        "vector_type": "URL parameters",
        "name": "searchFor",
        "priority": 1
    }
    
    generated_vector = stage1_live_analysis(target)
    input_vector = ensure_dict(generated_vector)
    print("\nfinal one\n")
    print(input_vector)
    # stage3_payload_injection(target, input_vector)