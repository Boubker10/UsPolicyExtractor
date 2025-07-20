import os  
from src.main import build_pipeline
import json 
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        if "body" not in event or event["body"] is None:
            raise ValueError("Missing body in event")
        
        body = json.loads(event["body"])
        question = body.get("question")
        if not question:
            raise ValueError("Missing 'question' in request body")

        logger.info(f"Question received: {question}")

        pipeline = build_pipeline(question)

        result = pipeline.fit_transform(question)  

        logger.info(f"Pipeline result: {result}")

        response = {
            "statusCode": 200,
            "body": json.dumps({
                "answer": result
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
        return response

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
