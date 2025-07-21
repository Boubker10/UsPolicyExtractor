import os
import json
import logging
import traceback
from src.main import build_pipeline

# Configuration du logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Handler Lambda pour le traitement des questions juridiques avec OCR et IA
    """
    try:
        required_env_vars = [
            'DEEPSEEK_API_KEY',
            'SERPAPI_KEY'  
        ]
        
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Validation de l'événement
        if "body" not in event or event["body"] is None:
            raise ValueError("Missing body in event")
        
        # Parse du body JSON
        try:
            if isinstance(event["body"], str):
                body = json.loads(event["body"])
            else:
                body = event["body"]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in request body: {str(e)}")
        
        # Extraction de la question
        question = body.get("question")
        if not question or not isinstance(question, str) or not question.strip():
            raise ValueError("Missing or empty 'question' in request body")
        
        question = question.strip()
        logger.info(f"Question received: {question}")
        
        logger.info("Building pipeline...")
        pipeline = build_pipeline(question)
        
        logger.info("Executing pipeline...")
        result = pipeline.fit_transform(question)  
        
        logger.info(f"Pipeline completed successfully")
        logger.info(f"Result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "question": question,
                "result": result
            }, ensure_ascii=False),
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }
        
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_error_response(400, str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return create_error_response(500, "Internal server error")

def create_error_response(status_code: int, message: str):

    return {
        "statusCode": status_code,
        "body": json.dumps({
            "status": "error",
            "error": message
        }),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    }

def handle_options():

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400"
        },
        "body": ""
    }