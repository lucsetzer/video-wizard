# tools/prompt_wizard.py
from layout import layout
from utils.ai_client import enhance_prompt

def step1():
    content = '''
    <div class="card">
        <h1>Step 1: Goal</h1>
        <div class="grid">
            <a href="/tools/prompt/step2?goal=explain" class="card">Explain</a>
            <a href="/tools/prompt/step2?goal=create" class="card">Create</a>
        </div>
    </div>
    '''
    return layout("Prompt Wizard - Step 1", content, "Prompt Wizard")

def step2(goal: str):
    content = f'''
    <div class="card">
        <h1>Step 2: Audience for {goal}</h1>
        <!-- Content -->
    </div>
    '''
    return layout("Prompt Wizard - Step 2", content, "Prompt Wizard")

def process(goal: str, audience: str, prompt: str):
    # Call AI
    enhanced = enhance_prompt(goal, audience, prompt)
    
    content = f'''
    <div class="card">
        <h2>Enhanced Prompt:</h2>
        <pre>{enhanced}</pre>
    </div>
    '''
    return layout("Result", content, "Prompt Wizard")
