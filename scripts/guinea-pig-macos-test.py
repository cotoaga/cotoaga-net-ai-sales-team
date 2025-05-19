#!/usr/bin/env python3
"""
Guinea Pig macOS Test: Extract JUST Guine Pig from macOS Contacts
to see exactly what data we can get.
"""

import subprocess
import json

def extract_guinea_pig_only():
    """Extract just Guine Pig contact to see real macOS data."""
    
    # Simplified AppleScript that searches for specific contact
    applescript = '''
    tell application "Contacts"
        -- Search for contacts containing "Guine"
        set foundContacts to (every person whose name contains "Guine")
        
        if (count of foundContacts) > 0 then
            set targetContact to item 1 of foundContacts
            
            -- Get basic properties (SKIP NOTES to avoid error)
            set firstName to first name of targetContact
            set lastName to last name of targetContact
            set fullName to name of targetContact
            set orgName to organization of targetContact
            set jobTitle to job title of targetContact
            
            -- Get emails
            set emailList to emails of targetContact
            set emailData to ""
            repeat with emailItem in emailList
                set emailData to emailData & (value of emailItem) & " (" & (label of emailItem) & "), "
            end repeat
            
            -- Get phones
            set phoneList to phones of targetContact
            set phoneData to ""
            repeat with phoneItem in phoneList
                set phoneData to phoneData & (value of phoneItem) & " (" & (label of phoneItem) & "), "
            end repeat
            
            -- Handle missing values
            if firstName is missing value then set firstName to ""
            if lastName is missing value then set lastName to ""
            if fullName is missing value then set fullName to ""
            if orgName is missing value then set orgName to ""
            if jobTitle is missing value then set jobTitle to ""
            
            -- Return structured data (NO NOTES!)
            return "FOUND:" & return & ¬
                "Full Name: " & fullName & return & ¬
                "First Name: " & firstName & return & ¬
                "Last Name: " & lastName & return & ¬
                "Organization: " & orgName & return & ¬
                "Job Title: " & jobTitle & return & ¬
                "Emails: " & emailData & return & ¬
                "Phones: " & phoneData & return & ¬
                "END_CONTACT"
        else
            return "NOT_FOUND: No contact containing 'Guine' found in macOS Contacts"
        end if
    end tell
    '''
    
    try:
        print("🐹 Searching for Guine Pig in macOS Contacts...")
        result = subprocess.run(['osascript', '-e', applescript], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ AppleScript error: {result.stderr}")
            return None
            
        output = result.stdout.strip()
        
        if "NOT_FOUND" in output:
            print("❌ Guine Pig not found in macOS Contacts!")
            print("Make sure you've added him to your macOS Contacts app first.")
            return None
        
        # Parse the output
        print("✅ Found Guine Pig! Here's what macOS Contacts reveals:")
        print("=" * 60)
        print(output)
        print("=" * 60)
        
        return output
        
    except Exception as e:
        print(f"❌ Error extracting guinea pig: {e}")
        return None

def analyze_extraction_results(contact_data):
    """Analyze what we successfully extracted."""
    if not contact_data:
        return
    
    print("\n📊 EXTRACTION ANALYSIS")
    print("=" * 40)
    
    lines = contact_data.split('\n')
    available_fields = []
    empty_fields = []
    
    for line in lines:
        if ':' in line and line.startswith(('Full Name:', 'First Name:', 'Last Name:', 
                                          'Organization:', 'Job Title:', 'Emails:', 
                                          'Phones:', 'Addresses:', 'Notes:')):
            field_name = line.split(':')[0]
            field_value = ':'.join(line.split(':')[1:]).strip()
            
            if field_value and field_value != "":
                available_fields.append(f"✅ {field_name}: Has data")
            else:
                empty_fields.append(f"❌ {field_name}: Empty")
    
    print("AVAILABLE DATA:")
    for field in available_fields:
        print(f"  {field}")
    
    print("\nMISSING DATA:")
    for field in empty_fields:
        print(f"  {field}")
    
    # Recommendations
    print("\n🎯 EXTRACTION RECOMMENDATIONS:")
    if len(available_fields) >= 4:
        print("✅ Good data quality - proceed with mass extraction")
    elif len(available_fields) >= 2:
        print("⚠️  Minimal data - consider manual enrichment")
    else:
        print("❌ Insufficient data - check guinea pig setup")

def suggest_optimizations():
    """Suggest improvements to the extraction script."""
    print("\n🔧 SCRIPT OPTIMIZATION SUGGESTIONS")
    print("=" * 40)
    print("Based on guinea pig test, we should:")
    print("1. Handle multiple emails/phones gracefully")
    print("2. Extract address for country detection")
    print("3. Skip note extraction (caused previous error)")
    print("4. Add error handling for missing fields")
    print("5. Format phone numbers consistently")
    print("6. Validate email addresses")

if __name__ == "__main__":
    print("🐹 GUINEA PIG macOS EXTRACTION TEST")
    print("=" * 50)
    print("Testing extraction of Guine Pig from macOS Contacts...")
    print("This will show us exactly what data we can get.")
    print("")
    
    # Extract guinea pig
    contact_data = extract_guinea_pig_only()
    
    if contact_data:
        # Analyze results
        analyze_extraction_results(contact_data)
        
        # Suggest optimizations
        suggest_optimizations()
        
        print("\n🎉 Guinea pig test complete!")
        print("Use this data to optimize the mass extraction script.")
    else:
        print("\n❌ Guinea pig test failed.")
        print("TROUBLESHOOTING:")
        print("1. Make sure Guine Pig exists in macOS Contacts")
        print("2. Check macOS privacy settings for script access")
        print("3. Try running from Terminal with admin privileges")