#!/usr/bin/env python3
"""
FUSION REACTOR: Mass macOS Contact Extraction
Optimized based on guinea pig test results.
"""

import os
import subprocess
import csv
import pandas as pd
import re
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class FusionContactExtractor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        self.export_file = "data/macos_contacts_fusion_export.csv"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def extract_all_contacts(self):
        """Extract ALL contacts using optimized AppleScript."""
        
        # Guinea pig proven AppleScript (notes-free!)
        applescript = '''
        tell application "Contacts"
            set allContacts to every person
            set contactData to {}
            
            repeat with aPerson in allContacts
                -- Get basic properties (NO NOTES!)
                set firstName to first name of aPerson
                set lastName to last name of aPerson
                set fullName to name of aPerson
                set orgName to organization of aPerson
                set jobTitle to job title of aPerson
                
                -- Get emails with labels
                set emailList to emails of aPerson
                set emailData to ""
                repeat with emailItem in emailList
                    set emailData to emailData & (value of emailItem) & "|" & (label of emailItem) & ";"
                end repeat
                
                -- Get phones with labels
                set phoneList to phones of aPerson
                set phoneData to ""
                repeat with phoneItem in phoneList
                    set phoneData to phoneData & (value of phoneItem) & "|" & (label of phoneItem) & ";"
                end repeat
                
                -- Handle missing values
                if firstName is missing value then set firstName to ""
                if lastName is missing value then set lastName to ""
                if fullName is missing value then set fullName to ""
                if orgName is missing value then set orgName to ""
                if jobTitle is missing value then set jobTitle to ""
                
                -- Build contact record (using || as delimiter)
                set contactRecord to fullName & "||" & firstName & "||" & lastName & "||" & orgName & "||" & jobTitle & "||" & emailData & "||" & phoneData
                set end of contactData to contactRecord
            end repeat
            
            return contactData
        end tell
        '''
        
        try:
            print("🚀 FUSION EXTRACTION: Processing ALL macOS contacts...")
            print("   (This may take a moment depending on contact count)")
            
            result = subprocess.run(['osascript', '-e', applescript], 
                                   capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ AppleScript error: {result.stderr}")
                return None
                
            raw_data = result.stdout.strip().split('\n')
            print(f"✅ Extracted {len(raw_data)} contacts from macOS!")
            return raw_data
            
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            return None
    
    def parse_email_phone_labels(self, data_string):
        """Parse email/phone data with labels."""
        if not data_string:
            return []
        
        items = []
        parts = data_string.split(';')
        
        for part in parts:
            if '|' in part:
                value, label = part.split('|', 1)
                # Clean up the label (remove AppleScript formatting)
                clean_label = re.sub(r'_\$!<(.+?)>!\$_', r'\1', label)
                items.append({
                    'value': value.strip(),
                    'label': clean_label.strip()
                })
        
        return items
    
    def process_contacts(self, raw_data):
        """Process raw contact data into structured format."""
        contacts = []
        skipped_count = 0
        
        print(f"📊 Processing {len(raw_data)} raw contact records...")
        
        for line in raw_data:
            if not line.strip():
                continue
                
            parts = line.split('||')
            if len(parts) < 7:
                skipped_count += 1
                continue
            
            full_name = parts[0].strip()
            first_name = parts[1].strip()
            last_name = parts[2].strip()
            organization = parts[3].strip()
            job_title = parts[4].strip()
            email_data = parts[5].strip()
            phone_data = parts[6].strip()
            
            # Parse emails and phones
            emails = self.parse_email_phone_labels(email_data)
            phones = self.parse_email_phone_labels(phone_data)
            
            # Skip contacts with no useful data
            if not full_name and not organization and not emails:
                skipped_count += 1
                continue
            
            # Use first email and phone
            primary_email = emails[0]['value'] if emails else ""
            primary_phone = phones[0]['value'] if phones else ""
            
            # Build contact record
            contact = {
                'full_name': full_name or f"{first_name} {last_name}".strip() or organization or "Unknown Contact",
                'first_name': first_name,
                'last_name': last_name,
                'organization': organization,
                'job_title': job_title,
                'email': primary_email,
                'email_label': emails[0]['label'] if emails else "",
                'phone': primary_phone,
                'phone_label': phones[0]['label'] if phones else "",
                'total_emails': len(emails),
                'total_phones': len(phones),
                'source': 'macOS Contacts',
                'processing_stage': 'Raw Import',
                'extraction_date': datetime.now().isoformat()
            }
            
            contacts.append(contact)
        
        print(f"✅ Successfully processed {len(contacts)} contacts")
        print(f"⚠️  Skipped {skipped_count} incomplete records")
        
        return contacts
    
    def analyze_contacts(self, contacts):
        """Analyze extracted contacts for insights."""
        df = pd.DataFrame(contacts)
        
        print("\n" + "=" * 60)
        print("📈 FUSION EXTRACTION ANALYSIS")
        print("=" * 60)
        
        total = len(df)
        with_email = len(df[df['email'] != ''])
        with_org = len(df[df['organization'] != ''])
        with_title = len(df[df['job_title'] != ''])
        with_phone = len(df[df['phone'] != ''])
        
        print(f"📊 EXTRACTION STATS:")
        print(f"   Total contacts: {total}")
        print(f"   With email: {with_email} ({with_email/total*100:.1f}%)")
        print(f"   With organization: {with_org} ({with_org/total*100:.1f}%)")
        print(f"   With job title: {with_title} ({with_title/total*100:.1f}%)")
        print(f"   With phone: {with_phone} ({with_phone/total*100:.1f}%)")
        
        # Email label analysis
        if with_email > 0:
            email_labels = df[df['email_label'] != '']['email_label'].value_counts()
            print(f"\n📧 EMAIL TYPES:")
            for label, count in email_labels.head(5).items():
                print(f"   {label}: {count}")
        
        # Top organizations
        if with_org > 0:
            top_orgs = df[df['organization'] != '']['organization'].value_counts().head(10)
            print(f"\n🏢 TOP ORGANIZATIONS:")
            for org, count in top_orgs.items():
                print(f"   {org}: {count}")
        
        # Domain analysis
        if with_email > 0:
            domains = df[df['email'] != '']['email'].apply(
                lambda x: x.split('@')[-1] if '@' in x else 'invalid'
            ).value_counts().head(10)
            print(f"\n🌐 EMAIL DOMAINS:")
            for domain, count in domains.items():
                print(f"   {domain}: {count}")
        
        return df
    
    def save_contacts(self, contacts_df):
        """Save contacts to CSV with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/macos_fusion_extract_{timestamp}.csv"
        
        contacts_df.to_csv(filename, index=False)
        contacts_df.to_csv(self.export_file, index=False)  # Also save as latest
        
        print(f"💾 Contacts saved to: {filename}")
        print(f"💾 Latest copy: {self.export_file}")
    
    def upload_to_notion(self, contacts, batch_size=5):
        """Upload contacts to Notion in small batches."""
        print(f"\n🚀 FUSION UPLOAD: Sending {len(contacts)} contacts to Notion...")
        print(f"   (Processing in batches of {batch_size} to avoid rate limits)")
        
        success_count = 0
        error_count = 0
        errors = []
        
        for i in range(0, len(contacts), batch_size):
            batch = contacts[i:i+batch_size]
            batch_num = i//batch_size + 1
            total_batches = (len(contacts) + batch_size - 1) // batch_size
            
            print(f"📦 Batch {batch_num}/{total_batches} ({len(batch)} contacts)...", end=" ")
            
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
                    
                    # Add extraction metadata to notes
                    metadata = f"Extracted: {contact['extraction_date'][:10]}"
                    if contact['email_label']:
                        metadata += f" | Email: {contact['email_label']}"
                    if contact['total_emails'] > 1:
                        metadata += f" | {contact['total_emails']} emails"
                    if contact['total_phones'] > 1:
                        metadata += f" | {contact['total_phones']} phones"
                    
                    properties["Internal Notes"] = {"rich_text": [{"text": {"content": metadata}}]}
                    
                    # Create the page
                    self.notion.pages.create(
                        parent={"database_id": self.database_id},
                        properties=properties
                    )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"{contact['full_name']}: {str(e)}")
            
            print("✅")
        
        print(f"\n🎉 FUSION UPLOAD COMPLETE!")
        print(f"   ✅ Successfully uploaded: {success_count}")
        print(f"   ❌ Errors: {error_count}")
        
        if errors and len(errors) <= 10:
            print(f"\n⚠️  Error details:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors")
        
        return success_count, error_count
    
    def run_fusion_extraction(self):
        """Run the complete fusion extraction process."""
        print("🔥" * 20)
        print("🚀 FUSION REACTOR: MASS CONTACT EXTRACTION 🚀")
        print("🔥" * 20)
        print(f"Target: Notion Database {self.database_id}")
        print(f"Strategy: Extract → Process → Analyze → Upload")
        print("")
        
        # Step 1: Extract from macOS
        raw_data = self.extract_all_contacts()
        if not raw_data:
            print("❌ FUSION FAILED: Could not extract contacts")
            return
        
        # Step 2: Process the data
        contacts = self.process_contacts(raw_data)
        if not contacts:
            print("❌ FUSION FAILED: No valid contacts found")
            return
        
        # Step 3: Analyze the extraction
        contacts_df = self.analyze_contacts(contacts)
        
        # Step 4: Save to CSV
        self.save_contacts(contacts_df)
        
        # Step 5: Confirm upload
        print(f"\n" + "=" * 60)
        print(f"🎯 READY TO UPLOAD {len(contacts)} CONTACTS TO NOTION")
        print(f"   All contacts will be marked as 'Raw Import' stage")
        print(f"   This is irreversible (but safe - they're just marked as raw)")
        print("=" * 60)
        
        response = input("\n🚀 Proceed with fusion upload? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            success, errors = self.upload_to_notion(contacts)
            
            print(f"\n" + "🔥" * 20)
            print("🎉 FUSION REACTOR COMPLETE! 🎉")
            print("🔥" * 20)
            print(f"✅ {success} contacts successfully imported")
            print(f"💾 Data backed up to: {self.export_file}")
            if errors:
                print(f"⚠️  {errors} contacts had issues")
            print("\n🎯 Next steps:")
            print("1. Review 'Raw Import' contacts in Notion")
            print("2. Run LinkedIn enrichment pipeline")
            print("3. Apply AI scoring algorithm")
            print("4. Graduate contacts through processing stages")
            print("\n🚀 The lead generation machine is LIVE!")
        else:
            print("\n🛑 Upload cancelled. Contacts saved to CSV for review.")
            print(f"💾 File location: {self.export_file}")

if __name__ == "__main__":
    extractor = FusionContactExtractor()
    extractor.run_fusion_extraction()