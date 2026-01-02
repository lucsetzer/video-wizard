# layout.py
def layout(title: str, content: str, current_tool: str = "Dashboard") -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} | Prompts Alchemy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #8b5cf6;
            --secondary: #f59e0b;
            --dark: #1f2937;
            --light: #f9fafb;
        }}
        
        /* Your CSS from earlier */
        .suite-nav {{ background: white; border-bottom: 2px solid var(--light); padding: 1rem 0; }}
        .brand {{ font-size: 1.5rem; font-weight: bold; background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        /* ... rest of your CSS ... */
    </style>
</head>
<body style="background: var(--light); min-height: 100vh;">
    <!-- Navigation -->
    <nav class="suite-nav">
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <a href="/" class="brand" style="text-decoration: none;">
                        <i class="fas fa-flask"></i> Prompts Alchemy
                    </a>
                </div>
                <div>
                    <a href="/dashboard" style="margin: 0 0.5rem; color: var(--dark); text-decoration: none;">
                        <i class="fas fa-th-large"></i> Dashboard
                    </a>
                    <a href="/tools/prompt" style="margin: 0 0.5rem; color: var(--dark); text-decoration: none;">
                        <i class="fas fa-hat-wizard"></i> Prompt Wizard
                    </a>
                    <!-- Add other tools -->
                </div>
            </div>
        </div>
    </nav>

    <main class="container" style="padding: 2rem 0;">
        {content}
    </main>
</body>
</html>'''
