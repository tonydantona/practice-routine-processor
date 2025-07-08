#!/usr/bin/env python3
"""
Guitar Practice Routine Processor
Utility to process images or manual input into structured JSON for guitar practice routines.
"""

import json
import os
import argparse
import sys
from typing import List, Dict, Any
from PIL import Image
import pytesseract

class RoutineProcessor:
    def __init__(self, json_file: str = "practice_routines.json"):
        self.json_file = json_file
        self.valid_categories = ["daily", "one_day", "two_three_days", "one_week"]
        self.valid_states = ["not_completed", "completed", "in_progress"]
    
    def load_routines(self) -> List[Dict[str, Any]]:
        """Load existing routines from JSON file or return empty list if file doesn't exist."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {self.json_file} contains invalid JSON. Starting with empty list.")
                return []
        return []
    
    def save_routines(self, routines: List[Dict[str, Any]]) -> None:
        """Save routines to JSON file."""
        with open(self.json_file, 'w') as f:
            json.dump(routines, f, indent=2)
        print(f"Saved {len(routines)} routines to {self.json_file}")
    
    def add_routine(self, text: str, category: str, tags: List[str], state: str) -> None:
        """Add a new routine to the JSON file."""
        routines = self.load_routines()
        
        new_routine = {
            "text": text,
            "category": category,
            "tags": tags,
            "state": state
        }
        
        routines.append(new_routine)
        self.save_routines(routines)
        print(f"Added routine: {text}")
    
    def manual_entry(self) -> None:
        """Interactive manual entry of practice routines (continuous mode)."""
        print("\n=== Manual Routine Entry ===")
        print("Enter routines one by one. Type 'q' or 'quit' to exit, or press Ctrl+C to quit.")
        print("-" * 50)
        
        try:
            while True:
                # Get text
                text = input("\nEnter practice routine text (or 'q' to quit): ").strip()
                if text.lower() in ['q', 'quit']:
                    break
                if not text:
                    print("Error: Text cannot be empty. Try again or type 'q' to quit.")
                    continue
                
                # Get category
                print(f"Available categories: {', '.join(self.valid_categories)}")
                category = input("Select category: ").strip()
                if category.lower() in ['q', 'quit']:
                    break
                if category not in self.valid_categories:
                    print(f"Error: Invalid category. Must be one of: {', '.join(self.valid_categories)}")
                    continue
                
                # Get tags
                tags_input = input("Enter tags (comma-separated): ").strip()
                if tags_input.lower() in ['q', 'quit']:
                    break
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                
                # Get state
                print(f"Available states: {', '.join(self.valid_states)}")
                state = input("Select state (default: not_completed): ").strip()
                if state.lower() in ['q', 'quit']:
                    break
                if not state:
                    state = "not_completed"
                elif state not in self.valid_states:
                    print(f"Error: Invalid state. Must be one of: {', '.join(self.valid_states)}")
                    continue
                
                # Add the routine
                self.add_routine(text, category, tags, state)
                print("✓ Routine added successfully!")
                
        except KeyboardInterrupt:
            print("\n\nExiting manual entry mode...")
        
        print("Manual entry session completed.")
    
    def process_image(self, image_path: str) -> None:
        """Process an image to extract practice routines."""
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return
        
        try:
            # Extract text from image
            print(f"Processing image: {image_path}")
            image = Image.open(image_path)
            
            # Convert to RGB if needed (for better OCR)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Handle special formats like MPO by saving to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp:
                image.save(temp.name, 'PNG')
                extracted_text = pytesseract.image_to_string(temp.name)
                os.unlink(temp.name)  # Clean up temp file
            
            print(f"Extracted text from {image_path}:")
            print("-" * 50)
            print(extracted_text)
            print("-" * 50)
            
            # For now, let's do basic processing
            # TODO: Implement AI categorization
            lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
            
            routines = self.load_routines()
            added_count = 0
            
            for line in lines:
                if len(line) > 10:  # Basic filter for meaningful text
                    # Basic categorization (can be enhanced with AI)
                    category = self.categorize_text(line)
                    tags = self.extract_tags(line)
                    
                    new_routine = {
                        "text": line,
                        "category": category,
                        "tags": tags,
                        "state": "not_completed"
                    }
                    
                    routines.append(new_routine)
                    added_count += 1
                    print(f"Added routine: {line}")
            
            if added_count > 0:
                self.save_routines(routines)
                print(f"Successfully added {added_count} routines from image.")
            else:
                print("No meaningful text found in image.")
            
        except Exception as e:
            print(f"Error processing image: {e}")
            import traceback
            traceback.print_exc()
    
    def categorize_text(self, text: str) -> str:
        """Basic text categorization. Can be enhanced with AI."""
        text_lower = text.lower()
        
        # Simple keyword-based categorization
        if any(word in text_lower for word in ['daily', 'everyday', 'routine']):
            return "daily"
        elif any(word in text_lower for word in ['week', 'weekly']):
            return "one_week"
        elif any(word in text_lower for word in ['couple', 'few', 'two', 'three']):
            return "two_three_days"
        else:
            return "one_day"
    
    def extract_tags(self, text: str) -> List[str]:
        """Extract tags from text based on keywords."""
        text_lower = text.lower()
        tags = []
        
        # Common guitar practice keywords
        tag_keywords = {
            'scales': ['scale', 'scales', 'major', 'minor', 'pentatonic'],
            'chords': ['chord', 'chords', 'progression'],
            'technique': ['technique', 'picking', 'fingering', 'fretting'],
            'ear training': ['ear', 'listening', 'hearing'],
            'theory': ['theory', 'harmony', 'interval'],
            'improv': ['improv', 'improvise', 'improvisation', 'jam'],
            'rhythm': ['rhythm', 'timing', 'metronome'],
            'practice': ['practice', 'exercise', 'drill']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        return tags if tags else ['general']

def main():
    parser = argparse.ArgumentParser(description='Guitar Practice Routine Processor')
    parser.add_argument('--json-file', default='practice_routines.json', 
                       help='JSON file to store routines (default: practice_routines.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Manual entry command
    manual_parser = subparsers.add_parser('manual', help='Manual entry of practice routine')
    
    # Image processing command
    image_parser = subparsers.add_parser('image', help='Process image to extract routines')
    image_parser.add_argument('image_path', help='Path to the image file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    processor = RoutineProcessor(args.json_file)
    
    if args.command == 'manual':
        processor.manual_entry()
    elif args.command == 'image':
        processor.process_image(args.image_path)

if __name__ == "__main__":
    main()