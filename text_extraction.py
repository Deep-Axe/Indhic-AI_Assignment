import requests
import re
import json
import datetime
import argparse

def get_verses(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        raw_text = resp.text
        print(f"Got data from URL, size: {len(raw_text)} chars")
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return []

    text_marker = raw_text.find("# Text")
    if text_marker == -1:
        print("Couldn't find the Text section")
        return []
    
    text_content = raw_text[text_marker:]
    print(f"Found Text section at position {text_marker}")
    
    text_lines = text_content.split('\n')
    
    verse_start = -1
    for idx, line in enumerate(text_lines):
        if "aṣṭāvakragītā" in line.lower():
            verse_start = idx + 1 
            break
    
    if verse_start < 0:  
        print("Couldn't locate the verses section")
        return []
    
    print(f"Verses begin at line {verse_start}")
    
    all_verses = []
    verse_lines = []
    
    for idx in range(verse_start, len(text_lines)):
        line = text_lines[idx].strip()
        
        if not line:
            continue
        
        if "// Avg_" in line:
            txt = line.split("//")[0].strip()
            
            num_match = re.search(r'Avg_(\d+\.\d+)', line)
            verse_num = num_match.group(1) if num_match else "?"
            
            verse_lines.append(txt)
            
            verse_text = "\n".join(verse_lines)
            
            all_verses.append({
                "verse": verse_text,
                "index": verse_num
            })
            
            verse_lines = []
        else:
            verse_lines.append(line)
    
    print(f"Total verses found: {len(all_verses)}")
    return all_verses

def main():
    parser = argparse.ArgumentParser(description='Extract Sanskrit verses from text.')
    parser.add_argument('--url', type=str, 
                        help='Where to download the text from')
    parser.add_argument('--output', type=str, default="astavakra_verses.json",
                        help='Where to save the JSON output')
    args = parser.parse_args()
    
    if not args.url:
        print("Error: Provide a URL with --url")
        return
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Starting extraction at {now}")
    
    meta = {
        "extracted_at": now,
        "extracted_by": "Deepam Ahuja",
        "source": args.url,
        "text": "Aṣṭāvakragītā"
    }
    
    verses = get_verses(args.url)
    
    if verses:
        data = {
            "metadata": meta,
            "verses": verses
        }
        
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        out_file = args.output
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print(f"Saved {len(verses)} verses to {out_file}")
        
        print("\nExample verses:")
        for v in verses[:3]:
            print(f"Verse {v['index']}: {v['verse'][:40]}...")
    else:
        print("No verses found. Check the URL and try again.")

if __name__ == "__main__":
    main()