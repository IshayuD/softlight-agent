"""
Task Runner: Execute multiple UI capture tasks
"""

import asyncio
import json
from pathlib import Path
from agent_b import AgentB


# Define test tasks
TASKS = [
    # LINEAR TASKS
    {
        "app": "Linear",
        "description": "Create a new project in Linear",
        "url": "https://linear.app/test916/team/TES/active",
        "expected_states": [
            "Projects list view",
            "Create project button visible",
            "Create project modal open",
            "Project name input field",
            "Project settings options",
            "Success state with new project"
        ]
    },
    {
        "app": "Linear",
        "description": "Create a new issue in Linear",
        "url": "https://linear.app/test916/team/TES/active",
        "expected_states": [
            "Issues board view",
            "New issue button visible",
            "Issue creation modal",
            "Title and description fields",
            "Priority and assignee options",
            "Issue created confirmation"
        ]
    },
    {
        "app": "Linear",
        "description": "Filter issues by status in Linear",
        "url": "https://linear.app/test916/team/TES/active",
        "expected_states": [
            "Issues view with filters",
            "Filter menu button",
            "Filter dropdown expanded",
            "Status filter options",
            "Applied filter view",
            "Filtered results displayed"
        ]
    },
    
    # NOTION TASKS
    {
        "app": "Notion",
        "description": "Create a new page in Notion",
        "url": "https://www.notion.so/",
        "expected_states": [
            "Notion workspace",
            "New page button",
            "Empty page editor",
            "Title input",
            "Content area",
            "Page saved"
        ]
    },
    {
        "app": "Notion",
        "description": "Filter a database by property in Notion",
        "url": "https://www.notion.so/",
        "expected_states": [
            "Database view",
            "Filter button visible",
            "Filter options panel",
            "Property selection",
            "Filter applied",
            "Filtered database results"
        ]
    }
]


async def run_all_tasks(headless: bool = False):
    """
    Run all defined tasks and generate comprehensive dataset
    """
    print("=" * 80)
    print("AGENT B: UI STATE CAPTURE SYSTEM")
    print("=" * 80)
    print(f"\nPreparing to capture {len(TASKS)} tasks across multiple apps\n")
    
    agent = AgentB()
    results = []
    
    try:
        await agent.initialize_browser(headless=headless)
        
        for i, task in enumerate(TASKS, 1):
            print("\n" + "=" * 80)
            print(f"TASK {i}/{len(TASKS)}: {task['app']}")
            print("=" * 80)
            print(f"Description: {task['description']}")
            print(f"URL: {task['url']}")
            print(f"Expected states: {len(task['expected_states'])}")
            print()
            
            try:
                manifest_path = await agent.execute_task(
                    task_description=task['description'],
                    start_url=task['url'],
                    max_steps=15
                )
                
                results.append({
                    "task": task['description'],
                    "app": task['app'],
                    "status": "success",
                    "manifest": str(manifest_path)
                })
                
                print(f"\n✅ Task {i} completed successfully!")
                
                # Brief pause between tasks
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"\n❌ Task {i} failed: {e}")
                results.append({
                    "task": task['description'],
                    "app": task['app'],
                    "status": "failed",
                    "error": str(e)
                })
        
    finally:
        await agent.close_browser()
    
    # Generate summary report
    generate_summary_report(results)
    
    print("\n" + "=" * 80)
    print("ALL TASKS COMPLETED")
    print("=" * 80)
    print(f"\nTotal tasks: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'failed')}")
    print("\nDataset location: ./captured_states/")
    print("Summary report: ./dataset_summary.json")


def generate_summary_report(results: list):
    """
    Generate a summary report of all captured tasks
    """
    report = {
        "total_tasks": len(results),
        "successful_tasks": sum(1 for r in results if r['status'] == 'success'),
        "failed_tasks": sum(1 for r in results if r['status'] == 'failed'),
        "apps_covered": list(set(r['app'] for r in results)),
        "tasks": results,
        "dataset_structure": {
            "root": "captured_states/",
            "format": "Each task has its own directory with manifest.json and screenshots",
            "manifest_fields": [
                "task",
                "total_steps",
                "states (array of state objects)",
                "captured_at"
            ],
            "state_fields": [
                "step",
                "description",
                "timestamp",
                "url",
                "screenshot",
                "viewport",
                "title",
                "metadata"
            ]
        }
    }
    
    # Save report
    with open("dataset_summary.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n📊 Summary report generated: dataset_summary.json")


async def run_single_task(task_index: int = 0, headless: bool = False):
    """
    Run a single task for testing
    """
    if task_index >= len(TASKS):
        print(f"Invalid task index. Available tasks: 0-{len(TASKS)-1}")
        return
    
    task = TASKS[task_index]
    print(f"\n🎯 Running single task: {task['description']}\n")
    
    agent = AgentB()
    
    try:
        await agent.initialize_browser(headless=headless)
        
        manifest_path = await agent.execute_task(
            task_description=task['description'],
            start_url=task['url'],
            max_steps=15
        )
        
        print(f"\n✅ Task completed! Manifest: {manifest_path}")
        
    finally:
        await agent.close_browser()


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            # Run all tasks
            asyncio.run(run_all_tasks(headless=False))
        elif sys.argv[1].isdigit():
            # Run specific task by index
            task_idx = int(sys.argv[1])
            asyncio.run(run_single_task(task_idx, headless=False))
        else:
            print("Usage:")
            print("  python run_tasks.py          # Show help")
            print("  python run_tasks.py all      # Run all tasks")
            print("  python run_tasks.py 0        # Run specific task by index")
    else:
        print("\n🤖 Agent B Task Runner")
        print("\nAvailable tasks:")
        for i, task in enumerate(TASKS):
            print(f"  {i}: [{task['app']}] {task['description']}")
        print("\nUsage:")
        print("  python run_tasks.py all      # Run all tasks")
        print("  python run_tasks.py 0        # Run specific task")
        print()