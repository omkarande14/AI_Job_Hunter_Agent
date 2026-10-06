import time
from ddgs import DDGS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Broad & High-Yield Search Queries (LinkedIn, Naukri, Indeed)
TARGET_QUERIES = [
    "AI ML Engineer Intern Remote jobs LinkedIn Naukri",
    "Generative AI Developer Remote internship Naukri Indeed",
    "Data Engineer Intern Remote jobs LinkedIn"
]

# -------------------------------------------------------------------
# 1. Open Live Web Search Aggregator
# -------------------------------------------------------------------
class LiveJobFetcher:
    def __init__(self):
        self.ddgs = DDGS()

    def fetch_jobs(self, query):
        print(f"🔍 Searching Live Jobs: '{query}'...")
        cleaned_jobs = []
        try:
            # Fetching fresh web results
            results = list(self.ddgs.text(query, max_results=5))
            for item in results:
                title = item.get("title", "N/A")
                snippet = item.get("body", "")
                link = item.get("href", "N/A")

                # Anti-Spam Check
                if "registration fee" in snippet.lower() or "deposit" in snippet.lower():
                    continue

                cleaned_jobs.append({
                    "title": title,
                    "company": "Verified Portal Listing",
                    "platform": "Live Web Search",
                    "location": "Remote",
                    "jd": snippet[:400],
                    "apply_link": link
                })
            return cleaned_jobs
        except Exception as e:
            print(f"❌ Fetch Error: {e}")
            return []


# -------------------------------------------------------------------
# 2. AI Evaluator Agent (Llama 3 8B)
# -------------------------------------------------------------------
class AIJobAgent:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3:8b", temperature=0.1, num_ctx=1024)

    def evaluate_and_match(self, user_resume, job_details):
        prompt = PromptTemplate.from_template(
            """
            You are a Senior AI Recruiter. Evaluate this live job opportunity for a candidate.

            Candidate Resume Profile:
            {resume}

            Live Job Listing Title: {job_title}
            Job Details/Snippet:
            {jd}

            Perform the following analysis:
            1. Match Score (%): Objective score from 0% to 100% based on technical skills.
            2. Core Matching Skills: List top 2-3 matching technical skills.
            3. HR Outreach Note: Draft a concise 3-sentence application pitch for HR.

            Output Format:
            Match Score: [Score]%
            Key Matches: [Skills]
            Tailored HR Pitch: [Message]
            """
        )

        chain = prompt | self.llm
        return chain.invoke({
            "resume": user_resume, 
            "job_title": job_details["title"],
            "jd": job_details["jd"]
        })


# -------------------------------------------------------------------
# 3. Main Execution Workflow
# -------------------------------------------------------------------
if __name__ == "__main__":
    fetcher = LiveJobFetcher()
    agent = AIJobAgent()

    my_resume_profile = """
    B.Tech AI/ML Student skilled in Python, SQL, PyTorch, LangChain, ChromaDB, 
    Ollama (Llama 3 8B), Streamlit, RAG Systems, Data Structures, and Agentic Workflows.
    """

    print("="*65)
    print("🤖 Autonomous AI Job Discovery Agent (Live Engine)")
    print("="*65 + "\n")

    all_fetched_jobs = []
    seen_links = set()

    for query in TARGET_QUERIES:
        jobs = fetcher.fetch_jobs(query)
        for j in jobs:
            if j["apply_link"] not in seen_links:
                seen_links.add(j["apply_link"])
                all_fetched_jobs.append(j)
        time.sleep(1)

    print(f"\n✅ Total Unique Live Jobs Found: {len(all_fetched_jobs)}\n")

    if all_fetched_jobs:
        for idx, job in enumerate(all_fetched_jobs[:3], 1):
            print(f"--- 📍 Job #{idx}: {job['title']} ---")
            
            evaluation = agent.evaluate_and_match(my_resume_profile, job)
            print("\n🧠 AI Evaluation & HR Pitch:")
            print(evaluation)
            print(f"\n🔗 Direct Apply Link: {job['apply_link']}")
            print("-" * 65 + "\n")
    else:
        print("⚠️ No jobs found.")