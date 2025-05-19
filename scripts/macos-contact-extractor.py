#!/usr/bin/env python3
"""
Phase 1: macOS Contact Extraction & Import
Extracts contacts from macOS and imports them as "Raw Import" stage prospects.
"""

import os
import subprocess
import csv
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client
import re

load_dotenv()

class MacOSContactExtractor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        self.export_file = "data/macos_contacts_export.csv"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def extract_contacts_applescript(self):
        """Extract contacts using AppleScript."""
        applescript = '''
        tell application "Contacts"
            set allContacts to every person
            set contactData to {}
            
            repeat with aPerson in allContacts
                set firstName to first name of aPerson
                set lastName to last name of aPerson
                set orgName to organization of aPerson
                set jobTitle to job title of aPerson
                set emailList to emails of aPerson
                set phoneList to phones of aPerson
                set note to note of aPerson
                
                -- Get first email if available
                set emailAddr to ""
                if (count of emailList) > 0 then
                    set emailAddr to value of item 1 of emailList
                end if
                
                -- Get first phone if available
                set phoneNum to ""
                if (count of phoneList) > 0 then
                    set phoneNum to value of item 1 of phoneList
                end if
                
                -- Handle empty values
                if firstName is missing value then set firstName to ""
                if lastName is missing value then set lastName to ""
                if orgName is missing value then set orgName to ""
                if jobTitle is missing value then set jobTitle to ""
                if note is missing value then set note to ""
                
                -- Build contact record
                set contactRecord to firstName & "||" & lastName & "||" & orgName & "||" & jobTitle & "||" & emailAddr & "||" & phoneNum & "||" & note
                set end of contactData to contactRecord
            end repeat
            
            return contactData
        end tell
        '''
        
        try:
            print("🍎 Extracting contacts from macOS...")
            result = subprocess.run(['osascript', '-e', applescript], 
                                 capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ AppleScript error: {result.stderr}")
                return None
                
            return result.stdout.strip().split('\n')
            
        except Exception as e:
            print(f"❌ Error running AppleScript: {e}")
            return None
    
    def parse_contact_data(self, raw_data):
        """Parse the raw contact data into structured format."""
        contacts = []
        
        print(f"📊 Processing {len(raw_data)} contacts...")
        
        for line in raw_data:
            if not line.strip():
                continue
                
            # Split by our delimiter
            parts = line.split('||')
            if len(parts) >= 7:
                first_name = parts[0].strip()
                last_name = parts[1].strip()
                organization = parts[2].strip()
                job_title = parts[3].strip()
                email = parts[4].strip()
                phone = parts[5].strip()
                notes = parts[6].strip()
                
                # Build full name
                full_name = f"{first_name} {last_name}".strip()
                if not full_name:
                    # Use organization or email as fallback
                    full_name = organization or email or "Unknown Contact"
                
                # Skip contacts without email or organization
                if not email and not organization:
                    continue
                
                contact = {
                    'full_name': full_name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'organization': organization,
                    'job_title': job_title,
                    'email': email,
                    'phone': phone,
                    'notes': notes,
                    'source': 'macOS Contacts',
                    'processing_stage': 'Raw Import'
                }
                
                contacts.append(contact)
        
        return contacts
    
    def save_to_csv(self, contacts):
        """Save contacts to CSV for review/backup."""
        df = pd.DataFrame(contacts)
        df.to_csv(self.export_file, index=False)
        print(f"💾 Saved {len(contacts)} contacts to {self.export_file}")
        return df
    
    def analyze_contacts(self, contacts_df):
        """Analyze the contacts for insights."""
        print("\n📈 CONTACT ANALYSIS")
        print("=" * 50)
        
        total = len(contacts_df)
        with_email = len(contacts_df[contacts_df['email'] != ''])
        with_org = len(contacts_df[contacts_df['organization'] != ''])
        with_title = len(contacts_df[contacts_df['job_title'] != ''])
        
        print(f"Total contacts: {total}")
        print(f"With email: {with_email} ({with_email/total*100:.1f}%)")
        print(f"With organization: {with_org} ({with_org/total*100:.1f}%)")
        print(f"With job title: {with_title} ({with_title/total*100:.1f}%)")
        
        # Top organizations
        if with_org > 0:
            top_orgs = contacts_df[contacts_df['organization'] != '']['organization'].value_counts().head(10)
            print(f"\n🏢 Top Organizations:")
            for org, count in top_orgs.items():
                print(f"  {org}: {count}")
        
        # Email domains analysis
        if with_email > 0:
            domains = contacts_df[contacts_df['email'] != '']['email'].apply(
                lambda x: x.split('@')[-1] if '@' in x else 'invalid'
            ).value_counts().head(10)
            print(f"\n📧 Top Email Domains:")
            for domain, count in domains.items():
                print(f"  {domain}: {count}")
        
        return {
            'total': total,
            'with_email': with_email,
            'with_org': with_org,
            'with_title': with_title
        }
    
    def upload_to_notion(self, contacts, batch_size=10):
        """Upload contacts to Notion in batches."""
        print(f"\n🚀 Uploading {len(contacts)} contacts to Notion...")
        
        success_count = 0
        error_count = 0
        
        for i in range(0, len(contacts), batch_size):
            batch = contacts[i:i+batch_size]
            print(f"📦 Processing batch {i//batch_size + 1} ({len(batch)} contacts)...")
            
            for contact in batch:
                try:
                    # Build Notion properties
                    properties = {
                        "Name": {"title": [{"text": {"content": contact['full_name']}}]},
                        "Processing Stage": {"select": {"name": contact['processing_stage']}},
                        "Source": {"select": {"name": contact['source']}},
                        "Status": {"select": {"name": "New"}},
                        "Priority": {"select": {"name": "Low"}}
                    }
                    
                    # Add optional fields
                    if contact['organization']:
                        properties["Company"] = {"rich_text": [{"text": {"content": contact['organization']}}]}
                    
                    if contact['job_title']:
                        properties["Job Title"] = {"rich_text": [{"text": {"content": contact['job_title']}}]}
                    
                    if contact['email']:
                        properties["Email"] = {"email": contact['email']}
                    
                    if contact['phone']:
                        properties["Phone"] = {"phone_number": contact['phone']}
                    
                    if contact['notes']:
                        properties["Notes"] = {"rich_text": [{"text": {"content": contact['notes']}}]}
                    
                    # Create the page
                    self.notion.pages.create(
                        parent={"database_id": self.database_id},
                        properties=properties
                    )
                    
                    success_count += 1
                    
                except Exception as e:
                    print(f"  ❌ Error uploading {contact['full_name']}: {e}")
                    error_count += 1
        
        print(f"\n✅ Upload complete!")
        print(f"  Success: {success_count}")
        print(f"  Errors: {error_count}")
        
        return success_count, error_count
    
    def run_extraction(self):
        """Run the complete extraction process."""
        print("🔥 FUSION REACTOR: macOS Contact Extraction")
        print("=" * 50)
        
        # Step 1: Extract from macOS
        raw_data = self.extract_contacts_applescript()
        if not raw_data:
            print("❌ Failed to extract contacts")
            return
        
        # Step 2: Parse and clean
        contacts = self.parse_contact_data(raw_data)
        if not contacts:
            print("❌ No valid contacts found")
            return
        
        # Step 3: Save to CSV
        contacts_df = self.save_to_csv(contacts)
        
        # Step 4: Analyze
        stats = self.analyze_contacts(contacts_df)
        
        # Step 5: Confirm upload
        print(f"\n🎯 Ready to upload {len(contacts)} contacts to Notion?")
        response = input("Continue? (y/n): ").lower().strip()
        
        if response == 'y':
            success, errors = self.upload_to_notion(contacts)
            print(f"\n🎉 FUSION COMPLETE!")
            print(f"Raw material successfully injected into the pipeline!")
            print(f"✅ {success} contacts now in 'Raw Import' stage")
            if errors:
                print(f"⚠️  {errors} contacts had issues (check logs)")
        else:
            print("Upload cancelled. Contacts saved to CSV for review.")

if __name__ == "__main__":
    extractor = MacOSContactExtractor()
    extractor.run_extraction()