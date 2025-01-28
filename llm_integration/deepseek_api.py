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
        print("in the analyze inputes")
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """
                                You are a cybersecurity expert specializing in web application vulnerabilities.Generate response in the following example in this strict format:
                                
                                ```[
                                            {
                                            "vector_type": "URL parameters",
                                            "name": "searchFor",
                                            "priority": 1,
                                            
                                            },
                                            {
                                            "vector_type": "Form fields without CSRF tokens",
                                            "name": "searchFor",
                                            "priority": 2,
                                            
                                            },
                                            {
                                            "vector_type": "Headers like User-Agent or Referer",
                                            "name": "User-Agent/Referer",
                                            "priority": 3,
                                            }
                                        ]
                                        ```
                                
                            
                            """

                    },
                    {
                        "role": "user", 
                        "content": f""" As a security researcher, analyze this web application context:
                            {context}

                            List all user-controllable input vectors vulnerable to Reflected XSS, 
                            ordered by priority (most likely to least likely). Focus on:
                            - URL parameters
                            - Form fields without CSRF tokens
                            - Headers like User-Agent or Referer

                                """
                    }
                ]
            )
            # Accessing the content of the first choice
            content = response.choices[0].message.content
            
            print("\n\nFiltered Response Content:\n", content)
            return content  # Return the filtered content
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