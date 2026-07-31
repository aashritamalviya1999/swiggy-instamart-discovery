import argparse
import sys
import subprocess
import logging
from src.agents.pipeline_orchestrator import PipelineOrchestrator

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline(target_count: int):
    logger.info(f"Executing 7-Agent AI Discovery Pipeline (Target Count: {target_count})...")
    orchestrator = PipelineOrchestrator()
    res = orchestrator.run_pipeline(target_count=target_count)
    
    print("\n" + "="*50)
    print("      SWIGGY INSTAMART AI PIPELINE RUN COMPLETE")
    print("="*50)
    print(f"Reviews Collected:         {res['reviews_collected']}")
    print(f"Reviews Cleaned & Filtered: {res['reviews_cleaned']}")
    print(f"Reviews AI Analyzed:       {res['reviews_analyzed']}")
    print(f"PM Insights Synthesized:   {res['insights_generated']}")
    print(f"Opportunities Discovered:  {res['opportunities_generated']}")
    print("="*50 + "\n")

def run_dashboard():
    logger.info("Launching Streamlit dashboard (Blue, Orange & White Theme)...")
    try:
        cmd = ["streamlit", "run", "src/dashboard/app.py"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        logger.info("Dashboard stopped.")
    except Exception as e:
        logger.error(f"Failed to launch Streamlit dashboard: {e}")

def run_api():
    logger.info("Launching FastAPI REST server...")
    try:
        import uvicorn
        uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        logger.info("FastAPI stopped.")
    except Exception as e:
        logger.error(f"Failed to launch FastAPI backend: {e}")

def main():
    parser = argparse.ArgumentParser(description="Swiggy Instamart AI Product Discovery Engine Command Line CLI.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pipeline", action="store_true", help="Run the data collection and AI analysis pipeline")
    group.add_argument("--dashboard", action="store_true", help="Launch the interactive Streamlit dashboard")
    group.add_argument("--api", action="store_true", help="Launch the FastAPI server")
    
    parser.add_argument("-n", "--count", type=int, default=1000, help="Number of records to process (default: 1000)")
    
    args = parser.parse_args()
    
    if args.pipeline:
        run_pipeline(args.count)
    elif args.dashboard:
        run_dashboard()
    elif args.api:
        run_api()

if __name__ == "__main__":
    main()
