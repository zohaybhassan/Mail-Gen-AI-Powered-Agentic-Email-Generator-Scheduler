#!/usr/bin/env python
"""
Test script to verify email scheduling functionality.
Run this while the Flask app is running on localhost:5000.
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import time
import requests
import json


def test_remote_scheduler():
    """Test the scheduler via the running Flask app's API endpoints."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Email Scheduler Functionality")
    print("=" * 50)
    
    # 1. Test scheduler status
    print("\n📊 Checking scheduler status...")
    try:
        response = requests.get(f"{base_url}/debug/scheduler", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Scheduler running: {data['running']}")
            print(f"  📋 Total jobs: {data['jobs_count']}")
            print(f"  📧 Scheduled emails: {data['scheduled_emails_count']}")
        else:
            print(f"  ❌ Failed to get scheduler status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to Flask app. Is it running on localhost:5000?")
        return
    except Exception as e:
        print(f"  ❌ Error checking scheduler: {e}")
        return
    
    # 2. Test scheduler with a quick test job
    print("\n⏰ Testing scheduler with 10-second test job...")
    try:
        response = requests.get(f"{base_url}/test_scheduler", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Test job scheduled: {data['message']}")
            print(f"  ⏱️  Check Flask console output in ~10 seconds")
        else:
            print(f"  ❌ Failed to schedule test job: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error scheduling test: {e}")
    
    # 3. Check scheduled emails page
    print("\n📋 Checking scheduled emails page...")
    try:
        response = requests.get(f"{base_url}/scheduled_emails", timeout=5)
        if response.status_code == 200:
            print("  ✅ Scheduled emails page accessible")
        else:
            print(f"  ❌ Failed to access scheduled emails: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error accessing scheduled emails: {e}")
    
    print("\n" + "=" * 50)
    print("🔗 URLs for manual testing:")
    print(f"  Main App:        {base_url}")
    print(f"  Scheduled Emails: {base_url}/scheduled_emails")
    print(f"  Scheduler Debug:  {base_url}/debug/scheduler")
    print(f"  Test Scheduler:   {base_url}/test_scheduler")


def test_local_scheduler():
    """Test APScheduler locally without the Flask app."""
    print("\n🚀 Testing APScheduler locally...")
    
    results = {"executed": False}
    
    def test_function(message, test_id):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"  🎯 [{current_time}] Scheduled task executed: {message} (ID: {test_id})")
        results["executed"] = True
    
    scheduler = BackgroundScheduler()
    scheduler.start()
    print("  📅 Scheduler started")
    
    test_time = datetime.now() + timedelta(seconds=5)
    print(f"  ⏰ Scheduling test for: {test_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    job = scheduler.add_job(
        func=test_function,
        trigger=DateTrigger(run_date=test_time),
        args=["Test message", "test123"],
        id="test_job"
    )
    
    print(f"  ✅ Job scheduled with ID: {job.id}")
    print("  ⏳ Waiting 8 seconds for execution...")
    
    time.sleep(8)
    
    if results["executed"]:
        print("  ✅ LOCAL SCHEDULER TEST PASSED")
    else:
        print("  ❌ LOCAL SCHEDULER TEST FAILED - job did not execute")
    
    scheduler.shutdown()
    print("  🛑 Scheduler shutdown")


if __name__ == "__main__":
    print("=" * 50)
    print("  MailGen Scheduler Test Suite")
    print("=" * 50)
    
    # Always run the local test
    test_local_scheduler()
    
    # Try the remote test (Flask app may or may not be running)
    print("\n")
    test_remote_scheduler()

