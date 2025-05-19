#!/usr/bin/env python3
"""
MINIMAL FUSION REACTOR: Name + Company + Work Email Only
Sometimes less is more.
"""

import os
import subprocess
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class MinimalContactExtractor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        self.export_file = "data/minimal_contacts.csv"
        
        os.makedirs("data", exist_ok=True)
    
    def get_contact_count(self):
        """Quick contact count."""
        count_script = '''
        tell application "Contacts"
            return count of every person
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', count_script], 
                                   capture_output=True, text=True)
            return int(result.stdout.strip()) if result.returncode == 0 else None
        except:
            return None
    
    def extract_minimal_batch(self, start_index, batch_size):
        """Extract only the essentials: Name, Company, Work Email."""
        
        applescript = f'''
        tell application "Contacts"
            set allContacts to every person
            set startIdx to {start_index}
            set endIdx to {start_index + batch_size - 1}
            set totalCount to count of allContacts
            
            if endIdx > totalCount then set endIdx to totalCount
            
            set contactData to {{}}
            
            repeat with i from startIdx to endIdx
                set aPerson to item i of allContacts
                
                try
                    -- Get the basics
                    set fullName to name of aPerson
                    set orgName to organization of aPerson
                    
                    -- Find work email specifically
                    set emailList to emails of aPerson
                    set workEmail to ""
                    
                    repeat with emailItem in emailList
                        set emailLabel to label of emailItem
                        set emailValue to value of emailItem
                        
                        -- Look for work-related emails
                        if emailLabel contains "Work" or emailLabel contains "work" or emailLabel contains "WORK" then
                            set workEmail to emailValue
                            exit repeat
                        end if
                    end repeat
                    
                    -- If no work email found, use first email
                    if workEmail is "" and (count of emailList) > 0 then
                        set workEmail to value of item 1 of emailList
                    end if
                    
                    -- Handle missing values
                    if fullName is missing value then set fullName to ""
                    if orgName is missing value then set orgName to ""
                    if workEmail is missing value then set workEmail to ""
                    
                    -- Only include contacts with either name+email or company+email
                    if (fullName is not "" and workEmail is not "") or (orgName is not "" and workEmail is not "") then
                        set contactRecord to fullName & "||" & orgName & "||" & workEmail
                        set end of contactData to contactRecord
                    end if
                    
                on error
                    -- Skip problematic contacts silently
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
            
            # Split and filter empty lines
            contacts = [line for line in result.stdout.strip().split('\n') if line.strip()]
            return contacts, None
            
        except Exception as e:
            return None, str(e)
    
    def run_minimal_extraction(self, batch_size=50):
        """Extract with minimal complexity."""
        print("🔥 MINIMAL FUSION REACTOR: Name + Company + Email")
        print("=" * 55)
        
        # Get total count
        total_contacts = self.get_contact_count()
        if not total_contacts:
            print("❌ Cannot count contacts")
            return
        
        print(f"📊 Total contacts in macOS: {total_contacts}")
        
        # Calculate batches
        total_batches = (total_contacts + batch_size - 1) // batch_size
        print(f"📦 Processing in {total_batches} batches")
        print("")
        
        all_contacts = []
        
        # Extract in batches
        for batch_num in range(total_batches):
            start_index = batch_num * batch_size + 1
            
            print(f"📦 Batch {batch_num + 1}/{total_batches}...", end=" ")
            
            batch_data, error = self.extract_minimal_batch(start_index, batch_size)
            
            if error:
                print(f"❌ Error: {error}")
                continue
            
            if batch_data:
                all_contacts.extend(batch_data)
                print(f"✅ +{len(batch_data)} contacts")
            else:
                print("✅ No valid contacts")
            
            time.sleep(0.2)  # Brief pause
        
        print(f"\n✅ Extraction complete: {len(all_contacts)} valid contacts")
        
        # Process the data
        processed_contacts = self.process_minimal_contacts(all_contacts)
        
        # Analysis
        self.analyze_minimal_data(processed_contacts)
        
        # Save and upload
        self.save_and_upload_minimal(processed_contacts)
    
    def process_minimal_contacts(self, raw_contacts):
        """Process the minimal contact data."""
        contacts = []
        
        for line in raw_contacts:
            parts = line.split('||')
            if len(parts) >= 3:
                name = parts[0].strip()
                company = parts[1].strip()
                email = parts[2].strip()
                
                # Build display name
                display_name = name if name else (company if company else email.split('@')[0])
                
                contact = {
                    'name': display_name,
                    'company': company,
                    'email': email,
                    'source': 'macOS Contacts',
                    'processing_stage': 'Raw Import',
                    'extracted_at': datetime.now().isoformat()
                }
                
                contacts.append(contact)
        
        return contacts
    
    def analyze_minimal_data(self, contacts):
        """Quick analysis of minimal data."""
        print("\n📈 MINIMAL DATA ANALYSIS")
        print("=" * 30)
        
        total = len(contacts)
        with_company = len([c for c in contacts if c['company']])
        with_name = len([c for c in contacts if c['name'] and c['name'] != c['email'].split('@')[0]])
        
        print(f"Total valid contacts: {total}")
        print(f"With company: {with_company} ({with_company/total*100:.1f}%)")
        print(f"With full name: {with_name} ({with_name/total*100:.1f}%)")
        print(f"All have email: {total} (100%)")
        
        # Top domains
        domains = {}
        for contact in contacts:
            domain = contact['email'].split('@')[-1]
            domains[domain] = domains.get(domain, 0) + 1
        
        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\nTop email domains:")
        for domain, count in top_domains:
            print(f"  {domain}: {count}")
        
        # Top companies
        companies = {}
        for contact in contacts:
            if contact['company']:
                companies[contact['company']] = companies.get(contact['company'], 0) + 1
        
        if companies:
            top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"\nTop companies:")
            for company, count in top_companies:
                print(f"  {company}: {count}")
    
    def preview_minimal_contacts(self, contacts, num_preview=15):
        """Show preview of minimal contacts."""
        print(f"\n👀 CONTACT PREVIEW (First {num_preview}):")
        print("=" * 60)
        
        for i, contact in enumerate(contacts[:num_preview]):
            company_text = f" @ {contact['company']}" if contact['company'] else ""
            print(f"{i+1}. {contact['name']}{company_text}")
            print(f"   📧 {contact['email']}")
            if i < num_preview - 1:
                print()
        
        if len(contacts) > num_preview:
            print(f"\n... and {len(contacts) - num_preview} more contacts")
    
    def save_and_upload_minimal(self, contacts):
        """Save minimal contacts and upload to Notion."""
        # Save to CSV
        df = pd.DataFrame(contacts)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/minimal_extract_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        df.to_csv(self.export_file, index=False)
        
        print(f"\n💾 Saved to: {filename}")
        
        # Preview
        self.preview_minimal_contacts(contacts)
        
        # Upload decision
        print(f"\n🎯 Upload {len(contacts)} contacts to Notion?")
        print("   (They'll be marked as 'Raw Import' stage)")
        
        response = input("Proceed? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            self.upload_minimal_to_notion(contacts)
        else:
            print("Upload cancelled. Data saved for review.")
    
    def upload_minimal_to_notion(self, contacts):
        """Upload minimal contacts to Notion."""
        print(f"\n🚀 Uploading {len(contacts)} contacts to Notion...")
        
        success = 0
        errors = 0
        batch_size = 5
        
        for i in range(0, len(contacts), batch_size):
            batch = contacts[i:i+batch_size]
            batch_num = i//batch_size + 1
            total_batches = (len(contacts) + batch_size - 1) // batch_size
            
            print(f"📦 Batch {batch_num}/{total_batches}...", end=" ")
            
            for contact in batch:
                try:
                    properties = {
                        "Name": {"title": [{"text": {"content": contact['name']}}]},
                        "Email": {"email": contact['email']},
                        "Processing Stage": {"select": {"name": "Raw Import"}},
                        "Source": {"select": {"name": "macOS Contacts"}},
                        "Status": {"select": {"name": "New"}},
                        "Priority": {"select": {"name": "Low"}}
                    }
                    
                    # Add company if available
                    if contact['company']:
                        properties["Company"] = {"rich_text": [{"text": {"content": contact['company']}}]}
                    
                    # Add extraction metadata
                    properties["Internal Notes"] = {
                        "rich_text": [{"text": {"content": f"Minimal extraction: {contact['extracted_at'][:10]}"}}]
                    }
                    
                    self.notion.pages.create(
                        parent={"database_id": self.database_id},
                        properties=properties
                    )
                    
                    success += 1
                    
                except Exception as e:
                    errors += 1
            
            print(f"✅")
            time.sleep(1)
        
        print(f"\n🎉 MINIMAL EXTRACTION COMPLETE!")
        print(f"✅ Success: {success}")
        print(f"❌ Errors: {errors}")
        print(f"\n🎯 Next: Build enrichment pipeline for these raw prospects!")

if __name__ == "__main__":
    print("🔥 MINIMAL FUSION REACTOR")
    print("Extracting only: Name + Company + Email")
    print("")
    
    extractor = MinimalContactExtractor()
    extractor.run_minimal_extraction(batch_size=50)