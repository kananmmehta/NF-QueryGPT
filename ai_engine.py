# ai_engine.py
import json
import os
import streamlit as st
from google import genai
from google.genai import types

@st.cache_data
def load_cached_schema():
    """Reads the schema definition file once and caches it to keep performance high."""
    with open("schema.sql", "r") as f:
        return f.read()

db_schema = load_cached_schema()

SYSTEM_INSTRUCTION = f"""
You are NF QueryGPT, an expert business intelligence assistant for NikahForever.
Your role is to translate user natural language questions (written in English or Hinglish) into clean, optimized SQLite queries based strictly on the provided database schema.

Database Schema Context:
{db_schema}

Strict Execution Protocol:
1. ONLY generate standard SELECT statements. Never write data.
2. If a query is ambiguous, lacks relational context, or mentions properties not found in the schema tables, set status to 'ambiguous' and ask a friendly clarifying question. Do not guess or hallucinate.
3. Fully understand Hinglish mappings (e.g., 'ladka'/'munda'/'bhai' -> male, 'ladki'/'kudi'/'behen' -> female, 'shadi'/'biyah' -> marriage/matches, 'sheher' -> city, 'umra' -> age).
4. Provide a clear, non-technical explanation of what data your query targets.
5. Pay close attention to conversational history. If the user asks a follow-up question (e.g., "unme se premium kitne hain?"), refer back to the context of their previous queries to isolate the correct data filters.

You must return your response in a valid JSON format with these exact keys:
{{
    "status": "success" or "ambiguous",
    "sql": "The raw SQLite SELECT query or an empty string if status is ambiguous",
    "clarification": "Your targeted clarification question if status is ambiguous, else empty string",
    "explanation": "A clean 1-sentence description detailing what data this query pulls for a business user."
}}
"""

def generate_sql_response(user_prompt: str, chat_history: list = [], historical_context: str = ""):
    """Calls Gemini compiling conversational context, active prompt tokens, and schema targets."""
    client = genai.Client()
    
    # 1. Inject Conversational Memory Context
    memory_context = ""
    if chat_history:
        memory_context += "### RECENT CONVERSATIONAL HISTORY\n"
        # Extract the last 3 exchanges to keep context highly relevant without inflating token usage
        for turn in chat_history[-3:]:
            memory_context += f"User: {turn['query']}\nAI Generated SQL: {turn['sql']}\n"
        memory_context += "### END OF CONVERSATIONAL HISTORY\n\n"
    
    # 2. Inject Error Self-Healing Context if applicable
    if historical_context:
        memory_context += f"### CRITICAL REPAIR REQUIRED\n{historical_context}\n\n"
        
    full_prompt = f"{memory_context}Current User Request: {user_prompt}"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            temperature=0.1  # Low temperature ensures highly deterministic SQL generation
        ),
    )
    return json.loads(response.text)

def generate_self_healed_query(original_prompt: str, broken_sql: str, error_msg: str, chat_history: list = []):
    """
    Self-Correction Loop: If database execution fails, this agent evaluates 
    the error message against the schema to fix syntax or mapping mistakes automatically.
    """
    context = f"The query `{broken_sql}` failed execution with database error message: {error_msg}."
    try:
        healed_response = generate_sql_response(original_prompt, chat_history=chat_history, historical_context=context)
        return healed_response
    except Exception:
        return None

def generate_data_insights(df_sample_markdown: str):
    """
    Secondary Analyst Agent: Processes the query dataset outputs 
    to extract narrative patterns and plain-English summaries.
    """
    client = genai.Client()
    insight_prompt = f"""
    Analyze this sample data output from the NikahForever platform database. 
    Provide a brief, professional, 2-sentence executive summary identifying key business insights or anomalies:
    
    {df_sample_markdown}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=insight_prompt
        )
        return response.text
    except Exception as e:
        return f"Unable to compile data narrative insights at this moment: {str(e)}"