from openai import OpenAI
import requests
import os
from config import DEEPSEEK_API_KEY

class DeepSeekWrapper:
    def __init__(self):

        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
    
    
    def analyze_inputs(self, context):
        """Ask LLM to prioritize input points"""
        print("in the analyze inputs")
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a cybersecurity expert specializing in web application vulnerabilities, particularly XSS.
                        
                        You MUST respond in this exact JSON format, without any additional text or explanation:
                        [
                            {
                                "vector_type": "URL parameters",
                                "name": "parameter_name",
                                "priority": 1
                            }
                        ]
                        
                        Rules for response:
                        1. Only use these vector_type values:
                        - "URL parameters"
                        - "Form fields without CSRF tokens"
                        - "Headers like User-Agent or Referer"
                        2. Priority should be a number (1 is highest priority)
                        3. Name should be the actual parameter/field name found
                        4. Do not add any markdown, explanation, or additional text
                        5. Ensure valid JSON format with no trailing commas
                        """
                    },
                    {
                        "role": "user", 
                        "content": f"""Analyze this web application context and return ONLY the JSON array of input vectors:
                            {context}

                            Consider:
                            - URL parameters
                            - Form fields without CSRF tokens
                            - Headers like User-Agent or Referer
                            
                            Return ONLY the JSON array.
                        """
                    }
                ]
            )
            content = response.choices[0].message.content
            return content
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            return None

        
        

    def generate_payloads(self, input_vector):
        """Generate XSS payloads using DeepSeek's API"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a cybersecurity expert specializing in web application vulnerabilities. 
                        Generate Reflected XSS payloads in the following strict format:
                        ```
                        1. Payload 1
                        2. Payload 2
                        3. Payload 3
                        4. Payload 4
                        5. Payload 5
                        ```
                        - Do not include explanations, headers, or notes.
                        - Ensure payloads are context-aware and non-destructive.
                        - Use only valid HTML/JavaScript syntax."""
                    },
                    {
                        "role": "user", 
                        "content": f"""Generate 5 Reflected XSS payloads for this input vector:
                        {input_vector}"""
                    }
                ],
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            return None