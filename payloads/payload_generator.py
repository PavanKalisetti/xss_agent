from llm_integration.deepseek_api import DeepSeekWrapper

class PayloadEngine:
    def __init__(self):
        self.llm = DeepSeekWrapper()
        self.base_payloads = [  # Fallback list if LLM fails
            "<script>alert(1)</script>",
            "\"><img src=x onerror=alert(1)>",
            "javascript:alert(1)"
        ]

    def generate(self, input_vector):
        """Generate payloads for a specific input vector"""
        try:
            # Get LLM-generated payloads
            llm_payloads = self.llm.generate_payloads(input_vector)
            return self._parse_llm_response(llm_payloads)
        except Exception as e:
            print(f"LLM Error: {e}. Using base payloads")
            return self.base_payloads

    
    def _parse_llm_response(self, raw_text):
        """Extract payloads from DeepSeek's strict response format"""
        if not raw_text:
            return self.base_payloads

        payloads = []
        lines = raw_text.split('\n')
        for line in lines:
            if line.strip().startswith("```"):
                continue  # Skip code block markers
            if line.strip() and line[0].isdigit():  # Check for numbered lines
                payload = line.split(".", 1)[-1].strip()  # Extract payload after the number
                if payload:
                    payloads.append(payload)

        return payloads[:5] or self.base_payloads  # Return max 5 payloads