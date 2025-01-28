from automation.crawler import LiveCrawler  
from llm_integration.deepseek_api import DeepSeekWrapper  
from payloads.payload_generator import PayloadEngine
from automation.visible_browser import VisibleBrowser
from automation.visible_browser import VisibleBrowser
# from payloads.payload_generator import PayloadEngine
# from llm_integration.deepseek_api import DeepSeekWrapper
import json

def clean_json_string(json_str):
    """Clean JSON string by removing markdown code blocks and extra whitespace"""
    # Remove markdown code blocks if present
    if json_str.startswith('```') and json_str.endswith('```'):
        json_str = json_str[3:-3]  # Remove leading/trailing ```
    
    # Remove any language identifier if present (e.g., ```json)
    if '[' not in json_str.split('\n')[0]:
        json_str = '\n'.join(json_str.split('\n')[1:])
    
    # Strip whitespace and return
    return json_str.strip()

def ensure_dict(json_str):
    """Safely convert JSON string to dictionary"""
    if not json_str:
        return None
    
    try:
        import json
        cleaned_json = clean_json_string(json_str)
        return json.loads(cleaned_json)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        return None

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

    # Convert to Python dictionary
    input_vector = ensure_dict(prioritized)
    return input_vector
    
    

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


def stage3_payload_injection(target_url, input_vectors):
    """
    Test XSS payloads against one or more input vectors
    
    Args:
        target_url (str): The target URL to test
        input_vectors (dict|list): Single input vector object or list of input vector objects
    """
    # Initialize components
    browser = VisibleBrowser(target_url)
    payload_engine = PayloadEngine()
    
    # Convert single object to list for consistent handling
    if isinstance(input_vectors, dict):
        input_vectors = [input_vectors]
        
    # Sort vectors by priority if available
    input_vectors = sorted(input_vectors, key=lambda x: x.get('priority', 999))
    
    total_payloads = 0
    
    # Process each input vector
    for vector in input_vectors:
        print(f"\n[*] Testing input: {vector['name']} ({vector['vector_type']})")
        
        # Generate payloads for this vector
        payloads = payload_engine.generate(vector)
        print(f"[+] Generated {len(payloads)} payloads")
        total_payloads += len(payloads)
        
        print("\n[+] Payloads for this vector:")
        print(payloads)
        
        # Test each payload
        for payload in payloads:
            print(f"\n[→] Testing payload: {payload}")
            try:
                browser.inject_payload(vector["name"], payload)
                
                # Check for reflection and execution
                browser.check_reflection(payload)
                
            except Exception as e:
                print(f"[!] Error testing payload: {e}")
                continue
    
    print(f"\n[+] Completed testing {total_payloads} payloads across {len(input_vectors)} input vectors")
    browser.keep_alive()

if __name__ == "__main__":  
    # target = "http://testphp.vulnweb.com/search.php?searchFor=test"
    target = "https://brokencrystals.com/"
    
    
    
    # generated_vector = stage1_live_analysis(target)
    # input_vector = ensure_dict(generated_vector)
    # print("\nfinal one\n")
    # print(input_vector)
    generated_vector = stage1_live_analysis(target)

    stage3_payload_injection(target, generated_vector)

    # if generated_vector:
    #     print("\nParsed Input Vectors:")
    #     for vector in generated_vector:
    #         print(f"- {vector['vector_type']}: {vector['name']} (Priority: {vector['priority']})")
    # else:
    #     print("Failed to generate or parse input vectors")