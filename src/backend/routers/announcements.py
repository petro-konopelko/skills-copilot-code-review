"""
Announcements management endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId

from ..database import announcements_collection

router = APIRouter(
    prefix="/announcements",
    tags=["announcements"]
)


@router.get("/")
def get_announcements() -> List[Dict[str, Any]]:
    """Get all visible announcements for display"""
    announcements = list(announcements_collection.find({"visible": True}))
    
    for announcement in announcements:
        announcement["_id"] = str(announcement["_id"])
    
    return announcements


@router.get("/all")
def get_all_announcements() -> List[Dict[str, Any]]:
    """Get all announcements for admin management (signed-in users only)"""
    announcements = list(announcements_collection.find())
    
    for announcement in announcements:
        announcement["_id"] = str(announcement["_id"])
    
    return announcements


@router.post("/")
def create_announcement(
    title: str,
    message: str,
    expiration_date: str,
    start_date: Optional[str] = None,
    priority: str = "normal"
) -> Dict[str, Any]:
    """Create a new announcement (requires authentication)"""
    
    # Validate dates
    try:
        if start_date:
            datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if start_date and start_date >= expiration_date:
        raise HTTPException(status_code=400, detail="Start date must be before expiration date")
    
    announcement = {
        "title": title,
        "message": message,
        "start_date": start_date,
        "expiration_date": expiration_date,
        "priority": priority,
        "visible": True,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    result = announcements_collection.insert_one(announcement)
    announcement["_id"] = str(result.inserted_id)
    
    return announcement


@router.put("/{announcement_id}")
def update_announcement(
    announcement_id: str,
    title: str,
    message: str,
    expiration_date: str,
    start_date: Optional[str] = None,
    priority: str = "normal",
    visible: bool = True
) -> Dict[str, Any]:
    """Update an existing announcement (requires authentication)"""
    
    try:
        obj_id = ObjectId(announcement_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid announcement ID")
    
    # Validate dates
    try:
        if start_date:
            datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if start_date and start_date >= expiration_date:
        raise HTTPException(status_code=400, detail="Start date must be before expiration date")
    
    announcement = announcements_collection.find_one({"_id": obj_id})
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    update_data = {
        "title": title,
        "message": message,
        "start_date": start_date,
        "expiration_date": expiration_date,
        "priority": priority,
        "visible": visible
    }
    
    announcements_collection.update_one({"_id": obj_id}, {"$set": update_data})
    
    updated = announcements_collection.find_one({"_id": obj_id})
    updated["_id"] = str(updated["_id"])
    
    return updated


@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: str) -> Dict[str, str]:
    """Delete an announcement (requires authentication)"""
    
    try:
        obj_id = ObjectId(announcement_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid announcement ID")
    
    result = announcements_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    return {"message": "Announcement deleted successfully"}
