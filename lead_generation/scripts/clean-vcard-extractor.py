#!/usr/bin/env python3
"""
CLEAN vCard Extractor: Based on reconnaissance findings
Extracts Name + Company + Work Email from vCard file.
"""

import os
import re
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

class CleanVCardExtractor:
    def __init__(self, vcf_path="data/contacts_export.vcf"):
        self.vcf_path = vcf_path
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_PROSPECTS_DB_ID")
        
        os.makedirs("data", exist_ok=True)
    
    def parse_vcard_file(self):
        """Parse the entire vCard file."""
        print(f"📖 Parsing vCard file: {self.vcf_path}")
        
        if not os.path.exists(self.vcf_path):
            print(f"❌ vCard file not found: {self.vcf_path}")
            return None
        
        try:
            with open(self.vcf_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into individual vCards
            vcards = content.split('BEGIN:VCARD')[1:]  # Remove empty first element
            print(f"📊 Total vCards found: {len(vcards)}")
            
            contacts = []
            processed = 0
            valid_contacts = 0
            
            for i, vcard in enumerate(vcards):
                if i % 100 == 0:
                    print(f"   Processing: {i}/{len(vcards)} ({i/len(vcards)*100:.1f}%)")
                
                contact = self.parse_single_vcard(vcard)
                processed += 1
                
                # Only include contacts with email addresses
                if contact and contact.get('email'):
                    contacts.append(contact)
                    valid_contacts += 1
            
            print(f"✅ Processed: {processed} vCards")
            print(f"✅ Valid contacts with emails: {valid_contacts}")
            
            return contacts
            
        except Exception as e:
            print(f"❌ Error parsing vCard file: {e}")
            return None
    
    def parse_single_vcard(self, vcard_content):
        """Parse a single vCard into structured data."""
        lines = vcard_content.strip().split('\n')
        
        contact = {
            'name': '',
            'company': '',
            'job_title': '',
            'email': '',
            'email_type': '',
            'source': 'vCard Export',
            'processing_stage': 'Raw Import'
        }
        
        emails = []
        
        for line in lines:
            line = line.strip()
            
            # Full name
            if line.startswith('FN:'):
                contact['name'] = line[3:].strip()
            
            # Organization - clean up trailing semicolons
            elif line.startswith('ORG:'):
                org = line[4:].strip()
                contact['company'] = org.rstrip(';').strip()
            
            # Job title
            elif line.startswith('TITLE:'):
                contact['job_title'] = line[6:].strip()
            
            # Emails - collect all and prioritize later
            elif line.startswith('EMAIL') or line.startswith('item1.EMAIL'):
                email_data = self.parse_email_line(line)
                if email_data['value']:
                    emails.append(email_data)
        
        # Choose the best email
        if emails:
            # Priority: WORK > INTERNET > first email
            work_emails = [e for e in emails if 'WORK' in e['types']]
            internet_emails = [e for e in emails if 'INTERNET' in e['types']]
            
            if work_emails:
                best_email = work_emails[0]
            elif internet_emails:
                best_email = internet_emails[0]
            else:
                best_email = emails[0]
            
            contact['email'] = best_email['value']
            contact['email_type'] = ' + '.join(best_email['types'])
        
        # Clean and validate
        contact['name'] = contact['name'].strip()
        contact['company'] = contact['company'].strip()
        contact['email'] = contact['email'].strip()
        
        # Create display name if needed
        if not contact['name'] and contact['company']:
            contact['name'] = contact['company']
        elif not contact['name'] and contact['email']:
            contact['name'] = contact['email'].split('@')[0].replace('.', ' ').title()
        
        # Only return if we have name and email
        if contact['name'] and contact['email']:
            return contact
        
        return None
    
    def parse_email_line(self, line):
        """Parse an EMAIL line from vCard."""
        # Handle both EMAIL: and item1.EMAIL: formats
        if ':' not in line:
            return {'value': '', 'types': []}
        
        parts = line.split(':', 1)
        header = parts[0]  # EMAIL;type=WORK or item1.EMAIL;type=INTERNET
        email = parts[1]   # email@domain.com
        
        # Extract types
        types = []
        if ';' in header:
            type_parts = header.split(';')
            for part in type_parts:
                if part.startswith('type='):
                    type_value = part[5:].upper()
                    if type_value not in ['PREF']:  # Skip preference markers
                        types.append(type_value)
        
        return {
            'value': email.strip(),
            'types': types
        }
    
    def clean_and_deduplicate(self, contacts):
        """Clean and deduplicate contacts."""
        print(f"🧹 Cleaning and deduplicating {len(contacts)} contacts...")
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(contacts)
        
        # Remove duplicates based on email (case insensitive)
        df['email_lower'] = df['email'].str.lower()
        df_dedup = df.drop_duplicates(subset=['email_lower'])
        df_dedup = df_dedup.drop('email_lower', axis=1)
        
        # Remove invalid emails
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df_dedup = df_dedup[df_dedup['email'].str.match(email_pattern)]
        
        # Clean company names
        df_dedup['company'] = df_dedup['company'].str.replace(';', '').str.strip()
        
        print(f"✅ After cleaning: {len(df_dedup)} unique, valid contacts")
        print(f"   Removed {len(contacts) - len(df_dedup)} duplicates/invalid entries")
        
        return df_dedup.to_dict('records')
    
    def analyze_cleaned_contacts(self, contacts):
        """Analyze the cleaned contact data."""
        print(f"\n📈 CLEANED CONTACT ANALYSIS")
        print("=" * 40)
        
        total = len(contacts)
        with_company = len([c for c in contacts if c['company']])
        with_job_title = len([c for c in contacts if c['job_title']])
        
        print(f"Total contacts: {total}")
        print(f"With company: {with_company} ({with_company/total*100:.1f}%)")
        print(f"With job title: {with_job_title} ({with_job_title/total*100:.1f}%)")
        print(f"All have email: {total} (100%)")
        
        # Email type breakdown
        email_types = {}
        for contact in contacts:
            email_type = contact['email_type']
            email_types[email_type] = email_types.get(email_type, 0) + 1
        
        print(f"\nEmail types:")
        for email_type, count in sorted(email_types.items()):
            print(f"  {email_type}: {count}")
        
        # Domain analysis
        domains = {}
        for contact in contacts:
            domain = contact['email'].split('@')[-1].lower()
            domains[domain] = domains.get(domain, 0) + 1
        
        top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:15]
        print(f"\nTop email domains:")
        for domain, count in top_domains:
            print(f"  {domain}: {count}")
        
        # Company analysis
        if with_company > 0:
            companies = {}
            for contact in contacts:
                if contact['company']:
                    companies[contact['company']] = companies.get(contact['company'], 0) + 1
            
            top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"\nTop companies:")
            for company, count in top_companies:
                print(f"  {company}: {count}")
    
    def preview_contacts(self, contacts, num_preview=20):
        """Preview contacts before upload."""
        print(f"\n👀 CONTACT PREVIEW (First {num_preview}):")
        print("=" * 80)
        
        for i, contact in enumerate(contacts[:num_preview]):
            company_text = f" @ {contact['company']}" if contact['company'] else ""
            email_type_text = f" [{contact['email_type']}]" if contact['email_type'] else ""
            
            print(f"{i+1}. {contact['name']}{company_text}")
            print(f"   📧 {contact['email']}{email_type_text}")
            if contact['job_title']:
                print(f"   💼 {contact['job_title']}")
            print()
        
        if len(contacts) > num_preview:
            print(f"... and {len(contacts) - num_preview} more contacts")
    
    def save_contacts(self, contacts):
        """Save contacts to CSV with timestamp."""
        df = pd.DataFrame(contacts)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/vcard_clean_extract_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        print(f"💾 Saved to: {filename}")
        return filename
    
    def upload_to_notion(self, contacts, batch_size=5):
        """Upload contacts to Notion."""
        print(f"\n🚀 Uploading {len(contacts)} contacts to Notion...")
        
        success = 0
        errors = 0
        
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
                        "Source": {"select": {"name": "vCard Export"}},
                        "Status": {"select": {"name": "New"}},
                        "Priority": {"select": {"name": "Low"}}
                    }
                    
                    # Add optional fields
                    if contact['company']:
                        properties["Company"] = {"rich_text": [{"text": {"content": contact['company']}}]}
                    
                    if contact['job_title']:
                        properties["Job Title"] = {"rich_text": [{"text": {"content": contact['job_title']}}]}
                    
                    # Add metadata
                    metadata_parts = [f"vCard export: {datetime.now().strftime('%Y-%m-%d')}"]
                    if contact['email_type']:
                        metadata_parts.append(f"Email type: {contact['email_type']}")
                    
                    properties["Internal Notes"] = {
                        "rich_text": [{"text": {"content": " | ".join(metadata_parts)}}]
                    }
                    
                    self.notion.pages.create(
                        parent={"database_id": self.database_id},
                        properties=properties
                    )
                    
                    success += 1
                    
                except Exception as e:
                    errors += 1
                    if batch_num <= 5:  # Only log errors for first few batches
                        print(f"\n   ⚠️  Error with {contact['name']}: {e}")
            
            print(f"✅")
            
            # Rate limiting
            if batch_num % 10 == 0:
                print(f"   📊 Progress: {success} uploaded, {errors} errors")
                import time
                time.sleep(2)
        
        return success, errors
    
    def run_clean_extraction(self):
        """Run the complete clean extraction process."""
        print("🔥" * 20)
        print("🧹 CLEAN vCard EXTRACTION")
        print("🔥" * 20)
        print("Based on reconnaissance findings")
        print("")
        
        # Parse vCard file
        contacts = self.parse_vcard_file()
        if not contacts:
            print("❌ Failed to parse contacts")
            return
        
        # Clean and deduplicate
        clean_contacts = self.clean_and_deduplicate(contacts)
        
        # Analyze
        self.analyze_cleaned_contacts(clean_contacts)
        
        # Preview
        self.preview_contacts(clean_contacts)
        
        # Save
        filename = self.save_contacts(clean_contacts)
        
        # Upload decision
        print(f"\n🎯 Ready to upload {len(clean_contacts)} clean contacts to Notion?")
        print("   (No phantom contacts, properly extracted from vCard)")
        
        response = input("Proceed with upload? (yes/no): ").lower().strip()
        
        if response in ['yes', 'y']:
            success, errors = self.upload_to_notion(clean_contacts)
            
            print(f"\n🎉 CLEAN EXTRACTION COMPLETE!")
            print(f"✅ Successfully uploaded: {success}")
            print(f"❌ Errors: {errors}")
            print(f"💾 Backup saved: {filename}")
            print(f"\n🎯 Next: Build LinkedIn enrichment pipeline!")
            
        else:
            print(f"Upload cancelled. Data saved to: {filename}")

if __name__ == "__main__":
    print("🧹 CLEAN vCard EXTRACTION PROTOCOL")
    print("No phantoms, no ghosts, just clean contact data!")
    print("")
    
    extractor = CleanVCardExtractor()
    extractor.run_clean_extraction()