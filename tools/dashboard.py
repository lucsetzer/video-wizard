# tools/dashboard.py
from layout import layout

def get_dashboard():
    content = '''
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="brand">Prompts Alchemy</h1>
        <p>Choose your tool:</p>
        <div class="grid">
            <a href="/tools/prompt" class="card">
                <h3><i class="fas fa-hat-wizard"></i> Prompt Wizard</h3>
                <p>Create AI prompts</p>
            </a>
            <!-- Other tools -->
        </div>
    </div>
    '''
    return layout("Dashboard", content)
