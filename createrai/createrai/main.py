from flask import Flask, jsonify, request
import os
import re
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads"
ALLOWED_SCRIPT_EXTENSIONS = {"txt", "pdf", "doc", "docx"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "webm"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================
# CORS
# ==========================================

@app.after_request
def add_cors_headers(response):

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    return response


# ==========================================
# HELPERS
# ==========================================

def allowed_file(filename, allowed_extensions):

    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in allowed_extensions


def split_script(text):

    text = text.strip()

    if not text:
        return []

    # Split using paragraphs first
    paragraphs = re.split(r"\n\s*\n", text)

    sections = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) >= 10:
                sections.append(sentence)

    # If no sections were found
    if not sections:
        sections = [text]

    return sections[:20]


def create_demo_matches(sections):

    matches = []

    timestamps = [
        ("00:42", "01:18", 97),
        ("01:45", "02:22", 93),
        ("03:10", "03:52", 89),
        ("04:05", "04:41", 86),
        ("05:12", "05:49", 83)
    ]

    for index, section in enumerate(sections[:5]):

        start_time, end_time, score = timestamps[index]

        title = section

        if len(title) > 80:
            title = title[:77] + "..."

        matches.append({

            "id": index + 1,

            "title": title,

            "start_time": start_time,

            "end_time": end_time,

            "match_score": score

        })

    return matches


def create_clips(matches):

    clips = []

    platforms = [
        "Instagram Reels",
        "YouTube Shorts",
        "LinkedIn",
        "TikTok",
        "Facebook"
    ]

    for index, match in enumerate(matches):

        clips.append({

            "id": index + 1,

            "title": match["title"],

            "start_time": match["start_time"],

            "end_time": match["end_time"],

            "score": match["match_score"],

            "platform": platforms[
                index % len(platforms)
            ]

        })

    return clips


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return jsonify({

        "app": "CreatorAI",

        "message": "CreatorAI Backend is Running!",

        "status": "success",

        "version": "1.0.0"

    })


# ==========================================
# TEST
# ==========================================

@app.route("/api/test")
def test():

    return jsonify({

        "status": "success",

        "message": "CreatorAI API is working!",

        "ai": "ready"

    })


# ==========================================
# STATUS
# ==========================================

@app.route("/api/status")
def status():

    return jsonify({

        "status": "success",

        "creator_ai": "online",

        "backend": "online",

        "ai_engine": "development",

        "upload_system": "ready",

        "version": "1.0.0"

    })


# ==========================================
# CREATE PROJECT
# ==========================================

@app.route("/api/projects", methods=["POST"])
def create_project():

    data = request.get_json(silent=True) or {}

    project_name = data.get(
        "project_name",
        "Untitled Project"
    )

    content_type = data.get(
        "content_type",
        "Short Video"
    )

    project_id = str(uuid.uuid4())

    return jsonify({

        "status": "success",

        "message": "Project created successfully.",

        "project": {

            "id": project_id,

            "name": project_name,

            "content_type": content_type,

            "status": "created"

        }

    })


# ==========================================
# UPLOAD SCRIPT
# ==========================================

@app.route("/api/upload-script", methods=["POST"])
def upload_script():

    script_file = request.files.get("script")

    if not script_file:

        return jsonify({

            "status": "error",

            "message": "No script file was provided."

        }), 400

    if not allowed_file(
        script_file.filename,
        ALLOWED_SCRIPT_EXTENSIONS
    ):

        return jsonify({

            "status": "error",

            "message": "Unsupported script file."

        }), 400

    original_name = secure_filename(
        script_file.filename
    )

    unique_name = (
        str(uuid.uuid4())
        + "_"
        + original_name
    )

    path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    script_file.save(path)

    return jsonify({

        "status": "success",

        "message": "Script uploaded successfully.",

        "file": {

            "original_name": original_name,

            "saved_name": unique_name

        }

    })


# ==========================================
# UPLOAD VIDEO
# ==========================================

@app.route("/api/upload-video", methods=["POST"])
def upload_video():

    video_file = request.files.get("video")

    if not video_file:

        return jsonify({

            "status": "error",

            "message": "No video file was provided."

        }), 400

    if not allowed_file(
        video_file.filename,
        ALLOWED_VIDEO_EXTENSIONS
    ):

        return jsonify({

            "status": "error",

            "message": "Unsupported video format."

        }), 400

    original_name = secure_filename(
        video_file.filename
    )

    unique_name = (
        str(uuid.uuid4())
        + "_"
        + original_name
    )

    path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    video_file.save(path)

    return jsonify({

        "status": "success",

        "message": "Video uploaded successfully.",

        "file": {

            "original_name": original_name,

            "saved_name": unique_name

        }

    })


# ==========================================
# SCRIPT ANALYSIS
# ==========================================

@app.route("/api/analyze-script", methods=["POST"])
def analyze_script():

    text = ""

    if request.is_json:

        data = request.get_json(silent=True) or {}

        text = data.get("script", "")

    if not text:

        script_file = request.files.get("script")

        if script_file:

            try:

                text = script_file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            except Exception:

                text = ""

    if not text.strip():

        return jsonify({

            "status": "error",

            "message": "No script content provided."

        }), 400

    sections = split_script(text)

    return jsonify({

        "status": "success",

        "message": "Script analyzed successfully.",

        "section_count": len(sections),

        "sections": [

            {
                "id": index + 1,
                "text": section
            }

            for index, section
            in enumerate(sections)

        ]

    })


# ==========================================
# AI ANALYSIS
# ==========================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    script_file = request.files.get("script")

    video_file = request.files.get("video")

    pasted_script = request.form.get(
        "script_text",
        ""
    )

    # --------------------------------------
    # SCRIPT
    # --------------------------------------

    script_text = pasted_script

    if script_file:

        try:

            file_text = script_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            if file_text.strip():
                script_text = file_text

        except Exception:

            pass

    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not script_text.strip():

        return jsonify({

            "status": "error",

            "message": "Script content is required."

        }), 400

    if not video_file:

        return jsonify({

            "status": "error",

            "message": "Video file is required."

        }), 400

    # --------------------------------------
    # SAVE VIDEO
    # --------------------------------------

    video_name = secure_filename(
        video_file.filename
    )

    if not allowed_file(
        video_name,
        ALLOWED_VIDEO_EXTENSIONS
    ):

        return jsonify({

            "status": "error",

            "message": "Unsupported video format."

        }), 400

    analysis_id = str(uuid.uuid4())

    saved_video_name = (
        analysis_id
        + "_"
        + video_name
    )

    video_path = os.path.join(
        UPLOAD_FOLDER,
        saved_video_name
    )

    video_file.save(video_path)

    # --------------------------------------
    # SCRIPT SECTIONS
    # --------------------------------------

    sections = split_script(
        script_text
    )

    # --------------------------------------
    # MATCHING ENGINE
    # --------------------------------------
    #
    # Development matching engine.
    #
    # This currently generates structured
    # development results.
    #
    # A production AI/Whisper/video model
    # can be connected here later.
    #

    matches = create_demo_matches(
        sections
    )

    clips = create_clips(
        matches
    )

    # --------------------------------------
    # RESPONSE
    # --------------------------------------

    return jsonify({

        "status": "success",

        "message": "AI analysis completed.",

        "analysis_id": analysis_id,

        "script_sections": [

            {
                "id": index + 1,
                "text": section
            }

            for index, section
            in enumerate(sections)

        ],

        "matches": matches,

        "smart_clips": clips

    })


# ==========================================
# SMART CLIPS
# ==========================================

@app.route("/api/clips")
def get_clips():

    matches = create_demo_matches([

        "What is Data Science?",

        "Why Data Science matters",

        "Real world applications"

    ])

    return jsonify({

        "status": "success",

        "clips": create_clips(matches)

    })


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )