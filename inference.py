import os
from openai import OpenAI
from client import PiiRedactorEnv
from models import PiiRedactorAction

def main():
    api_base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
    api_key = os.getenv("HF_TOKEN") or "sk-dummy"

    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key
    )

    print(f"[START] task=pii_redaction env=pii_redactor model={model_name}", flush=True)
    
    steps_taken = 0
    rewards = []
    success = False
    
    try:
        # FIX: Using 127.0.0.1 instead of localhost for Windows compatibility
        env_url = "http://127.0.0.1:8000"
        
        with PiiRedactorEnv(base_url=env_url).sync() as env:
            # 1. Connect to Environment
            result = env.reset()
            obs = result.observation
            
            prompt = f"Task: {obs.task_description}\nText to redact: {obs.raw_text}\nRespond ONLY with the redacted text. Replace sensitive information with [REDACTED]."
            
            # 2. Connect to Hugging Face
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional PII redactor. Do not add conversational text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            
            redacted_text = response.choices[0].message.content.strip()
            
            # 3. Step Environment
            step_result = env.step(PiiRedactorAction(redacted_text=redacted_text))
            
            reward = float(step_result.reward or 0.0)
            done = step_result.done
            rewards.append(reward)
            steps_taken += 1
            
            done_str = str(done).lower()
            safe_action = redacted_text.replace('\n', ' ')
            print(f"[STEP] step={steps_taken} action='{safe_action}' reward={reward:.2f} done={done_str} error=null", flush=True)
            
            if reward > 0.5:
                success = True

    except Exception as e:
        # Added the specific Exception type so we know exactly what is breaking
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[STEP] step={steps_taken+1} action=null reward=0.00 done=true error='{error_msg}'", flush=True)
    
    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards) if rewards else "0.00"
        print(f"[END] success={str(success).lower()} steps={max(steps_taken, 1)} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    main()