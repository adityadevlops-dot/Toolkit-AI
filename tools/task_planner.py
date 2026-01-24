"""
Task Planner Tool - Plan and organize tasks with priorities and timelines.
"""

from .base_tool import BaseTool
from datetime import datetime, timedelta


class TaskPlannerTool(BaseTool):
    """Plan, organize, and manage tasks with priorities, deadlines, and dependencies."""
    
    def __init__(self):
        super().__init__()
        self.name = "task_planner"
        self.description = "Plan and organize tasks with priorities, deadlines, dependencies, time estimates, and project breakdowns."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["create", "breakdown", "schedule", "prioritize", "estimate", "timeline", "dependencies", "daily_plan"],
                    "description": "Operation to perform",
                    "default": "create"
                },
                "task": {
                    "type": "string",
                    "description": "Main task or project description"
                },
                "subtasks": {
                    "type": "string",
                    "description": "Comma-separated list of subtasks"
                },
                "deadline": {
                    "type": "string",
                    "description": "Deadline date (YYYY-MM-DD)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Task priority",
                    "default": "medium"
                },
                "hours_available": {
                    "type": "number",
                    "description": "Hours available per day for work",
                    "default": 8
                },
                "category": {
                    "type": "string",
                    "description": "Task category (work, personal, study, etc.)"
                }
            },
            "required": ["task"]
        }
        
        self._priority_weights = {
            "high": 3,
            "medium": 2,
            "low": 1
        }
        
        self._task_templates = {
            "software_project": [
                "Requirements gathering",
                "System design",
                "Database design",
                "Frontend development",
                "Backend development",
                "API integration",
                "Testing",
                "Bug fixes",
                "Documentation",
                "Deployment"
            ],
            "presentation": [
                "Research topic",
                "Create outline",
                "Gather resources",
                "Design slides",
                "Add content",
                "Add visuals",
                "Practice delivery",
                "Get feedback",
                "Final revisions"
            ],
            "report": [
                "Define scope",
                "Research",
                "Create outline",
                "Write introduction",
                "Write main content",
                "Write conclusion",
                "Add references",
                "Proofread",
                "Format document",
                "Final review"
            ],
            "event": [
                "Define objectives",
                "Set budget",
                "Choose venue",
                "Create guest list",
                "Send invitations",
                "Arrange catering",
                "Plan activities",
                "Prepare materials",
                "Confirm attendees",
                "Final preparations"
            ],
            "learning": [
                "Define learning goals",
                "Gather resources",
                "Create study schedule",
                "Study fundamentals",
                "Practice exercises",
                "Build projects",
                "Review and revise",
                "Take assessments",
                "Apply knowledge"
            ]
        }
    
    def execute(self, task, operation="create", subtasks=None, deadline=None, priority="medium", hours_available=8, category=None):
        try:
            if not task:
                return "Please provide a task description."
            
            subtask_list = []
            if subtasks:
                subtask_list = [s.strip() for s in subtasks.split(",")]
            
            if operation == "create":
                return self._create_task(task, subtask_list, deadline, priority, category)
            elif operation == "breakdown":
                return self._breakdown_task(task, subtask_list, category)
            elif operation == "schedule":
                return self._schedule_task(task, subtask_list, deadline, hours_available)
            elif operation == "prioritize":
                return self._prioritize_tasks(task, subtask_list, priority)
            elif operation == "estimate":
                return self._estimate_time(task, subtask_list)
            elif operation == "timeline":
                return self._create_timeline(task, subtask_list, deadline, hours_available)
            elif operation == "dependencies":
                return self._analyze_dependencies(task, subtask_list)
            elif operation == "daily_plan":
                return self._create_daily_plan(task, subtask_list, hours_available, priority)
            else:
                return self._create_task(task, subtask_list, deadline, priority, category)
                
        except Exception as e:
            return "Task planning error: " + str(e)
    
    def _create_task(self, task, subtasks, deadline, priority, category):
        result = "TASK PLAN\n"
        result += "=" * 50 + "\n\n"
        
        result += "MAIN TASK\n"
        result += "-" * 30 + "\n"
        result += "Title: " + task + "\n"
        result += "Priority: " + priority.upper() + "\n"
        
        if category:
            result += "Category: " + category + "\n"
        
        if deadline:
            result += "Deadline: " + deadline + "\n"
            
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                today = datetime.now()
                days_left = (deadline_date - today).days
                
                if days_left < 0:
                    result += "Status: OVERDUE by " + str(abs(days_left)) + " days\n"
                elif days_left == 0:
                    result += "Status: DUE TODAY\n"
                elif days_left == 1:
                    result += "Status: Due tomorrow\n"
                else:
                    result += "Status: " + str(days_left) + " days remaining\n"
            except ValueError:
                pass
        
        result += "\n"
        
        if subtasks:
            result += "SUBTASKS (" + str(len(subtasks)) + ")\n"
            result += "-" * 30 + "\n"
            
            for i, subtask in enumerate(subtasks):
                result += "[ ] " + str(i + 1) + ". " + subtask + "\n"
        else:
            result += "SUGGESTED SUBTASKS\n"
            result += "-" * 30 + "\n"
            
            suggestions = self._suggest_subtasks(task)
            for i, subtask in enumerate(suggestions):
                result += "[ ] " + str(i + 1) + ". " + subtask + "\n"
        
        result += "\n"
        result += "NEXT STEPS\n"
        result += "-" * 30 + "\n"
        result += "1. Review and adjust subtasks as needed\n"
        result += "2. Estimate time for each subtask\n"
        result += "3. Identify dependencies between tasks\n"
        result += "4. Schedule work sessions\n"
        result += "5. Track progress daily\n"
        
        return result
    
    def _suggest_subtasks(self, task):
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["software", "app", "application", "program", "code", "develop"]):
            return self._task_templates["software_project"]
        elif any(word in task_lower for word in ["presentation", "slides", "pitch", "demo"]):
            return self._task_templates["presentation"]
        elif any(word in task_lower for word in ["report", "document", "paper", "essay", "article"]):
            return self._task_templates["report"]
        elif any(word in task_lower for word in ["event", "party", "meeting", "conference", "workshop"]):
            return self._task_templates["event"]
        elif any(word in task_lower for word in ["learn", "study", "course", "training", "skill"]):
            return self._task_templates["learning"]
        else:
            return [
                "Define objectives and scope",
                "Research and gather information",
                "Create detailed plan",
                "Execute main tasks",
                "Review and refine",
                "Get feedback",
                "Make final adjustments",
                "Complete and deliver"
            ]
    
    def _breakdown_task(self, task, subtasks, category):
        result = "TASK BREAKDOWN\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        result += "PHASE BREAKDOWN\n"
        result += "-" * 30 + "\n\n"
        
        phases = self._group_into_phases(subtasks)
        
        for phase_name, phase_tasks in phases.items():
            result += phase_name.upper() + "\n"
            
            for i, t in enumerate(phase_tasks):
                result += "  " + str(i + 1) + ". " + t["name"] + "\n"
                result += "     Est. time: " + str(t["hours"]) + " hours\n"
                result += "     Priority: " + t["priority"] + "\n"
            
            result += "\n"
        
        total_hours = sum(t["hours"] for phase in phases.values() for t in phase)
        
        result += "SUMMARY\n"
        result += "-" * 30 + "\n"
        result += "Total phases: " + str(len(phases)) + "\n"
        result += "Total tasks: " + str(len(subtasks)) + "\n"
        result += "Estimated total time: " + str(total_hours) + " hours\n"
        result += "Working days (8hr): " + str(round(total_hours / 8, 1)) + " days\n"
        
        return result
    
    def _group_into_phases(self, subtasks):
        phases = {
            "Planning": [],
            "Execution": [],
            "Review": []
        }
        
        for subtask in subtasks:
            subtask_lower = subtask.lower()
            
            hours = self._estimate_task_hours(subtask)
            priority = "medium"
            
            if any(word in subtask_lower for word in ["plan", "define", "research", "gather", "design", "scope", "requirement"]):
                phases["Planning"].append({"name": subtask, "hours": hours, "priority": priority})
            elif any(word in subtask_lower for word in ["review", "test", "refine", "feedback", "final", "proofread", "deploy"]):
                phases["Review"].append({"name": subtask, "hours": hours, "priority": priority})
            else:
                phases["Execution"].append({"name": subtask, "hours": hours, "priority": priority})
        
        return {k: v for k, v in phases.items() if v}
    
    def _estimate_task_hours(self, task):
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["research", "study", "analyze", "develop", "build", "create"]):
            return 4
        elif any(word in task_lower for word in ["test", "review", "refine", "revise"]):
            return 2
        elif any(word in task_lower for word in ["plan", "define", "outline"]):
            return 1
        elif any(word in task_lower for word in ["deploy", "launch", "publish"]):
            return 3
        else:
            return 2
    
    def _schedule_task(self, task, subtasks, deadline, hours_available):
        result = "TASK SCHEDULE\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n"
        result += "Hours available per day: " + str(hours_available) + "\n"
        
        if deadline:
            result += "Deadline: " + deadline + "\n"
        
        result += "\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        today = datetime.now()
        current_date = today
        
        result += "SCHEDULED TASKS\n"
        result += "-" * 30 + "\n\n"
        
        hours_remaining = hours_available
        day_num = 1
        
        result += "Day " + str(day_num) + " - " + current_date.strftime("%A, %b %d") + "\n"
        
        for subtask in subtasks:
            task_hours = self._estimate_task_hours(subtask)
            
            if task_hours <= hours_remaining:
                result += "  [" + str(task_hours) + "h] " + subtask + "\n"
                hours_remaining -= task_hours
            else:
                if hours_remaining > 0:
                    result += "  [" + str(hours_remaining) + "h] " + subtask + " (partial)\n"
                    task_hours -= hours_remaining
                
                while task_hours > 0:
                    day_num += 1
                    current_date += timedelta(days=1)
                    
                    if current_date.weekday() >= 5:
                        current_date += timedelta(days=7 - current_date.weekday())
                    
                    result += "\nDay " + str(day_num) + " - " + current_date.strftime("%A, %b %d") + "\n"
                    
                    hours_to_use = min(task_hours, hours_available)
                    result += "  [" + str(hours_to_use) + "h] " + subtask
                    
                    if task_hours > hours_available:
                        result += " (continued)"
                    
                    result += "\n"
                    task_hours -= hours_to_use
                    hours_remaining = hours_available - hours_to_use
        
        result += "\n"
        result += "SCHEDULE SUMMARY\n"
        result += "-" * 30 + "\n"
        result += "Start date: " + today.strftime("%Y-%m-%d") + "\n"
        result += "End date: " + current_date.strftime("%Y-%m-%d") + "\n"
        result += "Working days: " + str(day_num) + "\n"
        
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                if current_date <= deadline_date:
                    result += "Status: On track to meet deadline\n"
                else:
                    days_over = (current_date - deadline_date).days
                    result += "Status: WARNING - Schedule exceeds deadline by " + str(days_over) + " days\n"
            except ValueError:
                pass
        
        return result
    
    def _prioritize_tasks(self, task, subtasks, default_priority):
        result = "TASK PRIORITIZATION\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        prioritized = []
        
        for subtask in subtasks:
            subtask_lower = subtask.lower()
            
            if any(word in subtask_lower for word in ["urgent", "critical", "deadline", "blocker", "required"]):
                priority = "high"
            elif any(word in subtask_lower for word in ["important", "key", "main", "core"]):
                priority = "high"
            elif any(word in subtask_lower for word in ["optional", "nice to have", "if time"]):
                priority = "low"
            elif any(word in subtask_lower for word in ["review", "refine", "polish"]):
                priority = "medium"
            else:
                priority = default_priority
            
            impact = self._estimate_impact(subtask)
            effort = self._estimate_task_hours(subtask)
            
            score = (self._priority_weights[priority] * 10) + (impact * 5) - (effort * 0.5)
            
            prioritized.append({
                "task": subtask,
                "priority": priority,
                "impact": impact,
                "effort": effort,
                "score": score
            })
        
        prioritized.sort(key=lambda x: x["score"], reverse=True)
        
        result += "PRIORITIZED TASK LIST\n"
        result += "-" * 30 + "\n\n"
        
        result += "Priority | Impact | Effort | Task\n"
        result += "-" * 50 + "\n"
        
        for item in prioritized:
            priority_symbol = {"high": "!!!", "medium": "!! ", "low": "!  "}[item["priority"]]
            impact_bar = "*" * item["impact"]
            effort_str = str(item["effort"]) + "h"
            
            result += priority_symbol + "      | " + impact_bar.ljust(5) + " | " + effort_str.ljust(6) + " | " + item["task"] + "\n"
        
        result += "\n"
        result += "LEGEND\n"
        result += "-" * 30 + "\n"
        result += "!!! = High priority\n"
        result += "!!  = Medium priority\n"
        result += "!   = Low priority\n"
        result += "Impact: * to ***** (1-5)\n"
        
        result += "\n"
        result += "RECOMMENDATION\n"
        result += "-" * 30 + "\n"
        result += "Focus on these tasks first:\n"
        
        for item in prioritized[:3]:
            result += "1. " + item["task"] + " (" + item["priority"] + " priority)\n"
        
        return result
    
    def _estimate_impact(self, task):
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["critical", "essential", "core", "main", "key"]):
            return 5
        elif any(word in task_lower for word in ["important", "significant", "major"]):
            return 4
        elif any(word in task_lower for word in ["useful", "helpful", "good"]):
            return 3
        elif any(word in task_lower for word in ["minor", "small", "optional"]):
            return 2
        else:
            return 3
    
    def _estimate_time(self, task, subtasks):
        result = "TIME ESTIMATION\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        result += "TASK TIME ESTIMATES\n"
        result += "-" * 30 + "\n\n"
        
        total_min = 0
        total_likely = 0
        total_max = 0
        
        result += "Task".ljust(35) + " | Min | Likely | Max\n"
        result += "-" * 55 + "\n"
        
        for subtask in subtasks:
            likely = self._estimate_task_hours(subtask)
            min_hours = max(1, int(likely * 0.7))
            max_hours = int(likely * 1.5)
            
            total_min += min_hours
            total_likely += likely
            total_max += max_hours
            
            task_name = subtask[:33] + ".." if len(subtask) > 35 else subtask
            result += task_name.ljust(35) + " | " + str(min_hours).ljust(3) + " | " + str(likely).ljust(6) + " | " + str(max_hours) + "\n"
        
        result += "-" * 55 + "\n"
        result += "TOTAL".ljust(35) + " | " + str(total_min).ljust(3) + " | " + str(total_likely).ljust(6) + " | " + str(total_max) + "\n"
        
        result += "\n"
        result += "TIME SUMMARY\n"
        result += "-" * 30 + "\n"
        result += "Optimistic: " + str(total_min) + " hours (" + str(round(total_min / 8, 1)) + " days)\n"
        result += "Most likely: " + str(total_likely) + " hours (" + str(round(total_likely / 8, 1)) + " days)\n"
        result += "Pessimistic: " + str(total_max) + " hours (" + str(round(total_max / 8, 1)) + " days)\n"
        
        result += "\n"
        result += "RECOMMENDATION\n"
        result += "-" * 30 + "\n"
        result += "Plan for the 'Most likely' estimate but have\n"
        result += "contingency time for the 'Pessimistic' scenario.\n"
        result += "Buffer recommended: " + str(total_max - total_likely) + " hours\n"
        
        return result
    
    def _create_timeline(self, task, subtasks, deadline, hours_available):
        result = "PROJECT TIMELINE\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        today = datetime.now()
        
        result += "GANTT CHART (Text)\n"
        result += "-" * 30 + "\n\n"
        
        current_day = 0
        max_days = 0
        
        timeline_data = []
        
        for subtask in subtasks:
            hours = self._estimate_task_hours(subtask)
            days = max(1, round(hours / hours_available))
            
            start_day = current_day
            end_day = current_day + days
            
            timeline_data.append({
                "task": subtask,
                "start": start_day,
                "end": end_day,
                "days": days
            })
            
            current_day = end_day
            max_days = max(max_days, end_day)
        
        scale = min(30, max_days)
        
        result += "Task".ljust(25) + " | Timeline (each = represents ~1 day)\n"
        result += "-" * 60 + "\n"
        
        for item in timeline_data:
            task_name = item["task"][:23] + ".." if len(item["task"]) > 25 else item["task"]
            
            if max_days > 0:
                start_pos = int((item["start"] / max_days) * scale)
                bar_len = max(1, int((item["days"] / max_days) * scale))
            else:
                start_pos = 0
                bar_len = 1
            
            bar = " " * start_pos + "=" * bar_len
            
            result += task_name.ljust(25) + " |" + bar + "\n"
        
        result += "-" * 60 + "\n"
        result += "Day".ljust(25) + " |0" + " " * (scale - 2) + str(max_days) + "\n"
        
        result += "\n"
        result += "MILESTONES\n"
        result += "-" * 30 + "\n"
        
        quarter = len(subtasks) // 4
        
        if quarter > 0:
            result += "25% complete: After '" + subtasks[quarter - 1][:30] + "'\n"
        
        half = len(subtasks) // 2
        if half > 0:
            result += "50% complete: After '" + subtasks[half - 1][:30] + "'\n"
        
        three_quarter = (len(subtasks) * 3) // 4
        if three_quarter > 0 and three_quarter < len(subtasks):
            result += "75% complete: After '" + subtasks[three_quarter - 1][:30] + "'\n"
        
        result += "100% complete: After '" + subtasks[-1][:30] + "'\n"
        
        result += "\n"
        result += "DATES\n"
        result += "-" * 30 + "\n"
        result += "Start: " + today.strftime("%Y-%m-%d") + "\n"
        
        end_date = today + timedelta(days=max_days)
        result += "Projected end: " + end_date.strftime("%Y-%m-%d") + "\n"
        result += "Duration: " + str(max_days) + " working days\n"
        
        return result
    
    def _analyze_dependencies(self, task, subtasks):
        result = "DEPENDENCY ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        result += "PROJECT: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)
        
        result += "TASK DEPENDENCIES\n"
        result += "-" * 30 + "\n\n"
        
        for i, subtask in enumerate(subtasks):
            result += str(i + 1) + ". " + subtask + "\n"
            
            if i > 0:
                result += "   Depends on: " + str(i) + ". " + subtasks[i - 1][:30] + "\n"
            else:
                result += "   Depends on: None (can start immediately)\n"
            
            if i < len(subtasks) - 1:
                result += "   Blocks: " + str(i + 2) + ". " + subtasks[i + 1][:30] + "\n"
            else:
                result += "   Blocks: None (final task)\n"
            
            result += "\n"
        
        result += "CRITICAL PATH\n"
        result += "-" * 30 + "\n"
        result += "All tasks are on the critical path as they\n"
        result += "are sequentially dependent.\n\n"
        
        result += "Total tasks in critical path: " + str(len(subtasks)) + "\n"
        
        result += "\n"
        result += "PARALLEL OPPORTUNITIES\n"
        result += "-" * 30 + "\n"
        result += "Review tasks for potential parallel execution:\n"
        result += "- Independent research tasks\n"
        result += "- Documentation while developing\n"
        result += "- Testing while implementing new features\n"
        
        return result
    
    def _create_daily_plan(self, task, subtasks, hours_available, priority):
        result = "DAILY PLAN\n"
        result += "=" * 50 + "\n\n"
        
        today = datetime.now()
        result += "Date: " + today.strftime("%A, %B %d, %Y") + "\n"
        result += "Available hours: " + str(hours_available) + "\n"
        result += "Focus: " + task + "\n\n"
        
        if not subtasks:
            subtasks = self._suggest_subtasks(task)[:5]
        
        result += "TODAY'S SCHEDULE\n"
        result += "-" * 30 + "\n\n"
        
        current_hour = 9
        hours_left = hours_available
        
        result += "Morning Block (High Focus)\n"
        
        for i, subtask in enumerate(subtasks):
            if hours_left <= 0:
                break
            
            task_hours = min(2, hours_left)
            
            start_time = str(current_hour).zfill(2) + ":00"
            current_hour += task_hours
            end_time = str(current_hour).zfill(2) + ":00"
            
            result += "  " + start_time + " - " + end_time + ": " + subtask + "\n"
            hours_left -= task_hours
            
            if current_hour == 12:
                result += "\n  12:00 - 13:00: Lunch Break\n\n"
                result += "Afternoon Block (Moderate Focus)\n"
                current_hour = 13
            
            if i < len(subtasks) - 1 and hours_left > 0:
                result += "  " + str(current_hour).zfill(2) + ":00 - " + str(current_hour).zfill(2) + ":15: Short break\n"
                current_hour += 0.25
        
        result += "\n"
        result += "END OF DAY REVIEW\n"
        result += "-" * 30 + "\n"
        result += "[ ] Review completed tasks\n"
        result += "[ ] Update progress notes\n"
        result += "[ ] Plan tomorrow's priorities\n"
        result += "[ ] Clear workspace\n"
        
        result += "\n"
        result += "PRODUCTIVITY TIPS\n"
        result += "-" * 30 + "\n"
        result += "- Start with the most challenging task\n"
        result += "- Take regular short breaks (5-10 min)\n"
        result += "- Stay hydrated and take a proper lunch\n"
        result += "- Minimize distractions during focus blocks\n"
        result += "- Review progress at end of day\n"
        
        return result