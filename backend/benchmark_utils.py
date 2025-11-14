"""
Utility functions for AI maturity benchmarks
"""
import json
from pathlib import Path
from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorDatabase

async def seed_benchmarks(db: AsyncIOMotorDatabase):
    """
    Seed the database with benchmark data from JSON file.
    Only runs if benchmarks collection is empty.
    """
    # Check if benchmarks already exist
    count = await db.sector_benchmarks.count_documents({})
    if count > 0:
        print(f"Benchmarks already seeded ({count} records found)")
        return
    
    # Load benchmark data from JSON file
    json_path = Path(__file__).parent / "ai_maturity_benchmarks_v1_SYSTEM.json"
    
    with open(json_path, 'r') as f:
        benchmark_data = json.load(f)
    
    # Insert all benchmark records
    if benchmark_data:
        await db.sector_benchmarks.insert_many(benchmark_data)
        print(f"Successfully seeded {len(benchmark_data)} benchmark records")

async def get_sector_benchmarks(db: AsyncIOMotorDatabase, sector: str) -> Dict[str, float]:
    """
    Retrieve benchmarks for a specific sector.
    Returns a dictionary mapping domain names to benchmark scores (0-100%).
    
    Args:
        db: Database connection
        sector: Sector name (e.g., "Finance / Insurance")
    
    Returns:
        Dictionary with domain names as keys and benchmark scores as values
    """
    # Query benchmarks for the specified sector
    cursor = db.sector_benchmarks.find({"sector_type": sector})
    benchmarks = await cursor.to_list(length=None)
    
    if not benchmarks:
        return {}
    
    # Convert to dictionary format: {domain_name: score}
    result = {}
    for benchmark in benchmarks:
        domain_name = benchmark["domain_name"]
        score = benchmark["benchmark_mean_score"]
        result[domain_name] = score
    
    return result

async def get_all_sectors(db: AsyncIOMotorDatabase) -> List[str]:
    """
    Get a list of all available sectors in the benchmark data.
    
    Returns:
        List of unique sector names
    """
    sectors = await db.sector_benchmarks.distinct("sector_type")
    return sorted(sectors)
