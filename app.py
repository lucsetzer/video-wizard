# video_wizard/app.py - VIDEO WIZARD
from fastapi import FastAPI, Query, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import os

app = FastAPI()
# You'll need a different AI key for video analysis (GPT-4 Vision maybe)
DEEPSEEK_KEY = "sk-849662e0871841a5a4496e006311beb9"  # Might need different model

def layout(title: str, content: str) -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} | Video Alchemy</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: #10b981;  /* GREEN theme for video */
            --primary-hover: #0da271;
        }}
        
        [role="button"], button, .btn-primary {{
            background: var(--primary);
            border-color: var(--primary);
        }}
        
        a {{ color: var(--primary); }}
        a:hover {{ color: var(--primary-hover); }}
        
        /* Cards */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }}
        
        .step-card {{
            padding: 1.5rem;
            border: 2px solid #e5e7eb;
            border-radius: 0.75rem;
            text-align: center;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
        }}
        
        .step-card:hover {{
            border-color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .step-card i {{
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }}
        
        /* Loading bar */
        .loading-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            margin: 2rem 0;
            overflow: hidden;
        }}
        
        .loading-progress {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), #34d399);
            border-radius: 4px;
            animation: loading 2s infinite;
            width: 60%;
        }}
        
        @keyframes loading {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(350%); }}
        }}
        
        /* Step indicator */
        .steps {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 2rem 0;
        }}
        
        .step {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        .step.active {{
            background: var(--primary);
            color: white;
        }}
        
        /* Result box */
        .result-box {{
            background: #f8fafc;
            border: 2px solid #e5e7eb;
            border-left: 4px solid var(--primary);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            white-space: pre-wrap;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 1rem;
            line-height: 1.6;
            text-align: left;
            color: #1f2937;
            overflow-x: auto;
        }}
        
        .url-input {{
            width: 100%;
            padding: 1rem;
            border: 2px solid #e5e7eb;
            border-radius: 0.5rem;
            font-size: 1.1rem;
        }}
        
        .url-input:focus {{
            border-color: var(--primary);
            outline: none;
        }}
    </style>
</head>
<body style="background: white;">
<nav style="padding: 1rem 0; border-bottom: 1px solid #e5e7eb;">
    <div class="container">
        <a href="/" style="text-decoration: none; font-size: 1.25rem; font-weight: bold; color: var(--primary);">
            <i class="fas fa-video"></i> Video Alchemy
        </a>
        <span style="float: right;">
            <a href="/" style="margin-right: 1rem;">Home</a>
            <a href="/wizard">Video Wizard</a>
        </span>
    </div>
</nav>

<main class="container" style="padding: 2rem 0; min-height: 80vh;">
    {content}
</main>

<footer style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb;">
    <p>Video Wizard • Optimize videos for any platform</p>
</footer>
</body>
</html>'''

# ========== DASHBOARD ==========
@app.get("/")
async def home():
    content = '''
    <div style="text-align: center; padding: 4rem 0;">
        <h1 style="color: var(--primary);">
            <i class="fas fa-video"></i><br>
            Video Alchemy
        </h1>
        <p style="font-size: 1.25rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            AI-powered video optimization. Get platform-specific fixes in 6 steps.
        </p>
        
        <div style="margin: 3rem 0;">
            <a href="/wizard" role="button" style="padding: 1rem 2.5rem; font-size: 1.25rem;">
                <i class="fas fa-magic"></i> Start Video Wizard
            </a>
        </div>
        
        <div class="card-grid">
            <div class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube</h3>
                <p>Increase retention & views</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok</h3>
                <p>Master the algorithm</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram</h3>
                <p>Reels & IGTV optimization</p>
            </div>
            
            <div class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn</h3>
                <p>Professional video tips</p>
            </div>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Home", content))

# ========== STEP 1: PLATFORM ==========
@app.get("/wizard")
async def step1():
    content = '''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step active">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 1: Choose Platform</h1>
        <p style="text-align: center; color: #6b7280;">
            Where is your video published or will be published?
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step2?platform=youtube" class="step-card">
                <i class="fab fa-youtube"></i>
                <h3>YouTube</h3>
                <p>Long-form, monetization</p>
            </a>
            
            <a href="/wizard/step2?platform=tiktok" class="step-card">
                <i class="fab fa-tiktok"></i>
                <h3>TikTok</h3>
                <p>Short-form, viral potential</p>
            </a>
            
            <a href="/wizard/step2?platform=instagram" class="step-card">
                <i class="fab fa-instagram"></i>
                <h3>Instagram</h3>
                <p>Reels, Stories, IGTV</p>
            </a>
            
            <a href="/wizard/step2?platform=linkedin" class="step-card">
                <i class="fab fa-linkedin"></i>
                <h3>LinkedIn</h3>
                <p>Professional, B2B</p>
            </a>
            
            <a href="/wizard/step2?platform=facebook" class="step-card">
                <i class="fab fa-facebook"></i>
                <h3>Facebook</h3>
                <p>Groups, Pages, viral</p>
            </a>
            
            <a href="/wizard/step2?platform=twitter" class="step-card">
                <i class="fab fa-twitter"></i>
                <h3>Twitter/X</h3>
                <p>Short clips, threads</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" role="button" class="secondary">Cancel</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 1: Platform", content))

# ========== STEP 2: VIDEO TYPE ==========
@app.get("/wizard/step2")
async def step2(platform: str = Query("youtube")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step active">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 2: Video Type</h1>
        <p style="text-align: center; color: #6b7280;">
            What kind of video is this?
        </p>
        
        <p style="text-align: center;"><strong>Platform:</strong> {platform.title()}</p>
        
        <div class="card-grid">
            <a href="/wizard/step3?platform={platform}&type=tutorial" class="step-card">
                <i class="fas fa-chalkboard-teacher"></i>
                <h3>Tutorial</h3>
                <p>How-to, educational</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=vlog" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Vlog</h3>
                <p>Personal, day-in-life</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=review" class="step-card">
                <i class="fas fa-star"></i>
                <h3>Review</h3>
                <p>Product, service, media</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=entertainment" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Entertainment</h3>
                <p>Comedy, skits, fun</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=educational" class="step-card">
                <i class="fas fa-graduation-cap"></i>
                <h3>Educational</h3>
                <p>Deep dive, explainer</p>
            </a>
            
            <a href="/wizard/step3?platform={platform}&type=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Marketing, pitch, update</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 2: Video Type", content))

# ========== STEP 3: GOAL ==========
@app.get("/wizard/step3")
async def step3(platform: str = Query("youtube"), type: str = Query("tutorial")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step active">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 3: Choose Goal</h1>
        <p style="text-align: center; color: #6b7280;">
            What do you want to improve?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step4?platform={platform}&type={type}&goal=retention" class="step-card">
                <i class="fas fa-clock"></i>
                <h3>Retention</h3>
                <p>Keep viewers watching longer</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=views" class="step-card">
                <i class="fas fa-eye"></i>
                <h3>More Views</h3>
                <p>Increase view count</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=algorithm" class="step-card">
                <i class="fas fa-robot"></i>
                <h3>Algorithm</h3>
                <p>Better platform ranking</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=engagement" class="step-card">
                <i class="fas fa-comments"></i>
                <h3>Engagement</h3>
                <p>More likes, comments, shares</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=seo" class="step-card">
                <i class="fas fa-search"></i>
                <h3>SEO</h3>
                <p>Better search visibility</p>
            </a>
            
            <a href="/wizard/step4?platform={platform}&type={type}&goal=conversion" class="step-card">
                <i class="fas fa-shopping-cart"></i>
                <h3>Conversion</h3>
                <p>More clicks, sales, signups</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step2?platform={platform}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 3: Goal", content))

# ========== STEP 4: AUDIENCE ==========
@app.get("/wizard/step4")
async def step4(platform: str = Query("youtube"), type: str = Query("tutorial"), goal: str = Query("retention")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step active">4</div>
            <div class="step">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 4: Choose Audience</h1>
        <p style="text-align: center; color: #6b7280;">
            Who is your target viewer?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()} • 
            <strong>Goal:</strong> {goal.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=beginners" class="step-card">
                <i class="fas fa-baby"></i>
                <h3>Beginners</h3>
                <p>New to the topic</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=intermediate" class="step-card">
                <i class="fas fa-user"></i>
                <h3>Intermediate</h3>
                <p>Some experience</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=experts" class="step-card">
                <i class="fas fa-user-graduate"></i>
                <h3>Experts</h3>
                <p>Advanced knowledge</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=general" class="step-card">
                <i class="fas fa-users"></i>
                <h3>General</h3>
                <p>Broad audience</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=business" class="step-card">
                <i class="fas fa-briefcase"></i>
                <h3>Business</h3>
                <p>Professionals, B2B</p>
            </a>
            
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience=creators" class="step-card">
                <i class="fas fa-paint-brush"></i>
                <h3>Creators</h3>
                <p>Other content creators</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step3?platform={platform}&type={type}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 4: Audience", content))

# ========== STEP 5: TONE ==========
@app.get("/wizard/step5")
async def step5(platform: str = Query("youtube"), type: str = Query("tutorial"), goal: str = Query("retention"), audience: str = Query("beginners")):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step active">5</div>
            <div class="step">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 5: Choose Tone</h1>
        <p style="text-align: center; color: #6b7280;">
            What's the video's personality?
        </p>
        
        <p style="text-align: center;">
            <strong>Platform:</strong> {platform.title()} • 
            <strong>Type:</strong> {type.title()} • 
            <strong>Goal:</strong> {goal.title()} • 
            <strong>Audience:</strong> {audience.title()}
        </p>
        
        <div class="card-grid">
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=friendly" class="step-card">
                <i class="fas fa-smile"></i>
                <h3>Friendly</h3>
                <p>Warm, approachable</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=professional" class="step-card">
                <i class="fas fa-suitcase"></i>
                <h3>Professional</h3>
                <p>Formal, business-like</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=energetic" class="step-card">
                <i class="fas fa-bolt"></i>
                <h3>Energetic</h3>
                <p>Fast-paced, exciting</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=calm" class="step-card">
                <i class="fas fa-spa"></i>
                <h3>Calm</h3>
                <p>Relaxed, soothing</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=humorous" class="step-card">
                <i class="fas fa-laugh"></i>
                <h3>Humorous</h3>
                <p>Funny, entertaining</p>
            </a>
            
            <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone=authoritative" class="step-card">
                <i class="fas fa-crown"></i>
                <h3>Authoritative</h3>
                <p>Expert, confident</p>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step4?platform={platform}&type={type}&goal={goal}" role="button" class="secondary">Back</a>
        </div>
    </div>
    '''
    return HTMLResponse(layout("Step 5: Tone", content))

# ========== STEP 6: VIDEO INPUT ==========
@app.get("/wizard/step6")
async def step6(
    platform: str = Query("youtube"),
    type: str = Query("tutorial"),
    goal: str = Query("retention"),
    audience: str = Query("beginners"),
    tone: str = Query("friendly")
):
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="steps">
            <div class="step">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
            <div class="step">5</div>
            <div class="step active">6</div>
        </div>
        
        <h1 style="text-align: center; color: var(--primary);">Step 6: Video Details</h1>
        <p style="text-align: center; color: #6b7280;">
            Tell us about your video
        </p>
        
        <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin: 2rem 0;">
            <h3>Your Selections:</h3>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 1rem 0;">
                <div><strong>Platform:</strong><br>{platform.title()}</div>
                <div><strong>Type:</strong><br>{type.title()}</div>
                <div><strong>Goal:</strong><br>{goal.title()}</div>
                <div><strong>Audience:</strong><br>{audience.title()}</div>
                <div><strong>Tone:</strong><br>{tone.title()}</div>
            </div>
        </div>
        
        <div style="background: #f0f9ff; border: 2px solid #10b981; border-radius: 0.75rem; padding: 1rem; margin: 1rem 0;">
    <p style="margin: 0; color: #065f46; display: flex; align-items: center; gap: 0.5rem;">
        <i class="fas fa-lightbulb" style="color: #10b981;"></i>
        <strong>Pro Tip:</strong> Even brief descriptions work! AI analyzes 
        <strong>video structure & platform optimization</strong>, not specific content.
    </p>
</div>

        <form action="/process" method="POST">
            <input type="hidden" name="platform" value="{platform}">
            <input type="hidden" name="type" value="{type}">
            <input type="hidden" name="goal" value="{goal}">
            <input type="hidden" name="audience" value="{audience}">
            <input type="hidden" name="tone" value="{tone}">
            
            <div style="margin: 2rem 0;">
                <label for="video_url">
                    <strong>YouTube Video URL:</strong>
                    <p style="color: #6b7280; margin: 0.5rem 0;">Paste a public YouTube link (we'll analyze the title, description, etc.)</p>
                </label>
                <input type="url" id="video_url" name="video_url" 
                       placeholder="https://www.youtube.com/watch?v=..." 
                       class="url-input">
            </div>
            
            <div style="margin: 2rem 0;">
    <label for="video_description">
        <strong>Video Description:</strong>
        <p style="color: #6b7280; margin: 0.5rem 0;">
            Describe your video's <strong>core content only</strong>.
            <span style="color: #ef4444; display: block; margin-top: 0.5rem; font-size: 0.9rem;">
                ⚠️ Skip ad/sponsorship segments. AI analyzes based on this description.
            </span>
        </p>
    </label>
    <textarea id="video_description" name="video_description" rows="6" 
              placeholder="Example: 'Tutorial showing 3 paper airplane designs. Starts with basic dart, then Nakamura lock, finally Suzanne for distance. Key moments: 0:30 basic fold, 1:45 advanced technique, 3:20 flight test.'"
              style="width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem;"></textarea>
</div>
            
            <div style="text-align: center; margin: 2rem 0;">
                <button type="submit" style="padding: 1rem 3rem; font-size: 1.2rem;">
                    <i class="fas fa-chart-line"></i> Analyze & Optimize Video
                </button>
                <p style="margin-top: 1rem; color: #6b7280;">
                    <i class="fas fa-clock"></i> AI analysis takes 15-30 seconds
                </p>
            </div>
        </form>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/wizard/step5?platform={platform}&type={type}&goal={goal}&audience={audience}" 
               role="button" class="secondary">Back</a>
        </div>
    </div>

    

    '''
    return HTMLResponse(layout("Step 6: Video Details", content))

# ========== PROCESS ==========
@app.post("/process")
async def process_video(
    platform: str = Form(...),
    type: str = Form(...),
    goal: str = Form(...),
    audience: str = Form(...),
    tone: str = Form(...),
    video_url: str = Form(""),
    video_description: str = Form("")
):
    # Show loading page
    loading_content = f'''
    <div style="max-width: 800px; margin: 0 auto; text-align: center; padding: 4rem 0;">
        <div style="font-size: 4rem; color: var(--primary); margin-bottom: 2rem;">
            <i class="fas fa-chart-line"></i>
        </div>
        
        <h1 style="color: var(--primary);">Analyzing Your Video...</h1>
        <p style="font-size: 1.2rem; color: #6b7280; max-width: 500px; margin: 1rem auto;">
            Checking {platform.title()} best practices for {type} videos...
        </p>
        
        <div class="loading-bar">
            <div class="loading-progress"></div>
        </div>
        
        <p style="color: #6b7280; margin-top: 2rem;">
            Analyzing: {video_url[:50] if video_url else "Your video description"}...
        </p>
        
        <!-- Auto-refresh to result after 3 seconds -->
        <meta http-equiv="refresh" content="3;url=/result?platform={platform}&type={type}&goal={goal}&audience={audience}&tone={tone}&video_url={video_url}&video_description={video_description}">
    </div>
    '''
    
    return HTMLResponse(layout("Analyzing...", loading_content))

# ========== RESULT ==========
@app.get("/result")
async def show_result(
    platform: str = Query(...),
    type: str = Query(...),
    goal: str = Query(...),
    audience: str = Query(...),
    tone: str = Query(...),
    video_url: str = Query(""),
    video_description: str = Query("")
):
    # For now, simulate AI analysis until we implement real YouTube API + GPT-4 Vision
    analysis_prompt = f"""You are a video STRUCTURE optimization expert for {platform}.

VIDEO CONTEXT:
- Platform: {platform}
- Video type: {type}
- Target audience: {audience}
- Desired tone: {tone}
- Goal: {goal}

USER'S BRIEF DESCRIPTION: "{video_description}"

NOTE: User provided a brief description. This analysis focuses on 
STRUCTURAL optimization for a "{type}" style video on {platform}. 
The advice applies regardless of the specific subject matter.

YOUR TASK: Provide STRUCTURAL optimization advice ONLY.
DO NOT analyze if the content is accurate or good.
DO NOT make assumptions about specific video content.

FOCUS ON:
1. **Hook suggestions** (first 5-10 seconds)
2. **Retention strategies** (prevent viewer drop-off)
3. **{platform} SEO** (titles, description, tags optimization)
4. **Engagement tactics** (CTAs, comments, community)
5. **Thumbnail & title synergy**
6. **Platform-specific features** (chapters, end screens, etc.)

CRITICAL: Format your response EXACTLY like this example:

OVERALL SCORE: 8/10 - {platform} optimization potential based on current structure

HOOK SUGGESTIONS:
1. "Hook text here" - Brief explanation why it works for this audience
2. "Hook text here" - Brief explanation why it works for this audience
3. "Hook text here" - Brief explanation why it works for this audience

RETENTION STRATEGIES:
- Strategy 1: Explanation and implementation tip
- Strategy 2: Explanation and implementation tip
- Strategy 3: Explanation and implementation tip

PLATFORM SEO:
- Title optimization: Specific title suggestions with keywords
- Description template: Template with placeholders
- Tag suggestions: Top 5-7 relevant tags
- Chapter recommendations: Specific timestamps and titles

ENGAGEMENT TACTICS:
- CTA placement: Where and how to ask for engagement
- Comment strategy: How to seed and respond to comments
- Community building: Specific steps for this video type

THUMBNAIL & TITLE SYNERGY:
- Visual elements to include: Specific items or emotions
- Text overlay: Exact text to use (short)
- Color psychology: Colors that work for this audience/tone

PLATFORM FEATURES:
- Specific features to use: Chapters, end screens, cards, etc.
- Implementation tips: How to set them up for this video
- Timing suggestions: When to trigger them

QUICK WINS (<10 minute fixes):
1. Quick fix 1
2. Quick fix 2
3. Quick fix 3

LONG-TERM STRATEGY:
- Next video planning: How to follow up
- Series potential: If applicable
- Audience growth: Specific tactics for this niche

IMPORTANT: Always start with "OVERALL SCORE: X/10" where X is a number 1-10, followed by a brief explanation."""
    
    try:
        # For now, use text-only analysis. Later: YouTube API + GPT-4 Vision
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a video optimization expert for YouTube, TikTok, Instagram, and LinkedIn. Format your responses exactly as requested."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "stream": False
            },
            timeout=45
        )
        
        if response.status_code == 200:
            ai_text = response.json()["choices"][0]["message"]["content"]
            
            # YOUR TURQUOISE COLOR: #0d96c1
            TURQUOISE = "#0d96c1"
            TURQUOISE_LIGHT = "#ecfeff"
            TURQUOISE_DARK = "#0c4a6e"
            
            # Parse AI response into sections
            sections = {}
            current_section = None
            current_content = []
            
            for line in ai_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if line starts a new section (ends with colon)
                if line.endswith(':'):
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = line.rstrip(':')
                    current_content = []
                elif current_section:
                    current_content.append(line)
            
            # Save last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Build analysis cards
            analysis_html = ""
            
            # Define section icons and order
            section_config = [
                ("HOOK SUGGESTIONS", "fa-fish-hook", "Start strong with these hooks"),
                ("RETENTION STRATEGIES", "fa-chart-line", "Keep viewers watching"),
                ("PLATFORM SEO", "fa-search", "Optimize for discovery"),
                ("ENGAGEMENT TACTICS", "fa-comments", "Build community"),
                ("THUMBNAIL & TITLE SYNERGY", "fa-eye", "Increase click-through"),
                ("PLATFORM FEATURES", "fa-cogs", "Use platform tools"),
                ("QUICK WINS", "fa-bolt", "Fast improvements"),
                ("LONG-TERM STRATEGY", "fa-chess-board", "Sustainable growth")
            ]
            
            for i, (section_title, icon, description) in enumerate(section_config):
                if section_title in sections:
                    content = sections[section_title]
                    # Format bullet points and numbered lists
                    formatted_content = content.replace('- ', '<span style="color: #0c4a6e;">•</span> ')
                    formatted_content = formatted_content.replace('1. ', '<br><span style="font-weight: bold; color: #0d96c1;">1.</span> ')
                    formatted_content = formatted_content.replace('2. ', '<br><span style="font-weight: bold; color: #0d96c1;">2.</span> ')
                    formatted_content = formatted_content.replace('3. ', '<br><span style="font-weight: bold; color: #0d96c1;">3.</span> ')
                    
                    analysis_html += f'''
<div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; border: 2px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.1);">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <div style="background: {TURQUOISE}; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">
            <i class="fas {icon}"></i>
        </div>
        <div>
            <h3 style="margin: 0; color: {TURQUOISE};">{section_title.replace('_', ' ').title()}</h3>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: #64748b;">{description}</p>
        </div>
    </div>
    
    <div style="font-size: 1rem; line-height: 1.6; color: {TURQUOISE_DARK}; padding: 1rem; background: {TURQUOISE_LIGHT}; border-radius: 8px; border-left: 4px solid {TURQUOISE};">
        {formatted_content}
    </div>
</div>
'''
            
            # Add overall score if present - IMPROVED PARSING
            if "OVERALL SCORE" in ai_text:
                # Better score extraction from the text
                score_line = None
                for line in ai_text.split('\n'):
                    if "OVERALL SCORE" in line or "SCORE:" in line or "/10" in line:
                        score_line = line.strip()
                        break
                
                score = "8"  # default
                if score_line:
                    # Extract numeric score with regex
                    import re
                    score_match = re.search(r'(\d+(?:\.\d+)?)/10', score_line)
                    if score_match:
                        score = score_match.group(1)
                    else:
                        # Try to find any number before /10
                        score_match = re.search(r'(\d+(?:\.\d+)?)\s*/10', ai_text)
                        if score_match:
                            score = score_match.group(1)
                
                # Get score explanation if available
                score_explanation = ""
                if "OVERALL SCORE" in sections:
                    score_text = sections["OVERALL SCORE"]
                    # Remove the numeric score part for explanation
                    score_explanation = re.sub(r'\d+(?:\.\d+)?/10[:\s]*', '', score_text).strip()
                    if score_explanation and len(score_explanation) > 200:
                        score_explanation = score_explanation[:200] + "..."
                
                # Determine score color
                try:
                    score_num = float(score)
                    if score_num >= 8:
                        score_color = "#059669"  # emerald
                        score_icon = "fa-trophy"
                    elif score_num >= 6:
                        score_color = TURQUOISE  # your turquoise
                        score_icon = "fa-chart-line"
                    elif score_num >= 4:
                        score_color = "#d97706"  # amber
                        score_icon = "fa-exclamation-triangle"
                    else:
                        score_color = "#dc2626"  # red
                        score_icon = "fa-exclamation-circle"
                except:
                    score_color = TURQUOISE
                    score_icon = "fa-star"
                
                score_html = f'''
<div style="background: white; border-radius: 12px; padding: 2rem; margin: 2rem 0; border: 3px solid {score_color}; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15); text-align: center;">
    <div style="font-size: 0.9rem; color: {score_color}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
        <i class="fas {score_icon}"></i> Platform Optimization Score
    </div>
    <div style="font-size: 4rem; font-weight: bold; color: {score_color}; margin: 0.5rem 0; line-height: 1;">
        {score}<span style="font-size: 2rem; opacity: 0.7;">/10</span>
    </div>
    <div style="font-size: 1.1rem; color: #374151; margin-top: 0.5rem;">
        {platform.title()} • {type.title()} • {audience.title()}
    </div>
    {f'<div style="font-size: 0.95rem; color: #4b5563; margin-top: 1rem; padding: 0.75rem; background: {TURQUOISE_LIGHT}; border-radius: 6px; border-left: 3px solid {score_color};">{score_explanation}</div>' if score_explanation else ''}
    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 1.5rem;">
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-video"></i> {type.title()}</span>
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-users"></i> {audience.title()}</span>
        <span style="font-size: 0.8rem; color: #6b7280;"><i class="fas fa-bullseye"></i> {goal.title()}</span>
    </div>
</div>
'''
                # Insert at beginning
                analysis_html = score_html + analysis_html
            else:
                # If no score found, create a default score card
                score_html = f'''
<div style="background: white; border-radius: 12px; padding: 2rem; margin: 2rem 0; border: 3px solid {TURQUOISE}; box-shadow: 0 4px 12px rgba(13, 150, 193, 0.15); text-align: center;">
    <div style="font-size: 0.9rem; color: {TURQUOISE}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
        <i class="fas fa-chart-line"></i> Platform Optimization Score
    </div>
    <div style="font-size: 4rem; font-weight: bold; color: {TURQUOISE}; margin: 0.5rem 0; line-height: 1;">
        8<span style="font-size: 2rem; opacity: 0.7;">/10</span>
    </div>
    <div style="font-size: 0.95rem; color: #4b5563; margin-top: 1rem; padding: 0.75rem; background: {TURQUOISE_LIGHT}; border-radius: 6px;">
        <i class="fas fa-info-circle"></i> Based on structural analysis of your {type.lower()} video for {platform}
    </div>
    <div style="font-size: 1.1rem; color: #374151; margin-top: 1rem;">
        {platform.title()} • {type.title()} • {audience.title()}
    </div>
</div>
'''
                analysis_html = score_html + analysis_html
            
            result_content = f'''
<div style="max-width: 800px; margin: 0 auto;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; color: {TURQUOISE};">
            <i class="fas fa-chart-line"></i>
        </div>
        <h1 style="color: {TURQUOISE};">Video Analysis Complete!</h1>
        <p style="color: #64748b;">Optimized for <strong>{platform.title()}</strong> • <strong>{type.title()}</strong> • <strong>{goal.title()}</strong></p>
        <div style="background: {TURQUOISE_LIGHT}; padding: 0.75rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #a5f3fc;">
            <p style="color: {TURQUOISE_DARK}; margin: 0;"><i class="fas fa-file-alt"></i> <strong>Video Description:</strong> {video_description[:100]}{'...' if len(video_description) > 100 else ''}</p>
        </div>
    </div>
    
    {analysis_html}
    
    <div style="text-align: center; margin-top: 3rem;">
        <a href="/wizard" role="button" style="margin-right: 1rem; background: {TURQUOISE}; border-color: {TURQUOISE};">
            <i class="fas fa-video"></i> Analyze Another Video
        </a>
        <a href="/" role="button" style="background: #64748b; border-color: #64748b;">
            <i class="fas fa-home"></i> Dashboard
        </a>
    </div>
</div>
'''
        else:
            TURQUOISE = "#0d96c1"
            result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> API Error</h1>
    <p>Analysis failed. Status: {response.status_code}</p>
    <a href="/wizard/step6?platform={platform}&type={type}&goal={goal}&audience={audience}&tone={tone}" 
       role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Try Again</a>
</div>
'''
    except Exception as e:
        TURQUOISE = "#0d96c1"
        result_content = f'''
<div style="max-width: 800px; margin: 0 auto; text-align: center;">
    <h1 style="color: #dc2626;"><i class="fas fa-exclamation-triangle"></i> Analysis Error</h1>
    <p>{str(e)}</p>
    <p><small>Note: Full video analysis requires YouTube API access. Currently using description-only analysis.</small></p>
    <a href="/" role="button" style="margin-top: 2rem; background: {TURQUOISE}; border-color: {TURQUOISE};">Start Over</a>
</div>
'''
    
    return HTMLResponse(layout("Analysis Results", result_content))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port than Prompt Wizard
