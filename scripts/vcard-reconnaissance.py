#!/usr/bin/env python3
"""
vCard Reconnaissance Tool: Peek into the first contacts + Guinea Pig
Let's see what the vCard export actually contains.
"""

import os
import re
from datetime import datetime

class VCardReconnaissance:
    def __init__(self, vcf_path="data/contacts_export.vcf"):
        self.vcf_path = vcf_path
        self.contacts = []
    
    def check_file_exists(self):
        """Check if vCard file exists."""
        if not os.path.exists(self.vcf_path):
            print(f"❌ vCard file not found: {self.vcf_path}")
            print("\n📤 INSTRUCTIONS:")
            print("1. Open macOS Contacts")
            print("2. Select ALL (Cmd+A)")
            print("3. File → Export → Export vCard...")
            print("4. Save as: data/contacts_export.vcf")
            return False
        
        # Check file size
        size_mb = os.path.getsize(self.vcf_path) / (1024 * 1024)
        print(f"✅ Found vCard file: {size_mb:.1f}MB")
        return True
    
    def parse_single_vcard(self, vcard_lines):
        """Parse a single vCard entry."""
        contact = {
            'raw_lines': vcard_lines,
            'fields': {}
        }
        
        for line in vcard_lines:
            line = line.strip()
            
            # Full name
            if line.startswith('FN:'):
                contact['fields']['full_name'] = line[3:].strip()
            
            # Organization
            elif line.startswith('ORG:'):
                contact['fields']['organization'] = line[4:].strip()
            
            # Job title
            elif line.startswith('TITLE:'):
                contact['fields']['job_title'] = line[6:].strip()
            
            # Emails (can be multiple)
            elif line.startswith('EMAIL'):
                email_data = self.parse_email_line(line)
                if 'emails' not in contact['fields']:
                    contact['fields']['emails'] = []
                contact['fields']['emails'].append(email_data)
            
            # Phone numbers (can be multiple)
            elif line.startswith('TEL'):
                phone_data = self.parse_phone_line(line)
                if 'phones' not in contact['fields']:
                    contact['fields']['phones'] = []
                contact['fields']['phones'].append(phone_data)
            
            # Notes
            elif line.startswith('NOTE:'):
                contact['fields']['note'] = line[5:].strip()
        
        return contact
    
    def parse_email_line(self, line):
        """Parse an EMAIL line from vCard."""
        # EMAIL;type=WORK:email@domain.com
        # EMAIL;type=HOME;type=pref:email@domain.com
        parts = line.split(':', 1)
        if len(parts) < 2:
            return {'value': '', 'types': []}
        
        header = parts[0]  # EMAIL;type=WORK
        email = parts[1]   # email@domain.com
        
        # Extract types
        types = []
        if 'type=' in header:
            type_parts = header.split(';')
            for part in type_parts:
                if part.startswith('type='):
                    types.append(part[5:].upper())
        
        return {
            'value': email.strip(),
            'types': types,
            'raw_line': line
        }
    
    def parse_phone_line(self, line):
        """Parse a TEL line from vCard."""
        # TEL;type=WORK:+1-234-567-8900
        parts = line.split(':', 1)
        if len(parts) < 2:
            return {'value': '', 'types': []}
        
        header = parts[0]  # TEL;type=WORK
        phone = parts[1]   # +1-234-567-8900
        
        # Extract types
        types = []
        if 'type=' in header:
            type_parts = header.split(';')
            for part in type_parts:
                if part.startswith('type='):
                    types.append(part[5:].upper())
        
        return {
            'value': phone.strip(),
            'types': types,
            'raw_line': line
        }
    
    def extract_first_contacts(self, num_contacts=12):
        """Extract the first N contacts from vCard file."""
        print(f"🔍 Extracting first {num_contacts} contacts...")
        
        try:
            with open(self.vcf_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into individual vCards
            vcards = content.split('BEGIN:VCARD')[1:]  # Remove empty first element
            
            print(f"📊 Total vCards found: {len(vcards)}")
            
            # Parse first N contacts
            for i in range(min(num_contacts, len(vcards))):
                vcard_lines = ['BEGIN:VCARD'] + vcards[i].split('\n')
                contact = self.parse_single_vcard(vcard_lines)
                contact['index'] = i + 1
                self.contacts.append(contact)
            
            print(f"✅ Parsed first {len(self.contacts)} contacts")
            
        except Exception as e:
            print(f"❌ Error reading vCard file: {e}")
    
    def find_guinea_pig(self):
        """Search for Guinea Pig in the vCard file."""
        print("\n🐹 Searching for Guine Pig...")
        
        try:
            with open(self.vcf_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Search for Guinea Pig
            vcards = content.split('BEGIN:VCARD')[1:]
            
            for i, vcard in enumerate(vcards):
                if 'guine' in vcard.lower() or 'pig' in vcard.lower():
                    vcard_lines = ['BEGIN:VCARD'] + vcard.split('\n')
                    guinea_pig = self.parse_single_vcard(vcard_lines)
                    guinea_pig['index'] = i + 1
                    guinea_pig['is_guinea_pig'] = True
                    self.contacts.append(guinea_pig)
                    print(f"✅ Found Guinea Pig at position {i + 1}")
                    return
            
            print("❌ Guinea Pig not found in vCard export")
            
        except Exception as e:
            print(f"❌ Error searching for Guinea Pig: {e}")
    
    def display_contact_analysis(self, contact, contact_num):
        """Display detailed analysis of a single contact."""
        fields = contact['fields']
        
        print(f"\n{'='*60}")
        print(f"📇 CONTACT #{contact_num} {'(GUINEA PIG!)' if contact.get('is_guinea_pig') else ''}")
        print(f"{'='*60}")
        
        # Basic info
        print(f"👤 Name: {fields.get('full_name', 'N/A')}")
        print(f"🏢 Company: {fields.get('organization', 'N/A')}")
        print(f"💼 Job Title: {fields.get('job_title', 'N/A')}")
        
        # Emails
        emails = fields.get('emails', [])
        if emails:
            print(f"\n📧 Emails ({len(emails)}):")
            for email in emails:
                types_str = f" ({', '.join(email['types'])})" if email['types'] else ""
                print(f"   • {email['value']}{types_str}")
        else:
            print(f"\n📧 Emails: None")
        
        # Phones
        phones = fields.get('phones', [])
        if phones:
            print(f"\n📞 Phones ({len(phones)}):")
            for phone in phones:
                types_str = f" ({', '.join(phone['types'])})" if phone['types'] else ""
                print(f"   • {phone['value']}{types_str}")
        else:
            print(f"\n📞 Phones: None")
        
        # Notes
        if fields.get('note'):
            print(f"\n📝 Note: {fields['note'][:100]}{'...' if len(fields['note']) > 100 else ''}")
        
        # Raw data sample
        print(f"\n🔍 RAW vCard SAMPLE:")
        raw_lines = contact['raw_lines'][:10]  # First 10 lines
        for line in raw_lines:
            if line.strip():
                print(f"   {line.strip()}")
        if len(contact['raw_lines']) > 10:
            print(f"   ... and {len(contact['raw_lines']) - 10} more lines")
    
    def analyze_extraction_potential(self):
        """Analyze what we can extract reliably."""
        print(f"\n\n🎯 EXTRACTION POTENTIAL ANALYSIS")
        print(f"{'='*50}")
        
        total_contacts = len([c for c in self.contacts if not c.get('is_guinea_pig')])
        
        # Count fields
        with_name = 0
        with_company = 0
        with_emails = 0
        with_phones = 0
        with_job_title = 0
        
        email_types = {}
        phone_types = {}
        
        for contact in self.contacts:
            if contact.get('is_guinea_pig'):
                continue
                
            fields = contact['fields']
            
            if fields.get('full_name'):
                with_name += 1
            if fields.get('organization'):
                with_company += 1
            if fields.get('job_title'):
                with_job_title += 1
            if fields.get('emails'):
                with_emails += 1
                for email in fields['emails']:
                    for email_type in email['types']:
                        email_types[email_type] = email_types.get(email_type, 0) + 1
            if fields.get('phones'):
                with_phones += 1
                for phone in fields['phones']:
                    for phone_type in phone['types']:
                        phone_types[phone_type] = phone_types.get(phone_type, 0) + 1
        
        print(f"Sample size: {total_contacts} contacts")
        print(f"With name: {with_name}/{total_contacts} ({with_name/total_contacts*100:.1f}%)")
        print(f"With company: {with_company}/{total_contacts} ({with_company/total_contacts*100:.1f}%)")
        print(f"With job title: {with_job_title}/{total_contacts} ({with_job_title/total_contacts*100:.1f}%)")
        print(f"With emails: {with_emails}/{total_contacts} ({with_emails/total_contacts*100:.1f}%)")
        print(f"With phones: {with_phones}/{total_contacts} ({with_phones/total_contacts*100:.1f}%)")
        
        if email_types:
            print(f"\nEmail types found: {dict(email_types)}")
        if phone_types:
            print(f"Phone types found: {dict(phone_types)}")
    
    def recommend_extraction_strategy(self):
        """Recommend the best extraction strategy."""
        print(f"\n\n🚀 RECOMMENDED EXTRACTION STRATEGY")
        print(f"{'='*45}")
        
        print("Based on vCard analysis:")
        print("✅ Extract: Name + Company + Work Email")
        print("✅ Skip: Phone numbers (to avoid phantom contact issues)")
        print("✅ Priority: Contacts with WORK email type")
        print("✅ Fallback: Use first email if no WORK email")
        print("✅ Filter: Only contacts with email addresses")
        
        print("\n🎯 Next steps:")
        print("1. Build vCard parser targeting these fields")
        print("2. Test with this sample first")
        print("3. Scale to full 36.9MB file")
        print("4. Upload clean data to Notion")
    
    def run_reconnaissance(self):
        """Run the full reconnaissance mission."""
        print("🕵️ vCard RECONNAISSANCE MISSION")
        print("=" * 40)
        
        # Check file
        if not self.check_file_exists():
            return
        
        # Extract first contacts
        self.extract_first_contacts(12)
        
        # Find Guinea Pig
        self.find_guinea_pig()
        
        # Display each contact
        for i, contact in enumerate(self.contacts):
            contact_num = contact.get('index', i + 1)
            self.display_contact_analysis(contact, contact_num)
        
        # Analyze extraction potential
        self.analyze_extraction_potential()
        
        # Recommend strategy
        self.recommend_extraction_strategy()

if __name__ == "__main__":
    print("🕵️ vCard RECONNAISSANCE PROTOCOL")
    print("Analyzing vCard structure before full extraction")
    print("")
    
    recon = VCardReconnaissance()
    recon.run_reconnaissance()