from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# from moviepy.editor import VideoFileClip
import cv2
import numpy as np
from pathlib import Path
import asyncio
import aiofiles
import os
from typing import Optional
import logging
from datetime import datetime
from typing import Union
from ratelimit import limits, sleep_and_retry
import json
from typing import Dict, List
import shutil

# Import VideoProcessor from extract_frames
from claude_ocr_all import process_ocr
from extract_frames import VideoProcessor

app = FastAPI()

# Configure CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:8081",  # Expo web
        # "exp://35.2.11.129:8081",   # Expo development
        "*" # Testing only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Rate limiting decorator (15 requests per minute)
@sleep_and_retry
@limits(calls=15, period=60)
def rate_limit():
    pass

async def process_video(file_path: Path, fps: int = 1) -> dict:
    """Process video using VideoProcessor class"""
    try:
        # Initialize VideoProcessor with the saved video file
        processor = VideoProcessor(str(file_path))
        
        # Create output directory path
        frames_dir = PROCESSED_DIR / file_path.stem
        
        # Extract frames (returns list of saved frame paths)
        saved_frames = processor.extract_frames_every_second(str(frames_dir))
        
        # Process OCR and get the final schema
        # Run the synchronous process_ocr in a thread pool to not block
        final_schema = await asyncio.get_event_loop().run_in_executor(
            None, process_ocr, frames_dir
        )
        
        return {
            "frame_count": len(saved_frames),
            "ocr_results": final_schema
        }
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise

@app.post("/upload-video")
async def upload_video(
    video: UploadFile = File(...),
):
    """
    Upload a video file
    """
    rate_limit()
    try:
        if not video.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")

        # Save the uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = UPLOAD_DIR / f"{timestamp}_{video.filename}"

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await video.read(1024 * 1024):
                await out_file.write(content)

        # Process the video and extract frames
        result = await process_video(file_path)
        
        return {
            "message": "Video upload successful",
            "file_name": str(file_path.stem),
            "frame_count": result["frame_count"],
            "ocr_results": result["ocr_results"]
        }
    except Exception as e:
        logger.error(f"Error handling video upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
def get_root():
    return {"message" : "Hello World!"}

@app.get("/poll-data")
async def get_poll_data() -> Dict[str, Dict[str, dict]]:
    """
    Get all poll data from PollTickets directory.
    Returns a nested dictionary of {county: {township: data}}
    """
    try:
        poll_dir = Path("PollTickets")
        if not poll_dir.exists():
            raise HTTPException(status_code=404, detail="PollTickets directory not found")

        all_data = {}
        
        # Iterate through county directories
        for county_dir in poll_dir.iterdir():
            if county_dir.is_dir():
                county_name = county_dir.name
                all_data[county_name] = {}
                
                # Iterate through township JSON files
                for township_file in county_dir.glob("*.json"):
                    township_name = township_file.stem
                    async with aiofiles.open(township_file, 'r') as f:
                        content = await f.read()
                        all_data[county_name][township_name] = json.loads(content)
        return all_data

    except Exception as e:
        logger.error(f"Error reading poll data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/county/{county_name}/presidential-winner")
async def get_county_presidential_winner(county_name: str) -> Dict[str, Union[str, int, Dict[str, int]]]:
    """
    Get the winning party for presidential election in a specific county.
    Returns the winning party and vote totals for each party.
    """
    try:
        poll_dir = Path("PollTickets")
        county_dir = poll_dir / county_name
        
        if not county_dir.exists():
            raise HTTPException(status_code=404, detail=f"County {county_name} not found")

        # Dictionary to store party vote totals
        party_votes = {}
        
        # Process each township file in the county
        for township_file in county_dir.glob("*.json"):
            async with aiofiles.open(township_file, 'r') as f:
                content = await f.read()
                data = json.loads(content)
                
                # Find the relevant contests
                straight_party = None
                presidential = None
                
                for contest in data['results']['contests']:
                    if contest['title'] == 'Straight Party Ticket':
                        straight_party = contest
                    elif contest['title'] == 'Electors of President and Vice-President of the United States':
                        presidential = contest
                
                if straight_party and presidential:
                    # Map the party order from straight party to presidential candidates
                    party_order = [candidate['ticket'][0] for candidate in straight_party['candidates']]
                    
                    # Add votes to party totals
                    for i, candidate in enumerate(presidential['candidates']):
                        if i < len(party_order):  # Ensure we don't go out of bounds
                            party = party_order[i]
                            votes = int(candidate['votes'])
                            party_votes[party] = party_votes.get(party, 0) + votes

        if not party_votes:
            raise HTTPException(status_code=404, detail="No presidential election data found")

        # Find the winning party
        winning_party = max(party_votes.items(), key=lambda x: x[1])[0]
        
        return {
            "county": county_name,
            "winning_party": winning_party,
            "vote_totals": party_votes,
            "total_votes": sum(party_votes.values())
        }

    except Exception as e:
        logger.error(f"Error calculating presidential winner: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processed-results")
async def get_processed_results() -> Dict[str, dict]:
    """
    Retrieve OCR results from all processed subdirectories.
    Returns a dictionary of {directory_name: ocr_results}
    """
    try:
        if not PROCESSED_DIR.exists():
            raise HTTPException(status_code=404, detail="Processed directory not found")

        results = {}
        
        # Iterate through subdirectories in the processed directory
        for subdir in PROCESSED_DIR.iterdir():
            if subdir.is_dir():
                schema_file = subdir / "final_schema.json"
                if schema_file.exists():
                    async with aiofiles.open(schema_file, 'r') as f:
                        content = await f.read()
                        results[subdir.name] = json.loads(content)
        
        return results

    except Exception as e:
        logger.error(f"Error reading processed results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-processed-result/{directory_name}")
async def save_processed_result(directory_name: str, ocr_result: Dict) -> Dict[str, str]:
    """
    Save OCR results for a specific directory.
    
    Args:
        directory_name: Name of the directory to save results for
        ocr_result: Dictionary containing the OCR results
    
    Returns:
        Dictionary with success message
    """
    try:
        # Check if directory exists
        dir_path = PROCESSED_DIR / directory_name
        if not dir_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"Directory '{directory_name}' not found in processed directory"
            )
        
        # Save results to final_schema.json
        schema_file = dir_path / "final_schema.json"
        async with aiofiles.open(schema_file, 'w') as f:
            await f.write(json.dumps(ocr_result))
        
        return {"message": f"Successfully saved OCR results for {directory_name}"}

    except Exception as e:
        logger.error(f"Error saving processed results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/move-to-polltickets/{filename}/{county}/{township}")
async def move_to_polltickets(filename: str, county: str, township: str) -> Dict[str, str]:
    """
    Move processed OCR results to PollTickets directory structure.
    
    Args:
        filename: Name of the processed directory containing final_schema.json
        county: Name of the county directory to create/use
        township: Name of the township file (will add .json extension)
    
    Returns:
        Dictionary with success message
    """
    try:
        # Replace spaces with underscores in township name
        township = township.strip().replace(" ", "_")
        county = county.strip()

        # Construct paths
        source_file = PROCESSED_DIR / filename / "final_schema.json"
        poll_dir = Path("PollTickets")
        county_dir = poll_dir / county
        target_file = county_dir / f"{township}.json"

        # Check if source exists
        if not source_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Source file not found: {source_file}"
            )

        # Create county directory if it doesn't exist
        county_dir.mkdir(parents=True, exist_ok=True)

        # Check if target already exists and overwrite
        if target_file.exists():
            logger.info(f"Overwriting existing file: {target_file}")

        # Copy the file to new location
        async with aiofiles.open(source_file, 'r') as source:
            content = await source.read()
            async with aiofiles.open(target_file, 'w') as target:
                await target.write(content)

        return {
            "message": f"Successfully moved {filename}/final_schema.json to {county}/{township}.json"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moving processed results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

