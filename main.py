"""
LUMINA - לומינה
מערכת מחקר עסקי מולטי-סוכן
הרצה: python main.py
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Windows Unicode fix
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("❌ שגיאה: ANTHROPIC_API_KEY לא מוגדר")
    print("הגדר את המפתח: set ANTHROPIC_API_KEY=your_key_here")
    sys.exit(1)

from src.domains import DOMAINS
from src.agents import OrchestratorAgent

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    orchestrator = OrchestratorAgent(domains=DOMAINS, output_dir=output_dir)
    orchestrator.run_sequential()


if __name__ == "__main__":
    main()
