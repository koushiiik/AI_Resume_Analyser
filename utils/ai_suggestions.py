"""
ai_suggestions.py
-----------------
Uses the Groq API to generate concise resume improvement suggestions.
"""

import os
import logging
from groq import Groq

def get_ai_suggestions(resume_text: str, missing_skills: list, role: str) -> list:
    """
    Generate ATS-focused improvement suggestions using the Groq API.
    
    Args:
        resume_text (str): Extracted text from the resume
        missing_skills (list): List of skills missing from the resume
        role (str): The target role
    
    Returns:
        list: A list of actionable suggestion bullet points
    """
    
    # Handle the empty missing_skills edge case
    if not missing_skills:
        return {
            "overall": "Great job! Your resume aligns highly with the target role.",
            "bullets": [
                "Ensure your impact is backed by measurable metrics (e.g., increased efficiency by X%).",
                "Keep exploring advanced topics in your field to stay competitive."
            ]
        }
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {
            "overall": "Unable to generate AI suggestions.",
            "bullets": ["The GROQ_API_KEY is not set."]
        }

    try:
        client = Groq(api_key=api_key)
        
        truncated_text = resume_text[:10000]
        skills_str = ", ".join(missing_skills)
        
        system_prompt = (
            "You are an expert resume reviewer and ATS optimization specialist. "
            "Provide concise, high-impact improvement suggestions. Respond ONLY in valid JSON format."
        )
        
        user_prompt = f"""Target Role: {role}
Missing Skills: {skills_str}

Resume Excerpt:
{truncated_text}

Provide an overall assessment and exactly 3 short, highly practical bullet points.
Format your output exactly matching this JSON block:
{{
  "overall": "One short 2-3 sentence paragraph giving an overall honest assessment and suggestion.",
  "bullets": [
    "Brief point 1 focusing on how to add a critical missing skill",
    "Brief point 2 focusing on structure or impact metrics",
    "Brief point 3 focusing on ATS optimization"
  ]
}}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6,
            max_tokens=400,
        )
        
        import json
        raw_text = response.choices[0].message.content.strip()
        data = json.loads(raw_text)
        
        return {
            "overall": data.get("overall", ""),
            "bullets": data.get("bullets", [])
        }
        
    except Exception as e:
        logging.error(f"Groq API Error: {e}")
        return {
            "overall": "We encountered an error while communicating with the AI server.",
            "bullets": [f"Debug: {str(e)}", "Please try again later."]
        }
