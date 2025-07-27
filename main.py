import os
import json
import fitz  # PyMuPDF
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))


def gen_input_json(col_path, pdfs, cid, case, role, task, desc=""):
    data = {
        "challenge_info": {
            "challenge_id": cid,
            "test_case_name": case,
            "description": desc
        },
        "documents": [
            {"filename": f, "title": f.replace(".pdf", "")} for f in pdfs
        ],
        "persona": {"role": role},
        "job_to_be_done": {"task": task}
    }

    in_path = os.path.join(col_path, "challenge1b_input.json")
    with open(in_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Created: {in_path}")
    return data


def fetch_sections(pdf_path, max_sec=5):
    doc = fitz.open(pdf_path)
    secs, subs = [], []

    for pg_num in range(len(doc)):
        pg = doc[pg_num]
        blocks = pg.get_text("dict")["blocks"]

        for blk in blocks:
            if "lines" not in blk:
                continue
            text = "\n".join([s["text"] for l in blk["lines"] for s in l["spans"]]).strip()

            if 10 < len(text.split()) < 20:
                secs.append({
                    "document": os.path.basename(pdf_path),
                    "section_title": text,
                    "importance_rank": len(secs) + 1,
                    "page_number": pg_num + 1
                })
            elif len(text.split()) >= 40:
                subs.append({
                    "document": os.path.basename(pdf_path),
                    "refined_text": text,
                    "page_number": pg_num + 1
                })

            if len(secs) >= max_sec and len(subs) >= max_sec:
                break

    return secs[:max_sec], subs[:max_sec]


def gen_output_json(col_path, pdf_dir, role, task):
    pdfs = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    all_secs, all_subs = [], []

    for name in pdfs:
        path = os.path.join(pdf_dir, name)
        sec, sub = fetch_sections(path)
        all_secs.extend(sec)
        all_subs.extend(sub)

    out_data = {
        "metadata": {
            "input_documents": pdfs,
            "persona": role,
            "job_to_be_done": task,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": all_secs[:5],
        "subsection_analysis": all_subs[:5]
    }

    out_path = os.path.join(col_path, "challenge1b_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Output: {out_path}")


def main():
    for folder in os.listdir(ROOT):
        if not folder.lower().startswith("collection"):
            continue

        path = os.path.join(ROOT, folder)
        pdf_path = os.path.join(path, "PDFs")
        if not os.path.exists(pdf_path):
            print(f"⚠️ Skipped {path}: No PDFs folder.")
            continue

        pdfs = [f for f in os.listdir(pdf_path) if f.lower().endswith(".pdf")]
        if not pdfs:
            print(f"⚠️ Skipped {path}: No PDFs found.")
            continue

        role, task, desc = "Analyst", "Extract relevant information from given PDFs.", "Auto-gen"
        cid = f"round_1b_{folder[-1].zfill(3)}"
        case = f"collection_{folder[-1]}"

        # Custom overrides
        if "1" in folder:
            role = "Travel Planner"
            task = "Plan a trip of 4 days for a group of 10 college friends."
            desc = "France Travel"
        elif "2" in folder:
            role = "HR Professional"
            task = "Create and manage fillable forms for onboarding and compliance."
            desc = "Adobe Acrobat Learning"
        elif "3" in folder:
            role = "Food Contractor"
            task = "Prepare vegetarian buffet-style dinner menu for corporate gathering."
            desc = "Recipe Collection"

        in_data = gen_input_json(path, pdfs, cid, case, role, task, desc)
        gen_output_json(path, pdf_path, in_data["persona"]["role"], in_data["job_to_be_done"]["task"])


if __name__ == "__main__":
    main()
