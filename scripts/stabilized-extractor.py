#!/usr/bin/env python3
"""
STABILIZED FUSION REACTOR: Progressive Contact Extraction
With monitoring, progress indicators, and chunked processing.
"""

import os
import subprocess
import csv
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class StabilizedContactExtractor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        self.export_file = "data/macos_contacts_progressive.csv"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def get_contact_count(self):
        """Get total number of contacts first."""
        count_script = '''
        tell application "Contacts"
            return count of every person
        end tell
        '''
        
        try:
            print("🔍 Counting contacts in macOS...")
            result = subprocess.run(['osascript', '-e', count_script], 
                                   capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Count error: {result.stderr}")
                return None
            
            count = int(result.stdout.strip())
            print(f"📊 Found {count} total contacts")
            return count
            
        except Exception as e:
            print(f"❌ Error counting contacts: {e}")
            return None
    
    def extract_contacts_batch(self, start_index, batch_size):
        """Extract a batch of contacts with progress."""
        # Progressive extraction script
        applescript = f'''
        tell application "Contacts"
            set allContacts to every person
            set totalCount to count of allContacts
            set startIdx to {start_index}
            set endIdx to {start_index + batch_size - 1}
            
            -- Ensure we don't go past the end
            if endIdx > totalCount then set endIdx to totalCount
            
            set contactData to {{}}
            
            repeat with i from startIdx to endIdx
                set aPerson to item i of allContacts
                
                try
                    -- Get basic properties (NO NOTES!)
                    set firstName to first name of aPerson
                    set lastName to last name of aPerson
                    set fullName to name of aPerson
                    set orgName to organization of aPerson
                    set jobTitle to job title of aPerson
                    
                    -- Get first email only (faster)
                    set emailList to emails of aPerson
                    set primaryEmail to ""
                    set emailLabel to ""
                    if (count of emailList) > 0 then
                        set primaryEmail to value of item 1 of emailList
                        set emailLabel to label of item 1 of emailList
                    end if
                    
                    -- Get first phone only (faster)
                    set phoneList to phones of aPerson
                    set primaryPhone to ""
                    set phoneLabel to ""
                    if (count of phoneList) > 0 then
                        set primaryPhone to value of item 1 of phoneList
                        set phoneLabel to label of item 1 of phoneList
                    end if
                    
                    -- Handle missing values
                    if firstName is missing value then set firstName to ""
                    if lastName is missing value then set lastName to ""
                    if fullName is missing value then set fullName to ""
                    if orgName is missing value then set orgName to ""
                    if jobTitle is missing value then set jobTitle to ""
                    if emailLabel is missing value then set emailLabel to ""
                    if phoneLabel is missing value then set phoneLabel to ""
                    
                    -- Build contact record
                    set contactRecord to fullName & "||" & firstName & "||" & lastName & "||" & orgName & "||" & jobTitle & "||" & primaryEmail & "||" & emailLabel & "||" & primaryPhone & "||" & phoneLabel
                    set end of contactData to contactRecord
                    
                on error errorMessage
                    -- Skip problematic contacts
                    set contactRecord to "ERROR||" & errorMessage & "||||||||||||"
                    set end of contactData to contactRecord
                end try
            end repeat
            
            return contactData
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                   capture_output=True, text=True)
            
            if result.returncode != 0:
                return None, result.stderr
                
            return result.stdout.strip().split('\n'), None
            
        except Exception as e:
            return None, str(e)
    
    def extract_all_contacts_progressive(self, batch_size=50):
        """Extract all contacts in progressive batches."""
        print("\n🚀 PROGRESSIVE EXTRACTION PROTOCOL")
        print("=" * 50)
        
        # Step 1: Get total count
        total_contacts = self.get_contact_count()
        if not total_contacts:
            return None
        
        # Step 2: Calculate batches
        total_batches = (total_contacts + batch_size - 1) // batch_size
        print(f"📦 Processing in {total_batches} batches of {batch_size} contacts each")
        print("")
        
        all_contacts = []
        error_count = 0
        
        # Step 3: Process each batch
        for batch_num in range(total_batches):
            start_index = batch_num * batch_size + 1  # AppleScript is 1-indexed
            end_index = min(start_index + batch_size - 1, total_contacts)
            
            print(f"📦 Batch {batch_num + 1}/{total_batches}: Contacts {start_index}-{end_index}...", end=" ")
            
            # Extract batch with timeout
            start_time = time.time()
            batch_data, error = self.extract_contacts_batch(start_index, batch_size)
            elapsed = time.time() - start_time
            
            if error:
                print(f"❌ Failed ({elapsed:.1f}s): {error}")
                error_count += 1
                if error_count > 3:
                    print("\n🚨 Too many batch failures. Stopping extraction.")
                    break
                continue
            
            if batch_data:
                # Filter out error records
                valid_contacts = [c for c in batch_data if not c.startswith("ERROR||")]
                error_records = [c for c in batch_data if c.startswith("ERROR||")]
                
                all_contacts.extend(valid_contacts)
                print(f"✅ {len(valid_contacts)} contacts ({elapsed:.1f}s)")
                
                if error_records:
                    print(f"   ⚠️  {len(error_records)} contacts had errors")
            else:
                print(f"❌ No data returned ({elapsed:.1f}s)")
            
            # Brief pause to avoid overwhelming the system
            time.sleep(0.5)
        
        print(f"\n✅ EXTRACTION COMPLETE: {len(all_contacts)} contacts extracted")
        return all_contacts
    
    def clean_label(self, label):
        """Clean up AppleScript label formatting."""
        if not label:
            return ""
        # Remove AppleScript formatting
        import re
        clean = re.sub(r'_\$!<(.+?)>!\$_', r'\1', label)
        return clean.strip()
    
    def process_extracted_contacts(self, raw_contacts):
        """Process the extracted contact data."""
        print(f"\n📊 PROCESSING {len(raw_contacts)} EXTRACTED CONTACTS")
        print("=" * 50)
        
        contacts = []
        skipped_count = 0
        
        for line in raw_contacts:
            if not line.strip():
                continue
                
            parts = line.split('||')
            if len(parts) < 9:
                skipped_count += 1
                continue
            
            full_name = parts[0].strip()
            first_name = parts[1].strip()
            last_name = parts[2].strip()
            organization = parts[3].strip()
            job_title = parts[4].strip()
            email = parts[5].strip()
            email_label = self.clean_label(parts[6].strip())
            phone = parts[7].strip()
            phone_label = self.clean_label(parts[8].strip())
            
            # Skip empty contacts
            if not full_name and not organization and not email:
                skipped_count += 1
                continue
            
            # Build contact
            contact = {
                'full_name': full_name or f"{first_name} {last_name}".strip() or organization or "Unknown Contact",
                'first_name': first_name,
                'last_name': last_name,
                'organization': organization,
                'job_title': job_title,
                'email': email,
                'email_label': email_label,
                'phone': phone,
                'phone_label': phone_label,
                'source': 'macOS Contacts',
                'processing_stage': 'Raw Import',
                'extraction_date': datetime.now().isoformat()
            }
            
            contacts.append(contact)
        
        print(f"✅ Processed: {len(contacts)} valid contacts")
        print(f"⚠️  Skipped: {skipped_count} incomplete records")
        
        return contacts
    
    def preview_contacts(self, contacts, num_preview=10):
        """Show a preview of contacts before upload."""
        print(f"\n👀 CONTACT PREVIEW (First {num_preview}):")
        print("=" * 80)
        
        for i, contact in enumerate(contacts[:num_preview]):
            print(f"\n{i+1}. {contact['full_name']}")
            print(f"   Company: {contact['organization'] or 'N/A'}")
            print(f"   Title: {contact['job_title'] or 'N/A'}")
            print(f"   Email: {contact['email'] or 'N/A'} ({contact['email_label'] or 'N/A'})")
            print(f"   Phone: {contact['phone'] or 'N/A'} ({contact['phone_label'] or 'N/A'})")
        
        if len(contacts) > num_preview:
            print(f"\n... and {len(contacts) - num_preview} more contacts")
    
    def quick_analysis(self, contacts):
        """Quick analysis of extracted contacts."""
        df = pd.DataFrame(contacts)
        
        print(f"\n📈 QUICK ANALYSIS")
        print("=" * 30)
        
        total = len(df)
        with_email = len(df[df['email'] != ''])
        with_org = len(df[df['organization'] != ''])
        with_phone = len(df[df['phone'] != ''])
        
        print(f"Total: {total}")
        print(f"With email: {with_email} ({with_email/total*100:.1f}%)")
        print(f"With company: {with_org} ({with_org/total*100:.1f}%)")
        print(f"With phone: {with_phone} ({with_phone/total*100:.1f}%)")
        
        # Top email labels
        email_labels = df[df['email_label'] != '']['email_label'].value_counts()
        if len(email_labels) > 0:
            print(f"\nEmail types: {dict(email_labels.head(3))}")
        
        return df
    
    def save_and_upload(self, contacts_df):
        """Save to CSV and offer upload to Notion."""
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/macos_progressive_{timestamp}.csv"
        contacts_df.to_csv(filename, index=False)
        contacts_df.to_csv(self.export_file, index=False)
        
        print(f"\n💾 Saved to: {filename}")
        
        # Offer upload
        print(f"\n🎯 Ready to upload {len(contacts_df)} contacts to Notion?")
        print("   All will be marked as 'Raw Import' processing stage")
        
        response = input("Proceed with upload? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            return self.upload_to_notion(contacts_df.to_dict('records'))
        else:
            print("Upload cancelled. Contacts saved for later review.")
            return 0, 0
    
    def upload_to_notion(self, contacts, batch_size=3):
        """Upload to Notion with progress monitoring."""
        print(f"\n🚀 UPLOADING TO NOTION")
        print("=" * 30)
        
        total_batches = (len(contacts) + batch_size - 1) // batch_size
        success_count = 0
        error_count = 0
        
        for i in range(0, len(contacts), batch_size):
            batch = contacts[i:i+batch_size]
            batch_num = i//batch_size + 1
            
            print(f"📦 Batch {batch_num}/{total_batches}...", end=" ")
            
            for contact in batch:
                try:
                    properties = {
                        "Name": {"title": [{"text": {"content": contact['full_name']}}]},
                        "Processing Stage": {"select": {"name": "Raw Import"}},
                        "Source": {"select": {"name": "macOS Contacts"}},
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
                    
                    # Metadata
                    metadata = f"Extracted: {contact['extraction_date'][:10]}"
                    if contact['email_label']:
                        metadata += f" | Email: {contact['email_label']}"
                    if contact['phone_label']:
                        metadata += f" | Phone: {contact['phone_label']}"
                    
                    properties["Internal Notes"] = {"rich_text": [{"text": {"content": metadata}}]}
                    
                    self.notion.pages.create(
                        parent={"database_id": self.database_id},
                        properties=properties
                    )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
            
            print(f"✅ ({success_count} total)")
            time.sleep(1)  # Rate limiting
        
        return success_count, error_count
    
    def run_stabilized_extraction(self, batch_size=50):
        """Run the stabilized extraction process."""
        print("🔥" * 20)
        print("🛡️  STABILIZED FUSION REACTOR 🛡️")
        print("🔥" * 20)
        print("Progressive extraction with monitoring")
        print("")
        
        # Extract with progress
        raw_contacts = self.extract_all_contacts_progressive(batch_size)
        if not raw_contacts:
            print("❌ Extraction failed")
            return
        
        # Process
        contacts = self.process_extracted_contacts(raw_contacts)
        if not contacts:
            print("❌ No valid contacts found")
            return
        
        # Quick analysis
        contacts_df = self.quick_analysis(contacts)
        
        # Preview
        self.preview_contacts(contacts)
        
        # Save and upload
        success, errors = self.save_and_upload(contacts_df)
        
        if success > 0:
            print(f"\n🎉 MISSION COMPLETE!")
            print(f"✅ {success} contacts uploaded to Notion")
            print(f"❌ {errors} errors (if any)")

if __name__ == "__main__":
    extractor = StabilizedContactExtractor()
    
    # Ask for batch size preference
    print("🔧 FUSION REACTOR CONFIGURATION")
    print("Batch size affects speed vs stability:")
    print("  Small (25): Slower but very stable")
    print("  Medium (50): Balanced (recommended)")
    print("  Large (100): Faster but might timeout")
    
    batch_input = input("\nChoose batch size (25/50/100) or press Enter for 50: ").strip()
    
    if batch_input == "25":
        batch_size = 25
    elif batch_input == "100":
        batch_size = 100
    else:
        batch_size = 50
    
    print(f"🚀 Starting extraction with batch size: {batch_size}")
    extractor.run_stabilized_extraction(batch_size)