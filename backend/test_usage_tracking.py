#!/usr/bin/env python3
"""
Test script for usage tracking system
"""

import asyncio
import sys
import os
import sqlite3
import json
from uuid import uuid4
from datetime import datetime, date, timedelta

# Simple test without complex imports
class SimpleUsageTest:
    def __init__(self):
        self.db_path = "../Vidalytics.db"

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_current_billing_period(self):
        today = date.today()
        period_start = today.replace(day=1)

        if today.month == 12:
            period_end = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            period_end = date(today.year, today.month + 1, 1) - timedelta(days=1)

        return {
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat()
        }

    def test_database_connection(self):
        """Test if we can connect to the database"""
        try:
            conn = self.get_connection()
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%usage%'")
            tables = cursor.fetchall()
            conn.close()
            return [table[0] for table in tables]
        except Exception as e:
            print(f"Database connection error: {e}")
            return None

    def test_usage_limits(self):
        """Test if usage limits are properly set"""
        try:
            conn = self.get_connection()
            cursor = conn.execute("SELECT plan_id, usage_type, limit_amount FROM usage_limits")
            limits = cursor.fetchall()
            conn.close()
            return limits
        except Exception as e:
            print(f"Usage limits error: {e}")
            return None

    def test_track_usage(self, user_id, usage_type, amount=1, cost=0.05):
        """Test tracking usage"""
        try:
            conn = self.get_connection()
            period = self.get_current_billing_period()

            # Insert usage record
            cursor = conn.execute(
                """
                INSERT INTO usage_tracking (
                    user_id, usage_type, amount, cost_estimate,
                    metadata, period_start, period_end
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (str(user_id), usage_type, amount, cost,
                 json.dumps({"test": True}), period['period_start'], period['period_end'])
            )

            usage_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return {"usage_id": usage_id, "success": True}
        except Exception as e:
            print(f"Track usage error: {e}")
            return {"success": False, "error": str(e)}

    def test_get_usage_summary(self, user_id):
        """Test getting usage summary"""
        try:
            conn = self.get_connection()
            period = self.get_current_billing_period()

            # Get usage for current period
            cursor = conn.execute(
                """
                SELECT usage_type, SUM(amount) as total_amount, SUM(cost_estimate) as total_cost
                FROM usage_tracking
                WHERE user_id = ? AND period_start = ? AND period_end = ?
                GROUP BY usage_type
                """,
                (str(user_id), period['period_start'], period['period_end'])
            )

            usage_data = cursor.fetchall()
            conn.close()

            return {
                "period": period,
                "usage": [{"type": row[0], "amount": row[1], "cost": row[2]} for row in usage_data]
            }
        except Exception as e:
            print(f"Get usage summary error: {e}")
            return {"error": str(e)}

def test_usage_tracking():
    """Test the usage tracking system"""
    print("🧪 Testing Usage Tracking System")
    print("=" * 50)

    # Create test instance
    test = SimpleUsageTest()

    # Test user ID
    test_user_id = uuid4()
    print(f"📝 Test User ID: {test_user_id}")

    try:
        # Test 1: Database connection
        print("\n1️⃣ Testing database connection...")
        tables = test.test_database_connection()
        if tables:
            print(f"✅ Connected! Found tables: {tables}")
        else:
            print("❌ Database connection failed")
            return

        # Test 2: Usage limits
        print("\n2️⃣ Testing usage limits...")
        limits = test.test_usage_limits()
        if limits:
            print(f"✅ Found {len(limits)} usage limits:")
            for limit in limits[:5]:  # Show first 5
                print(f"   - {limit[0]}: {limit[1]} = {limit[2]}")
        else:
            print("❌ No usage limits found")
            return

        # Test 3: Track usage
        print("\n3️⃣ Testing usage tracking...")
        result = test.test_track_usage(test_user_id, "ai_conversations", 5, 0.25)
        if result.get("success"):
            print(f"✅ Tracked usage: ID {result['usage_id']}")
        else:
            print(f"❌ Failed to track usage: {result.get('error')}")
            return

        # Test 4: Track more usage
        print("\n4️⃣ Testing multiple usage tracking...")
        for i in range(10):
            result = test.test_track_usage(test_user_id, "ai_conversations", 1, 0.05)
            if not result.get("success"):
                print(f"❌ Failed on iteration {i}: {result.get('error')}")
                break
        else:
            print("✅ Successfully tracked 10 more usage records")

        # Test 5: Get usage summary
        print("\n5️⃣ Testing usage summary...")
        summary = test.test_get_usage_summary(test_user_id)
        if "error" not in summary:
            print(f"✅ Usage summary:")
            print(f"   Period: {summary['period']['period_start']} to {summary['period']['period_end']}")
            for usage in summary['usage']:
                print(f"   - {usage['type']}: {usage['amount']} uses, ${usage['cost']:.4f} cost")
        else:
            print(f"❌ Failed to get summary: {summary['error']}")

        print("\n🎉 Basic tests completed successfully!")
        print("\n💡 Next steps:")
        print("   - Start the FastAPI server to test the full API")
        print("   - Test the frontend usage tracking panel")
        print("   - Verify limit enforcement in real usage")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_usage_tracking()
