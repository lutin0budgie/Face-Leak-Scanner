import face_recognition
import os
import sys

def get_folder_input(prompt_text):
    folder = input(prompt_text)
    folder = folder.strip().strip('"').strip("'")
    if not os.path.isdir(folder):
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)
    return folder

def get_multiple_folders(prompt_text):
    print(prompt_text)
    print("Separate folders with a comma, ex. /path/one, /path/two")
    folders = input("> ").split(",")
    folders = [f.strip().strip('"').strip("'") for f in folders if f.strip()]
    for f in folders:
        if not os.path.isdir(f):
            print(f"❌ Folder not found: {f}")
            sys.exit(1)
    return folders

def scan_folder(folder, known_encodings, tolerance=0.35):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total = len(files)
    for i, file in enumerate(files):
        try:
            img = face_recognition.load_image_file(os.path.join(folder, file))
            encs = face_recognition.face_encodings(img)
            if not encs:
                continue
            for ref in known_encodings:
                result = face_recognition.compare_faces([ref], encs[0], tolerance=tolerance)
                if result[0]:
                    print(f"✅ Match found: {file} in {folder}")
                    break
        except Exception as e:
            print(f"😓 Error processing {file}: {e}")
        if (i+1) % 100 == 0 or (i+1) == total:
            print(f"Progress: Checked {i+1}/{total} files in {folder}")

def main():
    print("----Face Leak Scanner----")

    # get reference folder from user
    reference_folder = get_folder_input("Enter path to your reference selfies folder: ")

    # get the data/leak folders you need to scan thru
    leak_folders = get_multiple_folders("Enter the path(s) to folder(s) you want to scan for your face:")

    # set tolerance value
    tol_level = input("Enter match tolerance (default 0.35, lower = stricter, higher = more matches): ").strip()
    tolerance = float(tol_level) if tol_level else 0.35

    # load all your reference selfies
    known_encodings = []
    for file in os.listdir(reference_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = face_recognition.load_image_file(os.path.join(reference_folder, file))
            encs = face_recognition.face_encodings(img)
            if encs:
                known_encodings.append(encs[0])
    print(f"Loaded {len(known_encodings)} reference faces")

    if not known_encodings:
        print("❌ No reference faces found! Exiting.")
        sys.exit(1)

    # Scan each leak folder
    for folder in leak_folders:
        print(f"\n==> Scanning folder: {folder} {'*'*20}")
        scan_folder(folder, known_encodings, tolerance=tolerance)

    print("\n[Done scanning all folders!]")
    print("If you see any [✓] matches, those images might contain your face.")

if __name__ == "__main__":
    main()
